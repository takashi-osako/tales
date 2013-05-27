'''
Created on May 26, 2013

@author: dorisip
'''
from pyramid.httpexceptions import HTTPException, HTTPRequestTimeout
import json


def prepare_exception_response(msg):
    return {'text': unicode(json.dumps({'error': msg})), 'content_type': 'application/json'}


class SunnyHTTPException(HTTPException):
    '''
    Generic http exception class
    '''
    def __init__(self, msg):
        super(SunnyHTTPException, self).__init__(**prepare_exception_response(msg))


class SunnyHTTPRequestTimeout(HTTPRequestTimeout):
    def __init__(self, msg='Timeout Occurred'):
        super(SunnyHTTPRequestTimeout, self).__init__(**prepare_exception_response(msg))
