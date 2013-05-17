'''
Created on Apr 7, 2013

@author: dorisip
'''
from zope import component
from cloudy_tales.database.client import IDbClient
from pymongo.mongo_client import MongoClient


class DbConnectionManager(object):

    def __init__(self):
        self.__client = component.queryUtility(IDbClient).get_client()
        self.__db_name = component.queryUtility(IDbClient).get_db_name()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        # In memory mongo connection doesn't support close()
        if isinstance(self.__client, MongoClient):
            self.__client.close()

    def get_client(self):
        return self.__client

    def get_db(self):
        return self.get_client()[self.__db_name]

    def get_collection(self, collection_name):
        return self.get_db()[collection_name]

    def insert(self, collection_name, *args, **kwargs):
        '''
        Given a collection name, and a python dictionary, insert it
        '''
        _id = self.get_collection(collection_name).insert(*args, **kwargs)
        return _id

    def find(self, collection_name, *args, **kwargs):
        '''
        Find based on _id
        Returns a list of json objects
        '''
        results = self.get_collection(collection_name).find(*args, **kwargs)
        return list(results)

    def find_one(self, collection_name, *args, **kwargs):
        '''
        Find_one in collection
        '''
        result = self.get_collection(collection_name).find_one(*args, **kwargs)
        return result

    def remove(self, collection_name, *args, **kwargs):
        '''
        Remove document from mongo
        '''
        return self.get_collection(collection_name).remove(*args, **kwargs)

    def update(self, collection_name, *args, **kwargs):
        '''
        Update a document with doc
        '''
        return self.get_collection(collection_name).update(*args, **kwargs)

    def save(self, collection_name, *args, **kwargs):
        '''
        Saves a document (update and/or inserts)
        '''
        return self.get_collection(collection_name).save(*args, **kwargs)
