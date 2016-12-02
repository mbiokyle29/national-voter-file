# file national-voter-file/src/main/python/tests/test_NewYorkPrepare.py
"""
Tests for NewYorkPrepare script
"""

import unittest
import os
import tempfile
import shutil
import csv

import NewYorkPrepare as nyp
from settings import NY_INPUT_FIELD_NAMES

__modname__ = _mn_ = "test_NewYorkPrepare.py"
__author__ = "Kyle McChesney"
__credits__ = ["Kyle McChesney"]
__version__ = "0.1"
__maintainer__ = "Kyle McChesney"
__email__ = "kmcchesney@archerdx.com"
__status__ = "Development"


class NewYorkPrepareUnitTestSuite(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        Point to the test case file.
        """
        curr_dir = os.path.abspath(os.path.dirname(__file__))
        cls.test_file = os.path.join(curr_dir, "unittest_cases/new_york_data.csv")

    def setUp(self):
        """
        Make a tmp dir for output for each test case
        """
        self.output_dir = tempfile.mkdtemp()

    def tearDown(self):
        """
        Remove the temp dir
        """
        shutil.rmtree(self.output_dir)

    def makeRowGenerator(self):
        """
        Make a row reader over the test data
        """
        with open(self.test_file, encoding='latin-1') as csvfile:
            reader = csv.DictReader(csvfile, dialect='excel', fieldnames=NY_INPUT_FIELD_NAMES)
            for row in reader:
                yield row

    def testPrepareDate(self):
        """ test the prepareDate function """
        fields_with_date = ["DOB", "REGDATE"]
        for row in self.makeRowGenerator():

            for date_field in fields_with_date:
                raw_date = row[date_field]
                result = nyp.prepareDate(raw_date)
                result_deformatted = result.replace("-", "")
                self.assertEqual(raw_date, result_deformatted)

    def testAppendMailingAddress(self):
        """ test the appendMailingAddress function """
        pass

    def testAppendJurisdiction(self):
        """ test the appendJurisdiction function """
        pass

    def testConstructResidenceAddress(self):
        """ test the constructResidenceAddress function """
        pass

    def testConstructVoterRegOutrow(self):
        """ test the constructVoterRegOutrow function """
        pass

