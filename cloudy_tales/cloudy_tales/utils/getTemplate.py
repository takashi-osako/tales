'''
Created on May 12, 2013

@author: tosako
'''
from cloudy_tales.database.connectionManager import DbConnectionManager
from cloudy_tales.database.collections.base import BaseCollection
from cloudy_tales.exceptions.templateNotFound import TemplateNotFound


def get_template(template_name):
    # get template
    with DbConnectionManager() as connection:
        template_collection = BaseCollection(connectionManager=connection, name='templates')
        template = template_collection.find_one({"name": template_name})
    if template is None:
        raise TemplateNotFound(template_name)
    return template
