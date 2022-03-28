import glob
import json
import os.path as op

import pytest
from analysis.convert.convert import convert
from analysis.models import (AssessmentMethod, Corpus, MethodCategory,
                             Transcript)
from django.conf import settings
from django.core.files import File
from parse.parse_utils import create_utterance_objects

CORRECTIONS = '{"Insertion": [["23", "Insertion", "[\'ik\']", "SASTA", "Small Clause Treatment", "None", "fftje [: eventjes] passen?", "ik wil eventjes passen ?"], ["23", "Insertion", "[\'wil\']", "SASTA", "Small Clause Treatment", "None", "fftje [: eventjes] passen?", "ik wil eventjes passen ?"]], "Retracing": [["36", "Retracing", "[\'di\', \'zij\', \'hem\']", "CHAT", "None", "None", "nee dat wat <di zij hem> [//] hij verkoopt.", "dat wat hij verkoopt ."]], "parsed_as": [["4", "parsed_as", "kan nog een dingetje eraan .", "SASTA", "Correction", "None", "ja kan no(g) een dingetje d(e)raan.", "kan nog een dingetje eraan ."], ["7", "parsed_as", "even kijken waar .", "SASTA", "Correction", "None", "effe kijken waar.", "even kijken waar ."], ["11", "parsed_as", "je moet dan eventjes erop zetten .", "SASTA", "Correction", "None", "je moet dan effjes erop zetten.", "je moet dan eventjes erop zetten ."], ["12", "parsed_as", "dan ga ik dit eventjes maken .", "SASTA", "Correction", "None", "dan ga ik dit effjes maken.", "dan ga ik dit eventjes maken ."], ["19", "parsed_as", "deze past nergens meer op .", "SASTA", "Correction", "None", "ja &de &de deze past nerke [: nergens] meer op.", "deze past nergens meer op ."], ["20", "parsed_as", "dan zetten we dit effje aan de kant .", "SASTA", "Correction", "None", "dan zetten we deze effje aan de kant.", "dan zetten we dit effje aan de kant ."], ["22", "parsed_as", "kijk hier hebben wij heel veel .", "SASTA", "Correction", "None", "ja kij(k) hier hebben wij heel veel.", "kijk hier hebben wij heel veel ."], ["23", "parsed_as", "ik wil eventjes passen ?", "SASTA", "Correction", "None", "fftje [: eventjes] passen?", "ik wil eventjes passen ?"], ["24", "parsed_as", "teil .", "SASTA", "Correction", "None", "klik.", "teil ."], ["28", "parsed_as", "trappetje .", "SASTA", "Correction", "None", "ja trarpje [: trappetje].", "trappetje ."], ["32", "parsed_as", "alleen maar worstjes .", "SASTA", "Correction", "None", "nee wee [: alleen] maar wortjes [: worstjes].", "alleen maar worstjes ."], ["36", "parsed_as", "dat wat hij verkoopt .", "SASTA", "Correction", "None", "nee dat wat <di zij hem> [//] hij verkoopt.", "dat wat hij verkoopt ."]], "Replacement": [["16", "Replacement", "[\'gaan\']", "CHAT", "None", "None", "ander(s) kaat [: gaan] te [: de] tiern [: dieren] door \'t hek lopen.", null], ["16", "Replacement", "[\'de\']", "CHAT", "None", "None", "ander(s) kaat [: gaan] te [: de] tiern [: dieren] door \'t hek lopen.", null], ["16", "Replacement", "[\'dieren\']", "CHAT", "None", "None", "ander(s) kaat [: gaan] te [: de] tiern [: dieren] door \'t hek lopen.", null], ["19", "Replacement", "[\'nergens\']", "CHAT", "None", "None", "ja &de &de deze past nerke [: nergens] meer op.", "deze past nergens meer op ."], ["23", "Replacement", "[\'eventjes\']", "CHAT", "None", "None", "fftje [: eventjes] passen?", "ik wil eventjes passen ?"], ["28", "Replacement", "[\'trappetje\']", "CHAT", "None", "None", "ja trarpje [: trappetje].", "trappetje ."], ["30", "Replacement", "[\'parasol\']", "CHAT", "None", "None", "&oeps de parasel [: parasol].", null], ["32", "Replacement", "[\'alleen\']", "CHAT", "None", "None", "nee wee [: alleen] maar wortjes [: worstjes].", "alleen maar worstjes ."], ["32", "Replacement", "[\'worstjes\']", "CHAT", "None", "None", "nee wee [: alleen] maar wortjes [: worstjes].", "alleen maar worstjes ."], ["33", "Replacement", "[\'worstje\']", "CHAT", "None", "None", "kijk hier zit een wortje [: worstje] in.", null], ["34", "Replacement", "[\'staat\']", "CHAT", "None", "None", "wat taat [: staat] hierop?", null]], "GrammarError": [["20", "GrammarError", "deheterror", "SASTA", "Error", "None", "dan zetten we deze effje aan de kant.", "dan zetten we dit effje aan de kant ."]], "Disambiguation": [["24", "Disambiguation", "Avoid unknown reading", "SASTA", "Lexicon", "None", "klik.", "teil ."]], "ExtraGrammatical": [["4", "ExtraGrammatical", "ja, nee or nou filled pause", "SASTA", "Syntax", "None", "ja kan no(g) een dingetje d(e)raan.", "kan nog een dingetje eraan ."], ["19", "ExtraGrammatical", "ja, nee or nou filled pause", "SASTA", "Syntax", "None", "ja &de &de deze past nerke [: nergens] meer op.", "deze past nergens meer op ."], ["22", "ExtraGrammatical", "ja, nee or nou filled pause", "SASTA", "Syntax", "None", "ja kij(k) hier hebben wij heel veel.", "kijk hier hebben wij heel veel ."], ["28", "ExtraGrammatical", "ja, nee or nou filled pause", "SASTA", "Syntax", "None", "ja trarpje [: trappetje].", "trappetje ."], ["32", "ExtraGrammatical", "ja, nee or nou filled pause", "SASTA", "Syntax", "None", "nee wee [: alleen] maar wortjes [: worstjes].", "alleen maar worstjes ."], ["36", "ExtraGrammatical", "ja, nee or nou filled pause", "SASTA", "Syntax", "None", "nee dat wat <di zij hem> [//] hij verkoopt.", "dat wat hij verkoopt ."]], "Phonological Fragment": [["8", "Phonological Fragment", "[\'&hoo\']", "CHAT", "None", "None", "&hoo hij kom(t).", null], ["10", "Phonological Fragment", "[\'&oo\']", "CHAT", "None", "None", "&oo hij fiet(st) niet meer.", null], ["15", "Phonological Fragment", "[\'&nie\']", "CHAT", "None", "None", "hij kan &nie nie(t) meer daarheen (s)chuiven.", null], ["19", "Phonological Fragment", "[\'&de\']", "CHAT", "None", "None", "ja &de &de deze past nerke [: nergens] meer op.", "deze past nergens meer op ."], ["19", "Phonological Fragment", "[\'&de\']", "CHAT", "None", "None", "ja &de &de deze past nerke [: nergens] meer op.", "deze past nergens meer op ."], ["27", "Phonological Fragment", "[\'&uhh\']", "CHAT", "None", "None", "&uhh wat i(s) dit ook alweer?", null], ["30", "Phonological Fragment", "[\'&oeps\']", "CHAT", "None", "None", "&oeps de parasel [: parasol].", null]], "Informal Pronunciation": [["7", "Informal Pronunciation", "Alternative Pronunciation", "SASTA", "Pronunciation", "None", "effe kijken waar.", "even kijken waar ."], ["11", "Informal Pronunciation", "Alternative Pronunciation", "SASTA", "Pronunciation", "None", "je moet dan effjes erop zetten.", "je moet dan eventjes erop zetten ."], ["12", "Informal Pronunciation", "Alternative Pronunciation", "SASTA", "Pronunciation", "None", "dan ga ik dit effjes maken.", "dan ga ik dit eventjes maken ."]], "Insertion Token Mapping": [["23", "Insertion Token Mapping", "[None, None, 30, 50, 60]", "SASTA", "Token Mapping", "None", "fftje [: eventjes] passen?", "ik wil eventjes passen ?"]], "Alternative Pronunciation": [["4", "Alternative Pronunciation", "d-onset on er", "SASTA", "Pronunciation", "None", "ja kan no(g) een dingetje d(e)raan.", "kan nog een dingetje eraan ."]]}'


