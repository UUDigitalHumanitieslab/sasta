import os.path as op

from parse.parse_utils import corpus2alpino_parse
from lxml import etree
import pytest


@pytest.mark.skip(reason="need to figure out c2a uttids")
def test_c2a_parse(testfiles_dir, tmp_path):
    infile = op.join(testfiles_dir, 'ASTA', 'single_utt', 'single_utt.cha')
    outfile = op.join(tmp_path, 'single_utt.xml')
    parses = corpus2alpino_parse(infile, outfile, in_memory=True)
    parsed = next(parses)
    assert parsed  # is the file parsed?

    parsed_tree = etree.fromstring(bytes(parsed, encoding='utf-8'))
    assert parsed_tree  # can it be converted to an etree?

    uttids = parsed_tree.findall('.//meta[@name="uttid"]')
    uttid_values = [node.attrib['value'] for node in uttids]
    assert len(set(uttid_values)) == len(
        uttid_values)  # does it have unique uttids?
