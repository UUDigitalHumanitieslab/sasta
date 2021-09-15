import os.path as op

from lxml import etree as ET

from .zc_embedding import get_zc_embeddings

HERE = op.dirname(op.abspath(__file__))
FILES = op.join(HERE, 'testfiles')


def test_zc_embed():
    tree = ET.parse(op.join(FILES, 'zc_embed_test.xml'))
    expected_embeddings = [1, 1, 1, 1, 1, 2, 2, 2, 2]
    word_indices = [str(x) for x in range(0, 9)]
    expected = dict(zip(word_indices, expected_embeddings))
    assert expected == get_zc_embeddings(tree)
