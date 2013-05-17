'''
Created on Apr 8, 2013

@author: dorisip
'''
from zope import component, interface
from cloudy_tales.database.client import IDbClient
from ming import mim


def create_in_memory_db_client():
    '''
    Register mongoClient in zope for in memory mongo connection used in unit tests
    '''
    connector = MIMClient()
    component.provideUtility(connector, IDbClient)


class MIMClient:
    interface.implements(IDbClient)
    '''
    In memory mongo connection
    '''

    def __init__(self):
        self.__client = mim.Connection()

    def get_client(self):
        return self.__client

    def get_db_name(self):
        return 'dummy_db'
