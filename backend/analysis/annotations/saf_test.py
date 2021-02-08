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
from .utils import clean_item

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

@pytest.mark.django_db
def test_reader():
    '''test annotation reader: parse a transcript, write an annotation file, read it
    back, and check if it matches'''
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
    true_annotations = true_results.annotations

    # export annotation file
    spreadsheet = v2_to_xlsx(true_results, method)
    spreadsheet.save(xlsx_path)

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
            #test word
            assert word.text.lower() == true_word.word.lower()

            #test index
            assert word.idx == true_word.begin + 1

            #test annotations
            anns = word.annotations
            true_anns = true_word.hits

            def matching(ann, true_ann):
                    matching_level = true_ann['level'].lower() == ann.level
                    matching_label =  clean_item(true_ann['item']) == ann.label
                    matching_fase = true_ann['fase'] == ann.fase
                    return matching_level and matching_label and matching_fase

            for true_ann in true_anns:
                #check if true annotation has a match in the found annotations
                assert any(ann for ann in anns if matching(ann, true_ann))

            for ann in anns:
                #check if found annotation has a match in the true annotations
                assert any(true_ann for true_ann in true_anns if matching(ann, true_ann))