'''
Created on May 9, 2013

@author: dorisip
'''
import pystache
import json
from cloudy_tales.utils.exporter import export
from bson import json_util


def generate_templated_json(template, data):
    '''
    Given a template, and data, Use mustache to template it
    '''
    return pystache.render(template, data)


def combine_template_with_data(template, data, write_to_file=True):
    '''
    Given template data, mustache it
    '''
    template = json.dumps(template, default=json_util.default)
    generated = generate_templated_json(template, data)
    generated = json.loads(generated)

    if write_to_file:
        # Write to /tmp/template.json
        export(generated)

    return generated
