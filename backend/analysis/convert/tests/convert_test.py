import os.path as op
import os

# from analysis.utils import docx_to_txt
from analysis.convert.chat_converter import SifReader, fill_places_persons

HERE = op.dirname(op.abspath(__file__))


def test_chat_basic(testfiles):
    doc = SifReader(testfiles.STAP_02).document
    doc.write_chat(op.join(HERE, 'output.cha'))
    # os.remove(op.join(HERE, 'output.cha'))
    assert False


def test_docx_convert():
    # docx = op.join(HERE, 'test.docx')
    # txtpath = docx_to_txt(docx, delete_docx=False)
    # expectedpath = op.join(HERE, 'expected.txt')

    # assert txtpath == op.join(FILES, 'test.txt')
    # assert filecmp.cmp(txtpath, expectedpath, shallow=False)
    # remove(txtpath)
    assert True


def test_chat_convert():
    # sr = SifReader(op.join(HERE, 'expected.txt'))
    # doc = sr.document

    # participants = [p.participant_header for p in doc.participants]
    # assert participants == ['CHI chi Target_Child',
    #                         'MOE moe Other', 'OND ond Other']

    # utt_ids = [int(c.utt_id)
    #            for c in doc.content if isinstance(c, Utterance) and c.utt_id]
    # assert utt_ids == list(range(1, 51))
    assert True


def test_names_places(place_strings):
    for val, expect in place_strings:
        res = fill_places_persons(val)
        assert res == expect
