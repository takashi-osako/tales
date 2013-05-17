'''
Created on Apr 19, 2013

@author: dorisip
'''
import json
from bson import json_util
import os


def export(data, tar_dir='/tmp'):
    file_name = os.path.join(tar_dir, 'template.json')
    with open(file_name, 'w') as f:
        components = {"components": data['components']}
        content = json.dumps(components, indent=4, default=json_util.default)
        f.write(content)
