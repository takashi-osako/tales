'''
Created on May 5, 2013

@author: dorisip
'''
import unittest
from windy_tales.utils.utils import read_file
import os
from windy_tales.flat_file.header_parser import HeaderParser
from windy_tales.flat_file.parser import flat_to_json, convert_to_unordered_json
from cloudy_tales.database.tests.UnitTestWithMongoDB import UnitTestWithMongoDB
from windy_tales.database.collections.header_file_parsed_template import HeaderfileParsedTemplate
from cloudy_tales.database.connectionManager import DbConnectionManager


class TestParser(UnitTestWithMongoDB):

    def setUp(self):
        # Parse c header first
        here = os.path.abspath(os.path.dirname(__file__))
        file_name = os.path.join(here, '..', 'resources', 'sample.h')
        json = HeaderParser.generate_tempate(file_name)
        with DbConnectionManager() as connector:
            header = HeaderfileParsedTemplate(connector)
            header.save(data_name='sample', data=json, version=0)

    def test_flat_file_to_json(self):
        here = os.path.abspath(os.path.dirname(__file__))
        file_name = os.path.join(here, '..', 'resources', 'sample.flat')
        flat_content = read_file(file_name)
        value = flat_to_json('sample', flat_content[0])
        self.assertIsNotNone(value)

        self.assertEquals(value['book']['title'], 'Book Name')
        self.assertEquals(value['book']['description'], 'my desc')
        self.assertEquals(value['book']['ack'][0]['name'], 'Alex')
        self.assertEquals(value['book']['ack'][1]['name'], 'Ben')

    def test_flat_file_to_json_with_truncated_flat_file(self):
        here = os.path.abspath(os.path.dirname(__file__))
        file_name = os.path.join(here, '..', 'resources', 'truncated_sample.flat')
        flat_content = read_file(file_name)
        value = flat_to_json('sample', flat_content[0])
        self.assertEquals(value['book']['title'], 'MyBook')
        self.assertEquals(value['book']['description'], '')
        self.assertEquals(value['book']['ack'][0]['name'], '')
        self.assertEquals(value['book']['ack'][1]['name'], '')

    def test_flat_file_to_json_with_extra_characters_in_flat(self):
        here = os.path.abspath(os.path.dirname(__file__))
        file_name = os.path.join(here, '..', 'resources', 'extra_sample.flat')
        flat_content = read_file(file_name)
        value = flat_to_json('sample', flat_content[0])

        self.assertEquals(value['book']['ack'][0]['name'], 'Alex')
        self.assertEquals(value['book']['ack'][1]['name'], 'Benjam')

    def test_convert_to_unordered_json_simple(self):
        data = {'one': [{'two': 'three'}, {'four': 'five'}]}
        result = convert_to_unordered_json(data)
        self.assertEquals(len(result['one'].keys()), 2)
        self.assertEquals(result['one']['two'], 'three')
        self.assertEquals(result['one']['four'], 'five')

    def test_convert_to_unordered_json_inner_struct(self):
        data = {'one': [{'two': [[{'three': 'four'}, {'five': 'six'}], [{'seven': 'eight'}, {'nine': 'ten'}]]}]}
        result = convert_to_unordered_json(data)
        self.assertEquals(len(result['one'].keys()), 1)
        self.assertIs(type(result['one']['two']), list)
        self.assertEquals(result['one']['two'][0]['three'], 'four')
        self.assertEquals(result['one']['two'][0]['five'], 'six')
        self.assertEquals(result['one']['two'][1]['seven'], 'eight')
        self.assertEquals(result['one']['two'][1]['nine'], 'ten')

    def test_convert_to_unordered_json_complex(self):
        data = {'one': [{'two': [[{'three': 'four'}], [{'five': 'six'}]]}, [{'seven': 'eight'}], [{'nine': [[{'ten': 'zero'}]]}]]}
        result = convert_to_unordered_json(data)
        self.assertEquals(len(result['one'].keys()), 3)
        self.assertEquals(result['one']['nine'][0]['ten'], 'zero')
        self.assertEquals(result['one']['two'][0]['three'], 'four')


if __name__ == "__main__":
    unittest.main()
