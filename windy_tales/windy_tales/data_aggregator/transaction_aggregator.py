'''
Created on May 11, 2013

@author: tosako
'''
from cloudy_tales.database.collections.base import BaseCollection
from cloudy_tales.database.connectionManager import DbConnectionManager


def aggregate_for_transaction(data):
    '''
    aggregate transaction data with
    supplier
    '''
    with DbConnectionManager() as connector:
        collection = BaseCollection(connectionManager=connector, name="association")
        document = {"name": "Transheader"}
        transheader = collection.find_one(document)
        tables = transheader.get('tables')
        for table_name in tables.keys():
            # aggrigating table
            table = tables[table_name]
            aggrigating_document = {}
            for key in table.keys():
                aggrigating_document['fields.' + table[key]] = data.get(key)
            if aggrigating_document:
                with DbConnectionManager() as connector1:
                    aggrigating_collection = BaseCollection(connectionManager=connector1, name=table_name)
                    result = aggrigating_collection.find_one(aggrigating_document)
                    data[table_name] = result['fields']
            
    return data
