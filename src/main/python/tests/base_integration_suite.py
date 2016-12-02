# file national-voter-file/src/main/python/tests/base_integration_suite.py
"""
Base suite for integration tests
"""
import argparse
import csv
import os
import shutil
import tempfile
import unittest
from unittest.mock import patch


class BaseIntegrationSuite(unittest.TestCase):

    def setUp(self):
        self.main_func = self.main

        self.temp_dir = None
        self.input_file = None
        self.output_file = None
        self.err_file = None
        self.validation_functions = []

    def main(self):
        pass

    def testMain(self):
        """
        Run the main function set in setUp
        """
        with patch('argparse.ArgumentParser.parse_args',
                   return_value=argparse.Namespace(input_file=self.input_file,
                                                   output_file=self.output_file,
                                                   err_file=self.err_file)):
            self.main_func()
            for validation_function in self.validation_functions:
                validation_function(self.output_file)
