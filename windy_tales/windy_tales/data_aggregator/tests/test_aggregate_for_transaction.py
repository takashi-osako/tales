'''
Created on May 11, 2013

@author: tosako
'''
import unittest
from cloudy_tales.database.tests.UnitTestWithMongoDB import UnitTestWithMongoDB
from windy_tales.database.collections.supplier import Supplier
from windy_tales.data_aggregator.transaction_aggregator import aggregate_for_transaction
from windy_tales.database.collections.customer import Customer
from windy_tales.database.collections.account import Account
from windy_tales.database.collections.terminal import Terminal
from cloudy_tales.database.connectionManager import DbConnectionManager


class TestAggregateForTransaction(UnitTestWithMongoDB):

    def test_find_supplier_from_transaction(self):
        transaction = {}
        transaction['trans_ref_no'] = '0000000001'
        transaction['supplier_no'] = '0000000001'
        transaction['customer_no'] = '0000000001'
        transaction['account_no'] = '0000000001'
        transaction['term_id'] = '0000001'

        with DbConnectionManager() as connection:
            supplier = Supplier(connection)
            supplier_data = {}
            supplier_data['supplier_no'] = '0000000001'
            supplier_data['name'] = 'name1'
            supplier.save({'Supplier': supplier_data})
            supplier_data = {}
            supplier_data['supplier_no'] = '0000000002'
            supplier_data['name'] = 'name2'
            supplier.save({'Supplier': supplier_data})

            customer = Customer(connection)
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
            customer.save({'Customer': customer_data})

            account = Account(connection)
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
            account.save({'Account': account_data})

            terminal = Terminal(connection)
            terminal_data = {}
            terminal_data['term_id'] = '0000001'
            terminal_data['name'] = 'name'
            terminal_data['addr1'] = 'address'
            terminal_data['city'] = 'city'
            terminal_data['state'] = 'NY'
            terminal_data['zip'] = '99999'
            terminal.save({'Terminal': terminal_data})

        data = aggregate_for_transaction({'Transheader': transaction})
        self.assertEqual('name1', data['Transheader']['Supplier']['name'])
        self.assertEquals('90210', data['Transheader']['Customer']['zip'])
        self.assertEquals('ny', data['Transheader']['Account']['state'])
        self.assertEquals('99999', data['Transheader']['Terminal']['zip'])


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
