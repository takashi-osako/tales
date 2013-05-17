'''
Created on May 11, 2013

@author: tosako
'''
from windy_tales.database.collections.supplier import Supplier
from windy_tales.database.collections.customer import Customer
from windy_tales.database.collections.account import Account
from windy_tales.database.collections.terminal import Terminal
from cloudy_tales.database.connectionManager import DbConnectionManager


def aggregate_for_transaction(data):
    '''
    aggregate transaction data with
    supplier
    '''
    with DbConnectionManager() as connection:
        # find supplier and aggrigate the data
        # refactor: make it database driven
        transheader = data['Transheader']
        supplier = Supplier(connection)
        supplier_keys = supplier.get_keys()
        key_data = {}
        for supplier_key in supplier_keys:
            key_data[supplier_key] = transheader.get(supplier_key)
        supplier_data = supplier.find_by_keys(key_data)
        transheader[supplier.getName()] = supplier_data

        customer = Customer(connection)
        customer_keys = customer.get_keys()
        key_data = {}
        for customer_key in customer_keys:
            key_data[customer_key] = transheader.get(customer_key)
        customer_data = customer.find_by_keys(key_data)
        transheader[customer.getName()] = customer_data

        account = Account(connection)
        account_keys = account.get_keys()
        key_data = {}
        for account_key in account_keys:
            key_data[account_key] = transheader.get(account_key)
        account_data = account.find_by_keys(key_data)
        transheader[account.getName()] = account_data

        terminal = Terminal(connection)
        terminal_keys = terminal.get_keys()
        key_data = {}
        for terminal_key in terminal_keys:
            key_data[terminal_key] = transheader.get(terminal_key)
        terminal_data = terminal.find_by_keys(key_data)
        transheader[terminal.getName()] = terminal_data
    return data
