import os.path as op
from chamd import ChatReader


def test_chat_reader():
    here = op.dirname(op.abspath(__file__))
    fp = op.join(here, 'testfiles', 'minimal_example.cha')

    r = ChatReader()
    doc = r.read_file(fp)

    assert not r.errors
    assert len(doc.lines) == 4
