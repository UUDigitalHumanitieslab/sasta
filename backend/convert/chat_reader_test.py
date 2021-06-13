from .chat_reader import ChatDocument


def test_chat_reader(chafiles):
    for (input, _) in chafiles:
        doc = ChatDocument.from_chatfile(input)
        assert len(doc.lines)
