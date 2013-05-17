'''
Created on Apr 7, 2013

@author: dorisip
'''
from cloudy_tales.database.collections.base import BaseCollection
import pymongo


class Templates(BaseCollection):

    def __init__(self, connection, name='templates'):
        super(Templates, self).__init__(connectionManager=connection, name=name)

    def find_current(self, doc_id):
        '''
        Returns current revision of template
        '''
        results = self.find_all_revisions(doc_id, limit=1)
        if results is not None:
            results = results[0]
        return results

    def find_all_revisions(self, doc_id, limit=0):
        '''
        Returns a list of revisions of template in descending timestamp order
        '''
        return super(Templates, self).find({'metadata.parent_id': doc_id},
                                           sort=[('metadata.timestamp', pymongo.DESCENDING)],
                                           limit=limit)

    def revert_to_previous(self, doc_id):
        '''
        Reverts to previous revision, returns the current revision
        '''
        revisions = self.find_all_revisions(doc_id)
        if len(revisions) > 1:
            current = revisions[0]
            self.remove_by_id(current['_id'])
            return revisions[1]
        else:
            # There is nothing to revert
            return revisions[0]
