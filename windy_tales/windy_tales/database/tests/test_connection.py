'''
Created on May 5, 2013

@author: tosako
'''
import unittest
from cloudy_tales.database.tests.UnitTestWithMongoDB import UnitTestWithMongoDB
from cloudy_tales.database.connectionManager import DbConnectionManager


class TestWindyConnection(UnitTestWithMongoDB):

    def setUp(self):
        self.__conn = DbConnectionManager()

    def tearDown(self):
        # Drop rows in collection
        self.__conn.get_client()['dummy_db']['testCollection'].remove()

    def test_get_db(self):
        db = self.__conn.get_db()
        self.assertEquals(db.name, 'dummy_db')

    def test_get_collection(self):
        col = self.__conn.get_collection('testCollection')
        self.assertEquals(col.name, 'testCollection')


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
