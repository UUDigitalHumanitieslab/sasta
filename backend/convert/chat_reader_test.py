import os.path as op
from .chat_reader import ChatDocument


def test_chat_reader():
    here = op.dirname(op.abspath(__file__))
    fp = op.join(here, 'testfiles', 'tt_example.cha')
    doc = ChatDocument.from_chatfile(fp)
    assert len(doc.lines) == 3
