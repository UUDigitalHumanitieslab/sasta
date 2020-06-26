import pytest


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
