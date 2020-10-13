import os.path as op
from filecmp import cmp
from os import remove as rm

from analysis.utils import docx_to_txt
from analysis.convert.chat_converter import SifReader, fill_places_persons

HERE = op.dirname(op.abspath(__file__))


def test_docx_to_txt(testfiles):
    for fn, docx in testfiles.items():
        txt = docx_to_txt(docx, delete_docx=False)
        txt_exp = txt.replace(fn, f'{fn}_exp')
        assert cmp(txt, txt_exp, shallow=False)

        doc = SifReader(txt).document
        cha = op.join(HERE, f'{fn}.cha')
        doc.write_chat(cha)
        cha_exp = cha.replace(fn, f'{fn}_exp')
        assert cmp(cha, cha_exp, shallow=False)

        if op.exists(txt):
            rm(txt)
        if op.exists(cha):
            rm(cha)


def test_names_places(place_strings):
    for val, expect in place_strings:
        res = fill_places_persons(val)
        assert res == expect
