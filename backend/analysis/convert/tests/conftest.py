import pytest
import os.path as op
from types import SimpleNamespace


@pytest.fixture
def place_strings():
    return [
        ('Ik heet NAAM.', 'Ik heet Maria.'),
        ('Ik heet NAAM1.', 'Ik heet Jan.'),
        ('Ik heet VOORNAAM.', 'Ik heet Maria.'),
        ('Ik heet NAAMOVERIG1.', 'Ik heet Jan.'),
        ('Ik heet VOORNAAM1.', 'Ik heet Jan.'),
        ('Ik heet ACHTERNAAM1.', 'Ik heet Jan.'),
        ('Ik heet TWEELINGZUS.', 'Ik heet Maria.')
    ]


@pytest.fixture
def testfiles():
    here = op.dirname(op.abspath(__file__))
    files = ['basic', 'STAP_02']
    files = {fn: op.join(here, f'{fn}.txt') for fn in files}
    yield SimpleNamespace(**files)
