'''
Created on Apr 7, 2013

@author: dorisip
'''
from cloudy_tales.database.collections.base import BaseCollection
import datetime
from uuid import uuid4
from windy_tales.exceptions.exceptions import GenericCollectionException


class GenericCollection(BaseCollection):

    def __init__(self, connection, template):
        name = template['name']
        __keys = template['keys']
        self.__keys = []
        for key in __keys:
            for field in key.keys():
                self.__keys.append(field)
        if name is None or name == "":
            raise GenericCollectionException("name is missing")
        super(GenericCollection, self).__init__(connectionManager=connection, name=name)

    def save(self, data, currentDatetime=datetime.datetime.utcnow()):
        key_data = {}
        for k in self.get_keys():
            key_data[k] = data[k]

        uuid = str(uuid4())
        document = {"_id": uuid, "update": currentDatetime, "fields": data}
        # add data_key in document
        if key_data:
            document['key_data'] = key_data
        return BaseCollection.save(self, document)

    def find_by_keys(self, keys):
        if keys is None:
            raise GenericCollectionException('keys are missing')
        ks = self.get_keys()
        key_data = {}
        for k in ks:
            key_data['key_data.' + k] = keys[k]
        doc = super(GenericCollection, self).find_one(key_data)
        if doc:
            return doc['fields']

    def get_keys(self):
        '''
        return fieldname that uses for the key
        '''
        return self.__keys
