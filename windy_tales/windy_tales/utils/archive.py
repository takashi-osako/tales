'''
Created on May 6, 2013

@author: dorisip
'''
import os
from windy_tales.utils.utils import mkdir_p
import shutil
import datetime


def achive_file(file_name, archive_dir='/tmp/archive'):
    '''
    Moves file to archive directory
    '''
    # TODO: mkdir at startup only?
    if os.path.exists(archive_dir) is False:
        mkdir_p(archive_dir)

    if os.path.exists(file_name):
        base_name = os.path.basename(file_name)
        dest_name = os.path.join(archive_dir, base_name + '.' + datetime.datetime.now().strftime("%m-%d-%y-%T"))
        shutil.move(file_name, dest_name)
