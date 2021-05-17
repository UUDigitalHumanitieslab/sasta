import os.path as op
import os
from .chat_reader import ChatDocument
from .chat_writer import ChatWriter


def test_chat_writer():
    here = op.dirname(op.abspath(__file__))
    fp = op.join(here, 'testfiles', 'tt_example.cha')
    doc = ChatDocument.from_chatfile(fp)
    assert len(doc.lines) == 3

    out_fp = op.join(here, 'testfiles', 'tt_example_out.cha')

    with open(out_fp, 'w+') as target:
        writer = ChatWriter(doc, target=target)
        writer.write()

    out_doc = ChatDocument.from_chatfile(out_fp)
    assert out_doc == doc
    os.remove(out_fp)
