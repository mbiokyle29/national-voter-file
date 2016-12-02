# file national-voter-file/src/main/python/tests/test_integrations.py
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

import NewYorkPrepare as nyp
from tests.base_integration_suite import BaseIntegrationSuite

__modname__ = _mn_ = "test_integrations.py"
__author__ = "Kyle McChesney"
__credits__ = ["Kyle McChesney"]
__version__ = "0.1"
__maintainer__ = "Kyle McChesney"
__email__ = "kmcchesney@archerdx.com"
__status__ = "Development"


class TestNewYorkIntegrationSuite(BaseIntegrationSuite):

    def setUp(self):
        """
        This setUp function should basically accomplish everything 
        required to make the testMain function of BaseIntegrationSuite
        work well.

        - set self.main_func to the main() function of the prepare script to test
        - set self.input_file to the data file to be passed to main
        - set up temp files to write the output from
        - populate self.validation_functions with a set of functions that take the output file
          as input, and validate things about the output data.
        """
        self.main_func = nyp.main
        self.input_file = os.path.join(os.path.dirname(__file__), "integration_cases/new_york_integration.csv")
        
        self.temp_dir = tempfile.mkdtemp()
        self.output_file = os.path.join(temp_dir, "temp.out")
        self.err_file = os.path.join(temp_dir, "err.out")
        self.validation_functions = [self.validationExample]

    def tearDown(self):
        """
        Clean up the temp dir
        """
        shutil.rmtree(self.temp_dir)

    def validationExample(self, output_file):
        """
        Validate the output file in some way
        """
        pass
