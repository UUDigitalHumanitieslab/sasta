# from models import AssessmentMethod, AssessmentQuery
import os
import pandas as pd
from docx import Document
from django.db.utils import IntegrityError


import docx.document
import docx.oxml.table
import docx.oxml.text.paragraph
import docx.table
import docx.text.paragraph

import logging
logger = logging.getLogger('sasta')


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
        return txt_path
    except Exception as error:
        logger.error(error)
        print('error in docx_to_txt:\t', error)


# def docx_to_txt(filepath):
#     '''converts .docx file to .txt file'''
#     try:
#         document = Document(filepath)
#         txt_path = filepath.replace('.docx', '.txt')
#         with open(txt_path, 'w', encoding='utf-8') as txt_file:
#             for para in document.paragraphs:
#                 print(para.text, file=txt_file)
#         os.remove(filepath)
#         return txt_path
#     except Exception as error:
#         print(error)


def read_TAM(method) -> None:
    filepath = method.content.path
    dataframe = pd.read_excel(filepath,
                              true_values=['yes'], false_values=['no'])
    column_names = [c.lower() for c in dataframe.columns]
    column_names[0] = 'query_id'
    dataframe.columns = column_names
    dataframe.rename(columns={'fase': 'phase'}, inplace=True)
    dataframe = dataframe.where(dataframe.notnull(), None)

    for _i, series in dataframe.iterrows():
        # workaround for getting value to None instead of NaN
        try:
            series.phase = int(series.phase)
        except:
            series.phase = None
        create_query_from_series(series, method)


def create_query_from_series(series: pd.Series, method) -> None:
    from .models import AssessmentQuery  # pylint: disable=import-outside-toplevel

    instance = AssessmentQuery(method=method, **series)
    try:
        instance.save()
    except IntegrityError as error:
        logger.error(error)
        pass
