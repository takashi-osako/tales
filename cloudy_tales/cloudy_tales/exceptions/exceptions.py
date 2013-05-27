'''
Created on May 12, 2013

@author: tosako
'''


class CloudyException(Exception):
    '''
    base class for exceptions
    '''
    pass


class TemplateNotFound(CloudyException):
    '''
    Raised when C header file is not found
    '''
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return repr(self.name)


class RPCTimeout(CloudyException):
    '''
    Raised when rpc times out while waiting for result to be returned
    '''
    def __init__(self):
        pass

    def __str__(self):
        return "Timeout waiting for pdf content from queue"
