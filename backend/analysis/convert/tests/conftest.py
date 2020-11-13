import pytest
import os.path as op


@pytest.fixture
def place_strings():
    return [
        ('Ik heet NAAM.', 'Ik heet Maria.'),
        ('Ik heet NAAMKIND.', 'Ik heet Maria.'),
        ('Ik heet NAAM1.', 'Ik heet Jan.'),
        ('Ik heet VOORNAAM.', 'Ik heet Maria.'),
        ('Ik heet NAAMOVERIG1.', 'Ik heet Jan.'),
        ('Ik heet VOORNAAM1.', 'Ik heet Jan.'),
        ('Ik heet ACHTERNAAM1.', 'Ik heet Jan.'),
        ('Ik heet TWEELINGZUS.', 'Ik heet Maria.'),
        ('15 | PMA: in het uh hier in het PLAATSNAAM1 uh silahe ',
         '15 | PMA: in het uh hier in het Breda uh silahe '),
        ('15 | PMA: in het uh hier in het PLAATSNAAM uh silahe ',
         '15 | PMA: in het uh hier in het Utrecht uh silahe ')
    ]


@pytest.fixture
def testfiles():
    here = op.dirname(op.abspath(__file__))
    fns = ['STAP_02', 'ASTA_01']
    return {fn: op.join(here, f'{fn}.docx') for fn in fns}
