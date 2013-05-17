'''
Created on May 12, 2013

@author: tosako
'''


class CloundyException(Exception):
    '''
    base class for exceptions
    '''
    pass


class TemplateNotFound(CloundyException):
    '''
    Raised when C header file is not found
    '''
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return repr(self.name)
