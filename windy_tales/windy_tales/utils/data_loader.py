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
from cloudy_tales.queue import producer
from windy_tales.flat_file.header_parser import HeaderParser
import copy


def load_data_from_flatfile(filename):
    '''
    Flat file is given, convert it to json
    '''
    flat_contents = read_file(filename)
    for flat_content in flat_contents:
        # read first 20 chracters as data name
        data_name = flat_content[0:20].strip()
        content = flat_content[20:]

        # Get the Header Template
        template = HeaderParser.get_template(data_name)

        json_format = flat_to_json(template, content)

        with DbConnectionManager() as connection:
            # find data collection

            genericCollection = GenericCollection(connection, template)

            doc_id = genericCollection.save(json_format)

        # if data is transheader, then aggregate data for Data Fusion Service
        if data_name == "Transheader":
            json_format = aggregate_for_transaction(json_format)
            # TODO: TEMP:  get a template with the name 'test'
            template = get_template('test')
            combined = combine_template_with_data(template=template, data=json_format)

            # publish the templated result to the queue to create pdf
            if combined is not None:
                producer.publish(combined)

        print("#####")
        print(json.dumps(json_format))
        print("#####")
    return json_format
