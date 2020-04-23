import errno
import logging
import os
from shutil import copyfile
from typing import Any, Dict
from zipfile import ZipFile

import docx.document
import docx.oxml.table
import docx.oxml.text.paragraph
import docx.table
import docx.text.paragraph
import pandas as pd
from django.core.files import File
from django.db.utils import IntegrityError
from docx import Document
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill

logger = logging.getLogger('sasta')

ROMAN_NUMS = [None, 'I', 'II', 'III',
              'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X']

CORE_PROCESS_STR, POST_PROCESS_STR = 'core', 'post'
CORE_PROCESS, POST_PROCESS = 0, 1

LEVELS = ['Sz', 'Zc', 'Wg', 'VVW']


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

    except:
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
        corpus=file.corpus
    )
    transcript.save()
    transcript.content.save(filename, File(file_content))
    file_content.close()
    return transcript


def iter_paragraphs(parent, recursive=True):
    """
    Yield each paragraph and table child within *parent*, in document order.
    Each returned value is an instance of Paragraph. *parent*
    would most commonly be a reference to a main Document object, but
    also works for a _Cell object, which itself can contain paragraphs and tables.
    """
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


def docx_to_txt(filepath):
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
        os.remove(filepath)
        logger.info(f'DOC2TXT:\tconverting succes')
        return txt_path
    except Exception as error:
        logger.error(f'DOC2TXT:\tconverting failed')
        logger.error(error)
        print('error in docx_to_txt:\t', error)


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
                              true_values=['yes'], false_values=['no'])
    column_names = [c.lower() for c in dataframe.columns]
    dataframe.columns = column_names
    dataframe.rename(columns={'id': 'query_id'}, inplace=True)
    dataframe = dataframe.where(dataframe.notnull(), None)

    for _i, series in dataframe.iterrows():
        # workaround for getting value to None instead of NaN
        try:
            series.fase = int(series.fase)
        except:
            series.fase = None
        series.process = getprocess(series.process)
        create_query_from_series(series, method)
    logger.info(f'TAM-Reader:\treading done')


def create_query_from_series(series: pd.Series, method) -> None:
    from .models import AssessmentQuery  # pylint: disable=import-outside-toplevel

    instance = AssessmentQuery(method=method, **series)
    try:
        instance.save()
    except IntegrityError as error:
        logger.error(error)


def v1_to_xlsx(data: Dict[str, Any]):
    # writes the v1 results as excel file
    # rows contain query_id, utt_id, and number of matches
    # query_id is only written if different from previous row
    try:
        wb = Workbook()
        worksheet = wb.active

        # header
        worksheet.append(['Query', 'Item', 'Fase', 'Utterance', 'Matches'])
        header = worksheet["1:1"]
        for cell in header:
            cell.font = Font(bold=True)

        for key, entry in sorted(data['results'].items(), key=lambda x: x[1]['fase']):
            entry = data['results'][key]
            counter = entry['matches']
            for i, ele in enumerate(counter):
                row = [key,
                       entry['item'],
                       entry['fase'] if entry['fase'] != 0 else 'nvt'
                       ] if i == 0 else [None, None, None]
                row += [ele, counter[ele]]
                worksheet.append(row)
        return wb
    except Exception as e:
        logger.exception(e)


def v2_to_xlsx(data: Dict[str, Any]):
    try:
        wb = Workbook()
        worksheet = wb.active

        items = sorted(data['results'].items())
        max_words = max([len(words) for (_, words) in items])
        word_headers = [f'Word{i}' for i in range(1, max_words+1)]
        headers = ['ID', 'Level'] + word_headers + \
            ['Dummy', 'Unaligned', 'Fases', 'Commentaar']
        worksheet.append(headers)
        # levels = sorted(list(data['levels']))
        levels = LEVELS

        for utt_id, words in items:
            # Utt row, containing the word tokens
            words_row = [utt_id, 'Utt'] + [w.word for w in words]

            # trailing empty cells, necesarry?
            words_row += [None]*(len(headers) - len(words_row))

            # a cell for each word, and one to record phases
            level_rows = [[utt_id, level]+[set([]) for _ in range(max_words+1)] + [None] + [[]]
                          for level in levels]

            # iterate over hits
            # fill in items on their respective level
            # leaving cells without hits as None
            for i_word, word in enumerate(words):
                for hit in word.hits:
                    i_level = levels.index(hit['level'])
                    level_rows[i_level][i_word+2].add(hit['item'])
                    try:
                        level_rows[i_level][-1].append(
                            ROMAN_NUMS[int(hit['fase'])])
                    except:
                        pass

            worksheet.append(words_row)
            # condense cells and append to xlsx
            for row in level_rows:
                row = [','.join(sorted(cell)) or None
                       if (isinstance(cell, set) or isinstance(cell, list))
                       else cell
                       for cell in row]
                worksheet.append(row)

        # Formatting
        header = worksheet["1:1"]
        for cell in header:
            # bold headers
            cell.font = Font(bold=True)

        nth_row = len(levels) + 1
        for i, row in enumerate(worksheet.rows):
            # yellow background for each utterance row
            if i % nth_row == 1:
                for cell in row:
                    cell.fill = PatternFill(
                        start_color="ffff00", end_color="ffff00", fill_type="solid")
        return wb
    except Exception as e:
        print(e)
