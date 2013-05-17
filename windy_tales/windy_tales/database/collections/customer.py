'''
Created on May 11, 2013

@author: tosako
'''
from windy_tales.database.collections.generic_collection import GenericCollection


class Customer(GenericCollection):
    def __init__(self, connection):
        super(Customer, self).__init__(connection=connection, name='Customer')

    def get_keys(self):
        '''
        return fieldname that uses for the key of Supplier
        '''
        return ['supplier_no', 'customer_no']
