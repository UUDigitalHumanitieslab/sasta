# from models import AssessmentMethod, AssessmentQuery
import os
import pandas as pd
from docx import Document
from django.db.utils import IntegrityError


def docx_to_txt(filepath):
    '''converts .docx file to .txt file'''
    try:
        document = Document(filepath)
        txt_path = filepath.replace('.docx', '.txt')
        with open(txt_path, 'w', encoding='utf-8') as txt_file:
            for para in document.paragraphs:
                print(para.text, file=txt_file)
        os.remove(filepath)
        return txt_path
    except Exception as error:
        print(error)


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
    except IntegrityError:
        #TODO: log
        # print(e)
        pass
