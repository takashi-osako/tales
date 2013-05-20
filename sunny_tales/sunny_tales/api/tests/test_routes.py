'''
Created on Apr 14, 2013

@author: dorisip
'''
import unittest
from sunny_tales.api.v0.template.routes import get_toolbox, get_template, \
    save_custom_template, get_all_templates, create_new_template
from sunny_tales.database.collections.toolbox import Toolbox
from pyramid.httpexceptions import HTTPNotFound, HTTPBadRequest
from sunny_tales.database.collections.templates import Templates
from sunny_tales.api.tests.dummy import SunnyDummyRequest, \
    SunnyDummyInvalidJsonBodyRequest
from cloudy_tales.database.connectionManager import DbConnectionManager
from cloudy_tales.database.tests.UnitTestWithMongoDB import UnitTestWithMongoDB


class TestRoutes(UnitTestWithMongoDB):

    def setUp(self):
        connection = DbConnectionManager()
        self.__toolbox = Toolbox(connection)
        self.__template = Templates(connection)
        self.__request = SunnyDummyRequest()

    def tearDown(self):
        self.__toolbox.remove()
        self.__template.remove()

    def test_empty_toolbox(self):
        tools = get_toolbox(self.__request)
        self.assertEquals({}, tools)

    def test_non_empty_toolbox(self):
        entry = {'_id': 123, 'elements': {'line': 'value'}}
        self.__toolbox.insert(entry)
        tools = get_toolbox(self.__request)
        self.assertEquals(tools, entry)

    def test_get_invalid_uuid_template(self):
        self.__request.matchdict['uuid'] = 123
        results = get_template(self.__request)
        self.assertIsInstance(results, HTTPNotFound)

    def test_get_valid_uuid_template(self):
        self.__request.matchdict['uuid'] = 123

        entry = {'_id': 123, 'template': {'line': 'value'}}
        self.__template.insert(entry)

        results = get_template(self.__request)
        self.assertEquals(results, entry)

    def test_save_custom_template(self):
        self.__request.matchdict['uuid'] = 123

        entry = {'_id': 123, 'components': {'line': 'value'}}
        self.__template.insert(entry)

        self.__request.json_body = {'_id': 123, 'components': {'line': 'circle'}}

        results = save_custom_template(self.__request)
        self.assertEqual(results['_id'], 123)
        results = self.__template.find_one_by_id(results['_id'])
        self.assertEquals(results['components']['line'], 'value')

    def test_save_custom_template_upsert(self):
        self.__request.matchdict['uuid'] = 123
        entry = {'_id': 123, 'components': {'line': 'value'}}
        self.__request.json_body = entry
        save_custom_template(self.__request)
        results = self.__template.find_by_id(123)
        self.assertEquals(results['_id'], entry['_id'])
        self.assertEquals(results['metadata']['parent_id'], 123)

    def test_get_all_templates_with_no_results(self):
        results = get_all_templates(self.__request)
        self.assertEquals(results, [])

    def test_get_all_templates(self):
        self.__template.insert({'_id': 123, 'components': {'line': 'value'}})
        self.__template.insert({'_id': 234, 'components': {'line': 'value'}})
        results = get_all_templates(self.__request)
        self.assertIn(123, results)
        self.assertIn(234, results)
        self.assertEquals(len(results), 2)

    def test_create_new_template(self):
        self.__request.json_body = {'_id': 123, 'components': {'line': 'value'}}
        results = create_new_template(self.__request)
        self.assertIsNotNone(results)
        self.assertIsNotNone(results['_id'])
        results = self.__template.find_one_by_id(123)
        self.assertIsNotNone(results['metadata'])
        self.assertEquals(results['components']['line'], 'value')

    def test_create_new_template_with_invalid_payload(self):
        self.__request = SunnyDummyInvalidJsonBodyRequest()
        results = create_new_template(self.__request)
        self.assertIsInstance(results, HTTPBadRequest)

    def test_save_custom_template_invalid_json(self):
        self.__request = SunnyDummyInvalidJsonBodyRequest()
        self.__request.matchdict['uuid'] = 123
        results = save_custom_template(self.__request)
        self.assertIsInstance(results, HTTPBadRequest)

    def test_create_pdf_with_no_transheader(self):
        self.__request.matchdict['uuid'] = 123
        self.__request.matchdict['trans_ref_no'] = 234
        self.__template.insert({'_id': 123, 'components': {'line': 'value'}})
        # TODO: how to run UT without rabbitmq


if __name__ == "__main__":
    unittest.main()
