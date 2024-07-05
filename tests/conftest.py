import pytest
from sqlite_utils.db import Database
from click.testing import CliRunner


@pytest.fixture
def mock_db() -> Database:
    db = Database(memory=True)
    return db


@pytest.fixture
def cli_runner():
    return CliRunner()
