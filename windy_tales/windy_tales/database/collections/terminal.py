'''
Created on May 11, 2013

@author: tosako
'''
from windy_tales.database.collections.generic_collection import GenericCollection


class Terminal(GenericCollection):
    def __init__(self, connection):
        super(Terminal, self).__init__(connection=connection, name='Terminal')

    def get_keys(self):
        '''
        return fieldname that uses for the key
        '''
        return ['term_id']
