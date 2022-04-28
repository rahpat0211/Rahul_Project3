import logging
import os

from click.testing import CliRunner

from app import create_database

runner = CliRunner()




def test_create_database():
    response = runner.invoke(create_database)
    assert response.exit_code == 0
    root = os.path.dirname(os.path.abspath(__file__))
    # set the name of the apps log folder to logs
    dbdir = os.path.join(root, '../database')
    # make a directory if it doesn't exist
    assert os.path.exists(dbdir) == True

#Test to check if user uploaded music.csv

import pytest
import unittest

class CSV_Test(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def initdir(self, tmpdir):
        tmpdir.chdir()
        tmpdir.join("music.csv").write("# testdata")

    def test_method(self):
        with open("music.csv") as f:
            s = f.read()
        assert "testdata" in s