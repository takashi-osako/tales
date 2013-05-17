'''
Created on May 5, 2013

@author: tosako
'''
import unittest
from cloudy_tales.database.tests.UnitTestWithMongoDB import UnitTestWithMongoDB
from windy_tales.database.collections.header_file_parsed_template import HeaderfileParsedTemplate
import datetime
from cloudy_tales.database.connectionManager import DbConnectionManager


class TestHeaderFileParsedTemplate(UnitTestWithMongoDB):

    def testSave(self):
        data = {"address1": 10, "city": 5, "zip": 5}
        with DbConnectionManager() as connection:
            collection = HeaderfileParsedTemplate(connection)
            mydatetime = datetime.datetime.utcnow()
            doc_id = collection.save(data_name="myheadername", data=data, version="1", currentDatetime=mydatetime)
        self.assertIsNotNone(doc_id)

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
