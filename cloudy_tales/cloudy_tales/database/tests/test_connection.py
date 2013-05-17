'''
Created on Apr 7, 2013

@author: dorisip
'''
import unittest
from cloudy_tales.database.tests.UnitTestWithMongoDB import UnitTestWithMongoDB
from cloudy_tales.database.collections.base import BaseCollection
from cloudy_tales.database.connectionManager import DbConnectionManager


class TestConnection(UnitTestWithMongoDB):

    def setUp(self):
        self.__connection = DbConnectionManager()
        self.__collection = BaseCollection(self.__connection, 'testCollection')

    def tearDown(self):
        # Drop rows in collection
        self.__connection.get_client()['dummy_db']['testCollection'].remove()

    def test_get_client(self):
        client = self.__connection.get_client()
        self.assertIsNotNone(client)

    def test_get_db(self):
        db = self.__connection.get_db()
        self.assertEquals(db.name, 'dummy_db')

    def test_get_collection(self):
        col = self.__connection.get_collection('testCollection')
        self.assertEquals(col.name, 'testCollection')

    def test_insert(self):
        result = self.__collection.insert({'_id': 123})
        self.assertEquals(result['_id'], 123)
        self.assertEquals(len(self.__collection.find()), 1)

    def test_find_doc_not_exists(self):
        result = self.__collection.find({'not': 'exist'})
        self.assertEquals(result, [])

    def test_find_doc_exists(self):
        doc = {'_id': 1, 'value': 1}
        self.__collection.insert(doc)
        self.__collection.insert({'_id': 2, 'value': 1})
        self.__collection.insert({'_id': 3, 'value': 1})
        result = self.__collection.find({'_id': doc['_id']})
        self.assertIn(doc, result)
        self.assertEquals(len(result), 1)

        result = self.__collection.find({'value': 1})
        self.assertEquals(len(result), 3)

    def test_find_with_no_criteria(self):
        self.__collection.insert({'_id': 2, 'value': 1})
        self.__collection.insert({'_id': 3, 'value': 1})

        result = self.__collection.find()
        self.assertEquals(len(result), 2)

    def test_find_one(self):
        doc = {'_id': 1, 'value': 1}
        self.__collection.insert(doc)
        result = self.__collection.find_one()
        self.assertEquals(doc, result)

    def test_find_one_with_criteria(self):
        doc = {'_id': 1, 'value': 1}
        other_doc = {'_id': 2}
        self.__collection.insert(doc)
        self.__collection.insert(other_doc)

        result = self.__collection.find_one({'_id': 2})
        self.assertEquals(other_doc, result)

        result = self.__collection.find_one({'_id': 1})
        self.assertEquals(doc, result)

    def test_find_one_with_no_results(self):
        result = self.__collection.find_one({'_id': 2})
        self.assertIsNone(result)

    def test_remove(self):
        self.__collection.insert({'_id': 1, 'value': 234})
        self.__collection.remove({'_id': 1})
        result = self.__collection.find_one()
        self.assertIsNone(result)

    def test_remove_all(self):
        self.__collection.insert({'_id': 1, 'value': 234})
        self.__collection.insert({'_id': 2, 'value': 2})
        self.__collection.remove()
        result = self.__collection.find_one()
        self.assertIsNone(result)

    def test_update(self):
        self.__collection.insert({'_id': 1, 'value': 234})
        self.__collection.update({'_id': 1}, {'$set': {'value': 1}})

        result = self.__collection.find_one()
        self.assertEquals(result['value'], 1)

    def test_update_with_upsert(self):
        self.__collection.update({'_id': 1}, {'$set': {'value': 1}}, upsert=True)
        result = self.__collection.find_one()
        self.assertEquals(result['value'], 1)

    def test_save(self):
        self.__collection.save({'_id': 1, 'key': 'value'})
        result = self.__collection.find_one()
        self.assertEquals(result['key'], 'value')


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