@pytest.fixture
def cha_testfiles_dir():
    return op.join(settings.BASE_DIR, 'analysis', 'annotations', 'test_files')


@pytest.fixture
def tarsp_category(db):
    obj = MethodCategory.objects.create(name='TARSP', zc_embeddings=True, levels=['Sz', 'Zc', 'Wg', 'VVW'], marking_postcodes=['[+ G]'])
    yield obj
    obj.delete()


@pytest.fixture
def stap_category(db):
    obj = MethodCategory.objects.create(name='STAP', zc_embeddings=False, levels=['Complexiteit', 'Grammaticale fout'], marking_postcodes=['[+ G]', '[+ VU]'])
    yield obj
    obj.delete()


@pytest.fixture
def tarsp_method(db, tarsp_category):
    method_dir = op.join(settings.BASE_DIR, 'sastadev', 'methods')
    file = glob.glob(f'{method_dir}/TARSP Index Current.xlsx')[0]
    with open(file, 'rb') as f:
        wrapped_file = File(f)
        instance = AssessmentMethod(name='tarsp_test_method', category=tarsp_category)
        instance.content.save(op.basename(file), wrapped_file)
    yield instance
    instance.delete()


@pytest.fixture
def asta_method(db, asta_category):
    method_dir = op.join(settings.BASE_DIR, 'sastadev', 'methods')
    file = glob.glob(f'{method_dir}/ASTA Index Current.xlsx')[0]
    with open(file, 'rb') as f:
        wrapped_file = File(f)
        instance = AssessmentMethod(name='asta_test_method', category=asta_category)
        instance.content.save(op.basename(file), wrapped_file)
    yield instance
    instance.delete()


@pytest.fixture
def tarsp_corpus(db, admin_user, tarsp_method, tarsp_category):
    obj = Corpus.objects.create(
        user=admin_user,
        name='tarsp_test_corpus',
        status='created',
        default_method=tarsp_method,
        method_category=tarsp_category
    )
    yield obj
    obj.delete()


@pytest.fixture
def tarsp_transcript(db, tarsp_corpus, cha_testfiles_dir):
    obj = Transcript.objects.create(
        name='tarsp_sample_5',
        status=Transcript.PARSED,
        corpus=tarsp_corpus
    )
    with open(op.join(cha_testfiles_dir, 'sample_5.cha'), 'rb') as f:
        obj.content.save('sample_5.cha', File(f))
    convert(obj)
    with open(op.join(cha_testfiles_dir, 'sample_5.xml'), 'rb') as f:
        obj.parsed_content.save('sample_5.xml', File(f))
    obj.corrections = json.loads(CORRECTIONS)
    obj.status = Transcript.PARSED
    create_utterance_objects(obj)
    obj.save()
    yield obj
    obj.delete()
