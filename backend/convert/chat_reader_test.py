import os.path as op
from .chat_reader import ChatDocument


def test_chat_reader():
    here = op.dirname(op.abspath(__file__))
    fp = op.join(here, 'testfiles', 'minimal_example.cha')

    # r = ChatReader()
    # doc = r.read_file(fp)

    doc = ChatDocument.from_chatfile(fp)
    print(doc.__dict__)
    assert len(doc.lines) == 4
