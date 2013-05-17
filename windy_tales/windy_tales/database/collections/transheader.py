'''
Created on May 11, 2013

@author: tosako
'''
from windy_tales.database.collections.generic_collection import GenericCollection


class Transheader(GenericCollection):
    def __init__(self, connection):
        super(Transheader, self).__init__(connection=connection, name='Transheader')

    def get_keys(self):
        '''
        return fieldname that uses for the key
        '''
        return ['trans_ref_no']
