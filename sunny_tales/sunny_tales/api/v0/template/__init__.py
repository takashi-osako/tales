from sunny_tales.utils.element_loader import get_element_json
import uuid
from sunny_tales.database.collections.toolbox import Toolbox
from cloudy_tales.database.client import create_db_client
from cloudy_tales.database.connectionManager import DbConnectionManager


def includeme(config):
    config.add_route('individual_template', '/templates/{uuid}')
    config.add_route('templates', '/templates')
    config.add_route('toolbox', 'toolbox')
    config.add_route('create_pdf', '/createpdf/{uuid}/{trans_ref_no}')

    # Create mongo client connection
    create_db_client(db_name='DUMBO')

    config.scan()

    # Temp: On startup, insert document if none exists
    with DbConnectionManager() as connector:
        toolbox = Toolbox(connector)
        toolbox.remove()
    document = {}
    document = get_element_json()
    document['_id'] = str(uuid.uuid4())

    # Save new template to db
    toolbox.insert(document)
