'''
Created on Apr 14, 2013

@author: dorisip
'''
from pyramid.testing import DummyRequest
import json


class SunnyDummyRequest(DummyRequest):

    json_body = {}

    def __init__(self, *args, **kwargs):
        super(SunnyDummyRequest, self).__init__(*args, **kwargs)


class SunnyDummyInvalidJsonBodyRequest(DummyRequest):
    '''
    Dummy class that throws error when reading bad json
    '''
    @property
    def json_body(self):
        return json.loads('bad data')
