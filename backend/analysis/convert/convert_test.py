import filecmp
import os.path as op
from os import remove

from ..utils import docx_to_txt
from .chat_converter import SifReader, Utterance

HERE = op.dirname(op.abspath(__file__))
FILES = op.join(HERE, 'testfiles')


def test_docx_convert():
    docx = op.join(FILES, 'test.docx')
    txtpath = docx_to_txt(docx, delete_docx=False)
    expectedpath = op.join(FILES, 'expected.txt')

    assert txtpath == op.join(FILES, 'test.txt')
    assert filecmp.cmp(txtpath, expectedpath, shallow=False)
    remove(txtpath)


def test_chat_convert():
    sr = SifReader(op.join(FILES, 'expected.txt'))
    doc = sr.document

    participants = [p.participant_header for p in doc.participants]
    assert participants == ['CHI chi Target_Child',
                            'MOE moe Other', 'OND ond Other']

    utt_ids = [int(c.utt_id)
               for c in doc.content if isinstance(c, Utterance) and c.utt_id]
    assert utt_ids == list(range(1, 51))
