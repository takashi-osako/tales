'''
Created on May 5, 2013

@author: dorisip
'''
import unittest
from windy_tales.utils.utils import read_file
import os


class TestUtils(unittest.TestCase):

    def test_read_file_with_invalid_path(self):
        file_name = "/tmp/non-existing.file"
        self.assertRaises(IOError, read_file, file_name)

    def test_read_file_with_valid_path(self):
        here = os.path.abspath(os.path.dirname(__file__))
        file_name = os.path.join(here, '..', 'resources', 'sample.h')
        content = read_file(file_name)
        self.assertTrue(len(content) > 0)


if __name__ == "__main__":
    unittest.main()
