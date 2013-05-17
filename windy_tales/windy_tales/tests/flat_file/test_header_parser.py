'''
Created on May 5, 2013

@author: dorisip
'''
from windy_tales.flat_file.header_parser import HeaderParser
import os
from windy_tales.database.collections.header_file_parsed_template import HeaderfileParsedTemplate
import unittest
from windy_tales.exceptions.exceptions import HeaderFileNotFound
from cloudy_tales.database.tests.UnitTestWithMongoDB import UnitTestWithMongoDB
from cloudy_tales.database.connectionManager import DbConnectionManager


class TestHeaderParser(UnitTestWithMongoDB):

    def setUp(self):
        with DbConnectionManager() as connection:
            headerParsed = HeaderfileParsedTemplate(connection)
            headerParsed.remove()

    def test_get_template_with_invalid_name(self):
        self.assertRaises(HeaderFileNotFound, HeaderParser.get_template, 'invalid')

    def test_generate_tempate_from_sample(self):
        here = os.path.abspath(os.path.dirname(__file__))
        file_name = os.path.join(here, '..', 'resources', 'sample.h')
        json = HeaderParser.generate_tempate(file_name)
        with DbConnectionManager() as connection:
            headerParsed = HeaderfileParsedTemplate(connection)
            headerParsed.save(data_name='sample', data=json, version=0)
        template = HeaderParser.get_template('sample')

        self.assertEquals(template['book'][0]['title'], 10)
        self.assertEquals(template['book'][2]['ack'][0][0]['name'], 6)

    def test_generate_template_unsupported_header_file(self):
        here = os.path.abspath(os.path.dirname(__file__))
        file_name = os.path.join(here, '..', 'resources', 'unsupported.h')
        json = HeaderParser.generate_tempate(file_name)
        with DbConnectionManager() as connection:
            headerParsed = HeaderfileParsedTemplate(connection)
            headerParsed.save(data_name='sample', data=json, version=0)
        template = HeaderParser.get_template('sample')

        self.assertEquals(template['book'][0]['title'], 10)
        self.assertEquals(len(template['book']), 1)


if __name__ == "__main__":
    unittest.main()
