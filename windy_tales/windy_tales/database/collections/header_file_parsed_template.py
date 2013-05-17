from cloudy_tales.database.collections.base import BaseCollection
import datetime
from uuid import uuid4


class HeaderfileParsedTemplate(BaseCollection):
    def __init__(self, connection, name="headerfile_parsed_template"):
        BaseCollection.__init__(self, connectionManager=connection, name=name)

    def save(self, data_name, data, version, currentDatetime=datetime.datetime.utcnow()):
        uuid = str(uuid4())
        document = {"_id": uuid, "name": data_name, "version": version, "update": currentDatetime, "metadata": data}
        return BaseCollection.save(self, document)

    def find_by_name(self, name):
        document = {"name": name}
        result = BaseCollection.find(self, document)
        if result:
            return result[0]
