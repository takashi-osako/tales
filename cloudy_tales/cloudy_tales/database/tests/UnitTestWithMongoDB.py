'''
Created on May 5, 2013

@author: tosako
'''
import unittest
from cloudy_tales.database.tests.unittest_db_helper import create_in_memory_db_client


class UnitTestWithMongoDB(unittest.TestCase):

    @staticmethod
    def setUpClass():
        create_in_memory_db_client()
