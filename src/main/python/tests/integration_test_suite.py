# file national-voter-file/src/main/python/tests/test_NewYorkPrepare.py
"""
Base suite for integration tests
"""
import unittest
import os
import tempfile
import shutil
import csv

__modname__ = _mn_ = "integration_test_suite.py"
__author__ = "Kyle McChesney"
__credits__ = ["Kyle McChesney"]
__version__ = "0.1"
__maintainer__ = "Kyle McChesney"
__email__ = "kmcchesney@archerdx.com"
__status__ = "Development"

class BaseIntegrationTestSuite(unittest.TestCase):

    def setUp(self):
        self.main_func = None
        self.input_file = None
        self.output_file = None

    def testMain(self):
        """
        Run the main function set in setUp
        """
        self.main_func()