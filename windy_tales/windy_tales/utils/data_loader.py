'''
Created on May 11, 2013

@author: tosako
'''
from windy_tales.utils.utils import read_file
from windy_tales.flat_file.parser import flat_to_json
from windy_tales.database.collections.generic_collection import GenericCollection
from windy_tales.data_aggregator.transaction_aggregator import aggregate_for_transaction
import json
from cloudy_tales.data_fusion.translate import combine_template_with_data
from cloudy_tales.utils.getTemplate import get_template
from cloudy_tales.database.connectionManager import DbConnectionManager


def load_data_from_flatfile(filename):
    flat_contents = read_file(filename)
    for flat_content in flat_contents:
        # read first 20 chracters as data name
        data_name = flat_content[0:20].strip()
        content = flat_content[20:]
        json_format = flat_to_json(data_name, content)

        with DbConnectionManager() as connection:
            # find data collection
            try:
                collection_module = __import__('windy_tales.database.collections.' + data_name.lower(), globals(), locals(), [data_name])
                if collection_module:
                    genericCollection = getattr(collection_module, data_name)(connection)
                else:
                    genericCollection = GenericCollection(connection, data_name)
            except:
                genericCollection = GenericCollection(connection, data_name)
            doc_id = genericCollection.save(json_format)

        # if data is transheader, then aggregate data for Data Fusion Service
        if data_name == "Transheader":
            json_format = aggregate_for_transaction(json_format)
            # TODO: TEMP:  template json from flat file data
            template = get_template('test')
            combine_template_with_data(template=template, data=json_format, write_to_file=True)

        print("#####")
        print(json.dumps(json_format))
        print("#####")
    return json_format
