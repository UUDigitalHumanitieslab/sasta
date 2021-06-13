from .chat_reader import ChatDocument
from .chat_writer import ChatWriter


def test_chat_writer(chafiles):
    for inpath, outpath in chafiles:
        doc = ChatDocument.from_chatfile(inpath)
        with open(outpath, 'w+', encoding='utf-8') as target:
            writer = ChatWriter(doc, target=target)
            writer.write()
        out_doc = ChatDocument.from_chatfile(outpath)
        assert out_doc == doc
