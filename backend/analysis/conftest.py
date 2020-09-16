import pytest


@pytest.fixture(scope="session")
def django_db_setup():
    # settings.DATABASES["default"] = settings.DATABASES["default"]
    pass
