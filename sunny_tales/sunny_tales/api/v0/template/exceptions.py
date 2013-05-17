'''
Created on Apr 14, 2013

@author: dorisip
'''


class ApiError(Exception):
    '''
    Generic Error
    '''
    def __init__(self, msg):
        self.msg = msg


class InvalidPayloadError(ApiError):
    '''
    Request payload is not json error
    '''
    def __init__(self):
        self.msg = "Invalid Payload"
