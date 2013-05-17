'''
Created on Apr 9, 2013

@author: dorisip
'''
import unittest
from cloudy_tales.database.collections.base import BaseCollection
from zope import component
from cloudy_tales.database.client import IDbClient
from cloudy_tales.database.tests.UnitTestWithMongoDB import UnitTestWithMongoDB
from cloudy_tales.database.connectionManager import DbConnectionManager


class TestBaseCollection(UnitTestWithMongoDB):

    def setUp(self):
        connection = DbConnectionManager()
        self.__col = BaseCollection(connection, 'dummy')
        # This is the direct in memory db connection, so we can execute mongo commands directly
        # without going through our own code to isolate testing
        self.__direct_conn = component.queryUtility(IDbClient).get_client()['dummy_db']['dummy']

    def tearDown(self):
        # Drop rows in collection
        self.__col.remove()

    def test_insert(self):
        result = self.__col.insert({'_id': '123', 'value': '1'})
        self.assertEquals(result, {'_id': '123'})

    def test_remove_by_id_with_invalid_id(self):
        results = self.__col.remove_by_id('123')
        self.assertIsNone(results, None)

    def test_remove_by_id(self):
        self.__direct_conn.insert({'_id': '123', 'value': '1'})
        results = self.__direct_conn.find_one()
        self.assertIsNotNone(results)
        self.__col.remove_by_id('123')
        results = self.__direct_conn.find_one()
        self.assertIsNone(results)

    def test_remove(self):
        self.__direct_conn.insert({'_id': '123', 'value': '1'})
        self.__direct_conn.insert({'_id': '234', 'value': '1'})
        self.assertEquals(len(list(self.__direct_conn.find())), 2)
        self.__col.remove()
        self.assertEquals(len(list(self.__direct_conn.find())), 0)

    def test_remove_with_criteria(self):
        self.__direct_conn.insert({'_id': '123', 'value': '2'})
        self.__direct_conn.insert({'_id': '234', 'value': '1'})
        self.__col.remove({'value': '1'})
        results = self.__direct_conn.find()
        self.assertEquals(len(list(results)), 1)
        self.assertEquals(results[0]['_id'], '123')

    def test_update_by_id(self):
        self.__direct_conn.insert({'_id': '123', 'value': '2'})
        self.__col.update_by_id('123', {'value': '3'})
        doc = self.__direct_conn.find_one({'_id': '123'})
        self.assertEquals(doc['value'], '3')

    def test_update(self):
        self.__direct_conn.insert({'_id': '123', 'value': '2'})
        self.__col.update({'value': '2'}, {'$set': {'new': 'stuff'}})
        doc = self.__direct_conn.find_one({'_id': '123'})
        self.assertEquals(doc['new'], 'stuff')

    def test_find_by_id(self):
        self.__direct_conn.insert({'_id': '123', 'value': '2'})
        doc = self.__col.find_by_id('123')
        self.assertEquals(doc['value'], '2')

    def test_find_by_invalid_id(self):
        doc = self.__col.find_by_id('123')
        self.assertIsNone(doc)

    def test_find(self):
        self.__direct_conn.insert({'_id': '123', 'value': '2'})
        self.__direct_conn.insert({'_id': '234', 'value': '3'})
        doc = self.__col.find({'value': '2'})
        self.assertEquals(doc[0]['_id'], '123')

    def test_find_invalid_criteria(self):
        self.__direct_conn.insert({'_id': '123', 'value': '2'})
        self.__direct_conn.insert({'_id': '234', 'value': '3'})
        doc = self.__col.find({'value': '2234'})
        self.assertEquals(len(doc), 0)

    def test_find_one_by_id(self):
        self.__direct_conn.insert({'_id': '123', 'value': '2'})
        self.__direct_conn.insert({'_id': '234', 'value': '3'})
        doc = self.__col.find_one_by_id('123')
        self.assertEquals(doc['value'], '2')

    def test_find_one_by_invalid_id(self):
        self.__direct_conn.insert({'_id': '123', 'value': '2'})
        self.__direct_conn.insert({'_id': '234', 'value': '3'})
        doc = self.__col.find_one_by_id('00')
        self.assertIsNone(doc)

    def test_find_one(self):
        self.__direct_conn.insert({'_id': '123', 'value': '2'})
        self.__direct_conn.insert({'_id': '234', 'value': '3'})
        doc = self.__col.find_one({'value': '3'})
        self.assertEquals(doc['_id'], '234')

    def test_find_one_invalid_criteria(self):
        self.__direct_conn.insert({'_id': '123', 'value': '2'})
        self.__direct_conn.insert({'_id': '234', 'value': '3'})
        doc = self.__col.find_one({'value': '3234'})
        self.assertIsNone(doc)

    def test_save(self):
        doc = self.__col.save({'_id': 1, 'key': 'value'})
        self.assertEquals(doc['_id'], 1)

    def test_save_with_no_id(self):
        doc = self.__col.save({'key': 'value'})
        self.assertIsNotNone(doc.get('_id'))

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
