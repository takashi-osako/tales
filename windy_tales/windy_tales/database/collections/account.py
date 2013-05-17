'''
Created on May 11, 2013

@author: tosako
'''
from windy_tales.database.collections.generic_collection import GenericCollection


class Account(GenericCollection):
    def __init__(self, connection):
        super(Account, self).__init__(connection=connection, name='Account')

    def get_keys(self):
        '''
        return fieldname that uses for the key
        '''
        return ['supplier_no', 'customer_no', 'account_no']
