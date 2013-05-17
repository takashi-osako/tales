'''
Created on Apr 2, 2013

@author: tosako
'''
import os
import json


def get_element_json():
    here = os.path.abspath(os.path.dirname(__file__))
    template = os.path.join(here, '..', 'resources', 'elements.json')
    with open(template, 'r') as f:
        template_json = f.read()
    return json.loads(template_json)
