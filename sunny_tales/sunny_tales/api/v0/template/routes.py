'''
Created on Apr 2, 2013

@author: tosako
'''

from pyramid.view import view_config
from sunny_tales.database.collections.toolbox import Toolbox
from sunny_tales.database.collections.templates import Templates
import uuid
import datetime
from bson import json_util
import json
from pyramid.httpexceptions import HTTPNotFound, HTTPBadRequest
from sunny_tales.api.v0.template.exceptions import InvalidPayloadError
from cloudy_tales.data_fusion.translate import combine_template_with_data
from cloudy_tales.database.connectionManager import DbConnectionManager
from cloudy_tales.database.collections.base import BaseCollection
from cloudy_tales.queue import producer
from pyramid.response import Response


@view_config(route_name='toolbox', request_method='GET', renderer='json')
def get_toolbox(request):
    with DbConnectionManager() as connection:
        toolbox = Toolbox(connection)
        results = toolbox.find_one()

    return results


@view_config(route_name='individual_template', request_method='GET', renderer='json')
def get_template(request):
    '''
    Handles GET requests for a template, /templates/{uuid}
    '''
    uuid = request.matchdict['uuid']

    # TODO: static class instead of instance?
    with DbConnectionManager() as connection:
        templates = Templates(connection)
        results = templates.find_one_by_id(uuid)
    if results is None:
        return HTTPNotFound()

    # We need this because of date formmating in mongo is not in json
    return __convert_mongo_bson_to_json(results)


@view_config(route_name='individual_template', request_method='PUT', renderer='json')
def save_custom_template(request):
    '''
    Handles PUT requests to save new and overwrite existing custom template into template collection
    '''
    doc_id = request.matchdict['uuid']
    document = {}
    try:
        document.update(__get_payload(request))
    except InvalidPayloadError:
        return HTTPBadRequest()
    document['metadata'] = __generate_metadata(doc_id)

    with DbConnectionManager() as connection:
        templates = Templates(connection)
        results = templates.find_one_by_id(doc_id)
        if results is not None:
            # Need to archive if uuid exists in db
            # Current concept:  add metaData with timestamp and save 'parend_id'
            # To get current revision, look for parent_id = uuid with latest timestamp
            # To revert, delete/pop the latest timestamp
            # Idea 2:  swap content, so document with _id is always the most uptodate
            new_id = str(uuid.uuid4())
            document['_id'] = new_id

        # TODO: should I return the new_id or original id?
        results = templates.save(document)

    if results is None:
        raise HTTPBadRequest()
    return {'_id': doc_id}


@view_config(route_name='templates', request_method='GET', renderer='json')
def get_all_templates(request):
    '''
    Returns all custom templates' id
    '''
    with DbConnectionManager() as connection:
        templates = Templates(connection)
        results = templates.find()
    ids = []
    for result in results:
        ids.append(result['_id'])
    return ids


@view_config(route_name='templates', request_method='POST', renderer='json')
def create_new_template(request):
    '''
    Handles POST to /templates
    '''
    document = {}
    doc_id = str(uuid.uuid4())
    document['_id'] = doc_id

    try:
        document.update(__get_payload(request))
    except InvalidPayloadError:
        return HTTPBadRequest()

    document['metadata'] = __generate_metadata(doc_id)

    with DbConnectionManager() as connection:
        templates = Templates(connection)
        result = templates.insert(document)
    return result


@view_config(route_name='create_pdf', request_method='GET', renderer='json')
def create_pdf(request):
    '''
    Handles GET requests /createpdf/{uuid}/{trans_ref_no}
    '''
    uuid = request.matchdict['uuid']
    trans_ref_no = request.matchdict['trans_ref_no']

    with DbConnectionManager() as connection:
        templates = Templates(connection)
        # Since we archive revisions of templates
        # Get the current one
        current = templates.find_current(uuid)
        # Still get the original (parent) revision to return to FE
        parent = templates.find_by_id(uuid)

        collection = BaseCollection(connection, 'Transheader')
        key_data = {'key_data.trans_ref_no': trans_ref_no}
        data = collection.find_one(key_data)

    # Calls data fusion service to template, if any, writes to /tmp/template.json
    result = combine_template_with_data(template=current, data=data)

    # publish the templated result to the queue to create pdf
    pdf_content = producer.publish(result)

    #return __convert_mongo_bson_to_json(parent)
    return Response(body=pdf_content, content_type='application/pdf')


def __get_payload(request):
    '''
    Request python dictionary of request payload
    '''
    try:
        # pyramid tests if the payload is json format, throws exception if it isn't
        body = request.json_body
    except ValueError:
        raise InvalidPayloadError
    return body


def __generate_metadata(parent_id):
    '''
    Generate metadata for a template
    '''
    return {'parent_id': parent_id, 'timestamp': datetime.datetime.utcnow()}


def __convert_mongo_bson_to_json(results):
    # We need this because of date formmating in mongo is not in json
    json_str = json.dumps(results, default=json_util.default)
    return json.loads(json_str)
