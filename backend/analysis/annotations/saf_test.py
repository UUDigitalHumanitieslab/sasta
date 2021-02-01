import pytest
import os
from .safreader import SAFReader
from django.core.files import File
from ..models import (AssessmentMethod, AssessmentQuery, Corpus, Transcript,
                             Utterance)
from ..convert.convert import convert
from ..parse.parse import parse_and_create
from ..query.run import query_transcript, run_core_queries
from ..query.xlsx_output import v2_to_xlsx

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

@pytest.mark.django_db
def test_reader():
    log_file = open('test_log.txt', 'w')

    log = lambda x : log_file.write(str(x) + '\n')

    method = AssessmentMethod.objects.first()
    corpus = Corpus.objects.first()

    # paths
    filename = 'test_sample_1'
    cha_path = os.path.join(BASE_DIR, 'test_files', filename + '.cha')
    xlsx_path = os.path.join(BASE_DIR, 'test_files', filename + '.xlsx')

    # parse chat file
    with open(cha_path, 'rb') as cha_content:
        transcript = Transcript(
            name = filename, 
            status = 'converted',
            corpus = corpus,
            extracted_filename = filename + '.cha'
        )
        transcript.save()
        transcript.content.save(filename + '.cha', File(cha_content))

    parse_and_create(transcript)

    # query
    true_results, queries_with_funcs = query_transcript(transcript, method, annotate=True)

    # export annotation file
    spreadsheet = v2_to_xlsx(true_results, method)
    spreadsheet.save(xlsx_path)

    # read annotation file
    reader = SAFReader(xlsx_path, method)

    # TODO: compare result from reader with original results

    log_file.close()
    assert False
