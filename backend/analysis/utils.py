# from models import AssessmentMethod, AssessmentQuery
import os
import sys
# currentdir = os.path.dirname(os.path.realpath(__file__))
# parentdir = os.path.dirname(currentdir)
# sys.path.append(parentdir)
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sasta.settings")

import django
# django.setup()

from models import AssessmentMethod, AssessmentQuery
import pandas as pd
import numpy as np
from docx import Document


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


def read_TAM(filepath: str) -> None:
    AssessmentMethod.objects.all().delete()
    AssessmentQuery.objects.all().delete()

    name, _ = os.path.splitext(os.path.basename(filepath))
    dataframe = pd.read_excel(filepath,
                              true_values=['yes'], false_values=['no'])
    column_names = [c.lower() for c in dataframe.columns]
    column_names[0] = 'query_id'
    dataframe.columns = column_names
    dataframe.rename(columns={'fase': 'phase'}, inplace=True)
    dataframe = dataframe.where(dataframe.notnull(), None)

    tam, _created = AssessmentMethod.objects.get_or_create(name=name)
    for i, series in dataframe.iterrows():
        create_query_from_series(series, tam)


def create_query_from_series(series: pd.Series, method: AssessmentMethod) -> None:
    # workaround for getting value to None instead of NaN
    try:
        series.phase = int(series.phase)
    except:
        series.phase = None
    instance = AssessmentQuery(method=method, **series)
    
    try:
        instance.save()
    except django.db.utils.IntegrityError as e:
        #TODO: log
        print(e)
    pass
