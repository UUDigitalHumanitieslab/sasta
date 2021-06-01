import errno
import logging
import os
from shutil import copyfile
from zipfile import ZipFile

import docx.document
import docx.oxml.table
import docx.oxml.text.paragraph
import docx.table
import docx.text.paragraph
import pandas as pd
from django.core.files import File
from django.core.files.base import ContentFile
from django.db.utils import IntegrityError
from docx import Document

logger = logging.getLogger('sasta')

ROMAN_NUMS = [None, 'I', 'II', 'III',
              'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X']

CORE_PROCESS_STR, POST_PROCESS_STR = 'core', 'post'
CORE_PROCESS, POST_PROCESS = 0, 1

LEVELS = ['Sz', 'Zc', 'Wg', 'VVW']


def get_items_list(str, sep):
    rawresult = str.split(sep)
    cleanresult = [w.strip().lower() for w in rawresult]
    if cleanresult == ['']:
        return []
    return cleanresult


def extract(file):
    file.status = 'extracting'
    file.save()

    try:
        created_transcripts = []
        (origin_dir, filename) = os.path.split(file.content.path)
        target_dir = origin_dir.replace('uploads', 'extracted')
        # extract zipped files
        if filename.lower().endswith(".zip"):
            with ZipFile(file.content) as zipfile:
                for zip_name in zipfile.namelist():
                    zipfile.extract(zip_name, path=target_dir)
                    extracted_path = os.path.join(target_dir, zip_name)
                    created_transcripts.append(
                        create_transcript(file, extracted_path))
        # copy all others
        else:
            try:
                os.makedirs(target_dir)
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise
            new_path = os.path.join(target_dir, filename)
            copyfile(file.content.path, os.path.join(target_dir, filename))
            created_transcripts.append(create_transcript(file, new_path))

        file.status = 'extracted'
        file.save()
        return created_transcripts

    except Exception:
        file.status = 'extraction-failed'
        file.save()
        raise


def create_transcript(file, content_path):
    from .models import Transcript  # pylint: disable=import-outside-toplevel
    if content_path.endswith('.docx'):
        docx_to_txt(content_path)
        content_path = content_path.replace('.docx', '.txt')

    _dir, filename = os.path.split(content_path)

    file_content = open(content_path, 'rb')
    transcript = Transcript(
        name=filename.strip('.txt'),
        status='created',
        corpus=file.corpus,
        extracted_filename=content_path
    )
    transcript.save()
    transcript.content.save(filename, File(file_content))
    file_content.close()
    return transcript


def iter_paragraphs(parent, recursive=True):
    if isinstance(parent, docx.document.Document):
        parent_elm = parent.element.body
    elif isinstance(parent, docx.table._Cell):
        parent_elm = parent._tc
    else:
        raise TypeError(repr(type(parent)))

    for child in parent_elm.iterchildren():
        if isinstance(child, docx.oxml.text.paragraph.CT_P):
            yield docx.text.paragraph.Paragraph(child, parent)
        elif isinstance(child, docx.oxml.table.CT_Tbl):
            if recursive:
                table = docx.table.Table(child, parent)
                for row in table.rows:
                    for cell in row.cells:
                        for child_paragraph in iter_paragraphs(cell):
                            yield child_paragraph


def docx_to_txt(filepath, delete_docx=True):
    logger.info(f'DOC2TXT:\tconverting {os.path.basename(filepath)}')
    try:
        document = Document(filepath)
        txt_path = filepath.replace('.docx', '.txt')
        xsid_counter = 1
        with open(txt_path, 'w', encoding='utf-8') as txt_file:
            for paragraph in iter_paragraphs(document):
                par_pr = paragraph._p.pPr
                if par_pr is not None:
                    num_pr = par_pr.numPr
                    if num_pr is not None:
                        print(xsid_counter, paragraph.text, file=txt_file)
                        xsid_counter += 1
                    else:
                        print(paragraph.text, file=txt_file)
                else:
                    print(paragraph.text, file=txt_file)
        if delete_docx:
            os.remove(filepath)
        logger.info('DOC2TXT:\tconverting succes')
        return txt_path
    except Exception as error:
        logger.error('DOC2TXT:\tconverting failed')
        logger.exception(error)


def getprocess(process):
    if process.lower() == CORE_PROCESS_STR:
        return CORE_PROCESS
    elif process.lower() == POST_PROCESS_STR:
        return POST_PROCESS
    else:
        logger.error('Illegal value for process {}'.format(process))
        return -1


def read_TAM(method) -> None:
    filepath = method.content.path
    logger.info(f'TAM-Reader:\treading {os.path.basename(filepath)}')
    dataframe = pd.read_excel(filepath,
                              true_values=['yes'], false_values=['no', 'ignore'])
    dataframe.columns = [c.lower() for c in dataframe.columns]
    dataframe.rename(columns={'id': 'query_id'}, inplace=True)
    dataframe = dataframe.where(dataframe.notnull(), None)
    dataframe = dataframe.loc[:, ~dataframe.columns.str.contains('^unnamed')]

    for _i, series in dataframe.iterrows():
        # workaround for getting value to None instead of NaN
        try:
            series.fase = int(series.fase)
        except Exception:
            series.fase = None
        series.process = getprocess(series.process)
        create_query_from_series(series, method)
    logger.info('TAM-Reader:\treading done')


def create_query_from_series(series: pd.Series, method) -> None:
    from .models import AssessmentQuery

    instance = AssessmentQuery(method=method, **series)
    try:
        instance.save()
    except IntegrityError as error:
        logger.exception(error)


class StreamFile(ContentFile):
    """
    Django doesn't provide a File wrapper suitable
    for file-like objects (eg StringIO)
    """

    def __init__(self, stream):
        super(ContentFile, self).__init__(stream)
        stream.seek(0, 2)
        self.size = stream.tell()
