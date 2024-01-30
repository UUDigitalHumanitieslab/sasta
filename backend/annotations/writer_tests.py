from annotations.constants import (SAF_COMMENT_COLUMN, SAF_FASES_COLUMN,
                                   SAF_UNALIGNED_LEVEL)
from annotations.writer import SAFWriter

from .utils import ljust


def test_safwriter(safwriter: SAFWriter):
    safwriter.make_workbook()
    safwriter.write('/Users/a3248526/Documents/saf_writer_test.xlsx')
    assert safwriter


def test_headers(safwriter: SAFWriter):
    found = safwriter._annotations_header_row()
    expected = ['ID', 'Level', SAF_UNALIGNED_LEVEL,
                'Word1', 'Word2', 'Word3', 'Word4',
                'Word5', 'Word6', 'Word7', 'Word8',
                'Word9', 'Word10', 'Word11', 'Word12',
                'Word13', 'Word14', 'Word15', 'Word16',
                'Word17', 'Word18',
                SAF_FASES_COLUMN, SAF_COMMENT_COLUMN]
    assert found == expected


def test_uttlevel_row(safwriter: SAFWriter):
    id = 1
    words = safwriter.results.allutts[id]
    found = safwriter._uttlevel_row(id, words)
    expected = [1, 'Uiting', None, 'ja', 'uh', 'ik', 'vind', 'het', 'beetje',
                'moeilijk', 'om', 'het', 'goed', 'te', 'vertellen', 'want',
                'ik', 'heb', 'een', 'ongeluk', 'gehad', None, None]
    assert found == expected


def test_ljust_list():
    input = ['a', 'b', 'c']
    ljustified = ljust(input, 5)
    assert ljustified == input + [None, None]
    ljustified = ljust(input, 3)
    assert ljustified == input
    ljustified = ljust(input, 2)
    assert ljustified == input


def test_uttlevel_offset(safwriter: SAFWriter):
    assert safwriter._uttlevel_row_number(0, 'Samplegrootte') == 3
    assert safwriter._uttlevel_row_number(0, 'Taalmaat') == 5
    assert safwriter._uttlevel_row_number(0, 'Opmerkingen') == 8
    assert safwriter._uttlevel_row_number(2, 'Samplegrootte') == 17
    assert safwriter._uttlevel_row_number(2, 'Taalmaat') == 19
    assert safwriter._uttlevel_row_number(2, 'Opmerkingen') == 22
