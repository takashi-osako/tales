'''
Created on May 12, 2013

@author: tosako
'''
from cloudy_tales.database.connectionManager import DbConnectionManager
from cloudy_tales.database.collections.base import BaseCollection
from cloudy_tales.exceptions.templateNotFound import TemplateNotFound


def get_template(tempalte_name):
    # get template
    with DbConnectionManager() as connection:
        template_colleciton = BaseCollection(connectionManager=connection, name='templates')
        template = template_colleciton.find_one({"name": tempalte_name})
    # Temporary template the flat file's data and save to /tmp/template.json
    # use mustache
    if template is None:
        raise TemplateNotFound(tempalte_name)
