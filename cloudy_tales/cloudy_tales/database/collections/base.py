'''
Created on Apr 7, 2013

@author: dorisip
'''


class BaseCollection(object):
    '''
    Base database collection class
    '''

    def __init__(self, connectionManager, name):
        self.__connectionManager = connectionManager
        self.__collection_name = name

    def getName(self):
        return self.__collection_name

    def insert(self, *args, **kwargs):
        doc_id = self.__connectionManager.insert(self.__collection_name, *args, **kwargs)
        # TODO: error check?
        return {'_id': doc_id}

    def remove_by_id(self, doc_id, *args, **kwargs):
        return self.__connectionManager.remove(self.__collection_name, {'_id': doc_id}, *args, **kwargs)

    def remove(self, *args, **kwargs):
        return self.__connectionManager.remove(self.__collection_name, *args, **kwargs)

    def update_by_id(self, doc_id, doc, upsert=True, *args, **kwargs):
        result = self.__connectionManager.update(self.__collection_name, {'_id': doc_id}, {'$set': doc}, upsert=upsert, *args, **kwargs)
        if result and result['ok']:
            return {'_id': doc_id}
        else:
            return None

    def update(self, *args, **kwargs):
        return self.__connectionManager.update(self.__collection_name, *args, **kwargs)

    def find_by_id(self, doc_id, *args, **kwargs):
        return self.__connectionManager.find_one(self.__collection_name, {'_id': doc_id}, *args, **kwargs)

    def find(self, *args, **kwargs):
        return self.__connectionManager.find(self.__collection_name, *args, **kwargs)

    def find_one_by_id(self, doc_id, *args, **kwargs):
        return self.__connectionManager.find_one(self.__collection_name, {'_id': doc_id}, *args, **kwargs)

    def find_one(self, *args, **kwargs):
        return self.__connectionManager.find_one(self.__collection_name, *args, **kwargs)

    def save(self, *args, **kwargs):
        return {'_id': self.__connectionManager.save(self.__collection_name, *args, **kwargs)}
