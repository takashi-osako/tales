'''
Created on May 11, 2013

@author: tosako
'''
import unittest
from cloudy_tales.database.tests.UnitTestWithMongoDB import UnitTestWithMongoDB
from cloudy_tales.database.connectionManager import DbConnectionManager
from cloudy_tales.database.collections.base import BaseCollection
from cloudy_tales.data_aggregator.transaction_aggregator import aggregate_for_transaction


class TestAggregateForTransaction(UnitTestWithMongoDB):

    def test_find_supplier_from_transaction(self):
        transaction = {}
        transaction['trans_ref_no'] = '0000000001'
        transaction['supplier_no'] = '0000000001'
        transaction['customer_no'] = '0000000001'
        transaction['account_no'] = '0000000001'
        transaction['term_id'] = '0000001'

        with DbConnectionManager() as connection:
            supplier = BaseCollection(connectionManager=connection, name='Supplier')
            supplier_data = {}
            supplier_data['supplier_no'] = '0000000001'
            supplier_data['name'] = 'name1'
            supplier.save({'fields': supplier_data})
            supplier_data = {}
            supplier_data['supplier_no'] = '0000000002'
            supplier_data['name'] = 'name2'
            supplier.save({'fields': supplier_data})

            customer = BaseCollection(connectionManager=connection, name='Customer')
            customer_data = {}
            customer_data['customer_no'] = '0000000001'
            customer_data['supplier_no'] = '0000000001'
            customer_data['customer_name'] = 'name'
            customer_data['name1'] = 'name1'
            customer_data['name2'] = 'name2'
            customer_data['address1'] = 'address1'
            customer_data['address2'] = 'address2'
            customer_data['city'] = 'city'
            customer_data['state'] = 'NY'
            customer_data['zip'] = '90210'
            customer_data['country'] = 'US'
            customer.save({'fields': customer_data})

            account = BaseCollection(connectionManager=connection, name='Account')
            account_data = {}
            account_data['supplier_no'] = '0000000001'
            account_data['customer_no'] = '0000000001'
            account_data['account_no'] = '0000000001'
            account_data['account_name'] = 'name'
            account_data['name1'] = 'name1'
            account_data['name2'] = 'name2'
            account_data['address1'] = 'address1'
            account_data['address2'] = 'address2'
            account_data['city'] = 'city'
            account_data['state'] = 'ny'
            account_data['country'] = 'US'
            account_data['zip'] = '12345'
            account.save({'fields': account_data})

            terminal = BaseCollection(connectionManager=connection, name='Terminal')
            terminal_data = {}
            terminal_data['term_id'] = '0000001'
            terminal_data['name'] = 'name'
            terminal_data['addr1'] = 'address'
            terminal_data['city'] = 'city'
            terminal_data['state'] = 'NY'
            terminal_data['zip'] = '99999'
            terminal.save({'fields': terminal_data})

            association = BaseCollection(connectionManager=connection, name='association')
            association_data = {'name': 'Transheader',
                                "tables": {
                                        'Supplier': {'supplier_no': 'supplier_no'},
                                        'Customer': {'supplier_no': 'supplier_no', 'customer_no': 'customer_no'},
                                        'Account': {'supplier_no': 'supplier_no', 'customer_no': 'customer_no', 'account_no': 'account_no'},
                                        'Terminal': {'term_id': 'term_id'}}
                                }
            association.save(association_data)

        data = aggregate_for_transaction(transaction)
        self.assertEqual('name1', data['Supplier']['name'])
        self.assertEquals('90210', data['Customer']['zip'])
        self.assertEquals('ny', data['Account']['state'])
        self.assertEquals('99999', data['Terminal']['zip'])


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
