'''
Created on May 11, 2013

@author: tosako
'''
import unittest
from cloudy_tales.database.tests.UnitTestWithMongoDB import UnitTestWithMongoDB
from windy_tales.database.collections.supplier import Supplier
from cloudy_tales.database.connectionManager import DbConnectionManager


class Test(UnitTestWithMongoDB):

    def test_get_data_by_supplier_no(self):
        supplier_data = {'supplier_no': '0000000001', 'name': 'myname'}
        with DbConnectionManager() as connection:
            supplier = Supplier(connection)
            supplier.save({'Supplier': supplier_data})
            doc = supplier.find_by_keys({'supplier_no': '0000000001'})
        self.assertEquals(doc['name'], 'myname')

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
