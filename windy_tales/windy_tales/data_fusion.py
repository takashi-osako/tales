'''
Created on May 11, 2013

@author: dorisip
'''
from cloudy_tales.database.connectionManager import DbConnectionManager
from windy_tales.database.collections.generic_collection import GenericCollection
import json
from bson import json_util
from cloudy_tales.data_fusion.translate import generate_templated_json
from cloudy_tales.utils.exporter import export
import argparse
from cloudy_tales.database.client import create_db_client
import windy_tales


def template_json(flat_id, data_name, template_id=None):
    with DbConnectionManager() as connection:
        genericCollection = GenericCollection(connection, data_name)
        data = genericCollection.find_one_by_id(flat_id)

    # Temporary template the flat file's data and save to /tmp/template.json
    with DbConnectionManager() as sunny_connection:
        template_col = GenericCollection(sunny_connection, 'templates')
        if template_id:
            templ = template_col.find_one_by_id(template_id)
        else:
            templ = template_col.find_one()

        if templ:
            templ = json.dumps(templ, default=json_util.default)
            # use mustache
            generated = generate_templated_json(templ, data['metadata'])
            # Write to /tmp/template.json
            export(json.loads(generated))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Inject flat file values into custom template and output to /tmp/template.json')
    parser.add_argument("-d", "--data_name", help="set data name. Required")
    parser.add_argument("-f", "--flat", help="set flat file id. Required")
    parser.add_argument("-t", "--template", help="set custom template id")

    args = parser.parse_args()

    __flat_id = args.flat
    __template_id = args.template
    __data_name = args.data_name

    if __flat_id and __data_name:
        # initialize mongodb
        create_db_client()
        windy_tales.load_template()

        template_json(__flat_id, __data_name, __template_id)
    else:
        print ("Please provide flat file id and data name")
