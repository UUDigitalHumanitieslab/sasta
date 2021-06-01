import os

import pytest
from analysis.models import AssessmentMethod, Corpus, Transcript
from analysis.parse.parse import parse_and_create
from analysis.query.run import query_transcript
from analysis.query.xlsx_output import v1_to_xlsx, v2_to_xlsx
from django.core.files import File

from .safreader import SAFReader
from .utils import clean_item

BASE_DIR = os.path.dirname(os.path.realpath(__file__))


def create_annotation(filename, cha_path, xlsx_path, method, corpus):
    # parse chat file
    with open(cha_path, 'rb') as cha_content:
        transcript = Transcript(
            name=filename,
            status='converted',
            corpus=corpus,
            extracted_filename=filename + '.cha'
        )
        transcript.save()
        transcript.content.save(filename + '.cha', File(cha_content))

    parse_and_create(transcript)

    # query
    all_results, queries_with_funcs = query_transcript(transcript, method, annotate=True, only_inform=False)

    # export annotation file
    spreadsheet = v2_to_xlsx(all_results, method)
    spreadsheet.save(xlsx_path)

    return all_results, queries_with_funcs


@pytest.mark.django_db
def test_reader():
    '''test annotation reader: parse a transcript, write an annotation file, read it
    back, and check if annotations match'''
    method = AssessmentMethod.objects.first()
    corpus = Corpus.objects.first()

    # paths
    filename = 'test_sample_1'
    cha_path = os.path.join(BASE_DIR, 'test_files', filename + '.cha')
    xlsx_path = os.path.join(BASE_DIR, 'test_files', filename + '.xlsx')

    # parse chat and export annotation file
    true_results, _ = create_annotation(filename, cha_path, xlsx_path, method, corpus)
    true_annotations = true_results.annotations

    # read annotation file
    reader = SAFReader(xlsx_path, method)

    # compare result from reader with original results
    # utterance ids
    found_utt_ids = set(utt.utt_id for utt in reader.document.utterances)
    true_utt_ids = set(true_annotations.keys())
    assert found_utt_ids == true_utt_ids

    # annotations for each utterance
    for utt in reader.document.utterances:
        words = utt.words
        true_words = true_annotations[utt.utt_id]
        assert len(words) == len(true_words)

        for word, true_word in zip(words, true_words):
            # test word
            assert word.text.lower() == true_word.word.lower()

            # test index
            assert word.idx == true_word.begin + 1

            # test annotations
            anns = word.annotations
            true_anns = true_word.hits

            def matching(ann, true_ann):
                matching_level = true_ann['level'].lower() == ann.level
                matching_label = clean_item(true_ann['item']) == ann.label
                matching_fase = true_ann['fase'] == ann.fase
                return matching_level and matching_label and matching_fase

            for true_ann in true_anns:
                # check if true annotation has a match in the found annotations
                assert any(ann for ann in anns if matching(ann, true_ann))

            for ann in anns:
                # check if found annotation has a match in the true annotations
                assert any(true_ann for true_ann in true_anns if matching(ann, true_ann))


@pytest.mark.django_db
def test_annotation_to_query():
    '''test conversion of annotation reader output to query results: parse a
    transcript, write an annotation file and a query file. Read the annotation file,
    make new query file based on annotations and compare to real query file.'''

    method = AssessmentMethod.objects.first()
    corpus = Corpus.objects.first()

    # paths
    filename = 'test_sample_1'
    cha_path = os.path.join(BASE_DIR, 'test_files', filename + '.cha')
    annotations_path = os.path.join(BASE_DIR, 'test_files', filename + '.xlsx')

    # parse chat and export annotation file
    true_all_results, true_queries_with_funcs = create_annotation(filename, cha_path, annotations_path, method, corpus)

    true_query_output = v1_to_xlsx(true_all_results, true_queries_with_funcs)

    # read annotations and generate query file
    reader = SAFReader(annotations_path, method)
    query_output = reader.document.query_output()

    # save query output for inspection
    query_output.save(os.path.join(BASE_DIR, 'test_files', filename + '_query.xlsx'))
    true_query_output.save(os.path.join(BASE_DIR, 'test_files', filename + '_query_true.xlsx'))

    # compare query_output and true_query_output
    assert len(query_output.worksheets) == len(true_query_output.worksheets)
    for sheet, true_sheet in zip(query_output, true_query_output):
        assert sheet.dimensions == true_sheet.dimensions
        for row, true_row in zip(sheet.rows, true_sheet.rows):
            for cell, true_cell in zip(row, true_row):
                assert cell.value == true_cell.value
