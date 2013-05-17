'''
Created on Apr 5, 2013

@author: dorisip
'''
from pymongo.mongo_client import MongoClient
from zope import interface, component


def create_db_client(url='mongodb://localhost:27017', db_name=None):
    '''
    Register mongoClient in zope
    '''
    connector = DbClient(url=url, db_name=db_name)
    component.provideUtility(connector, IDbClient)


class IDbClient(interface.Interface):
    pass


class DbClient:
    interface.implements(IDbClient)

    def __init__(self, url, db_name, max_pool_size=10):
        self.__db_name = db_name
        self.__client = MongoClient(url, max_pool_size=max_pool_size)

    def get_client(self):
        return self.__client

    def get_db_name(self):
        return self.__db_name
