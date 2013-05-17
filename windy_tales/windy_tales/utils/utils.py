'''
Created on May 5, 2013

@author: dorisip
'''
import os
import errno


def read_file(file_name):
    '''
    Read and return list of content of a file in file system
    '''
    if os.path.exists(file_name) is False:
        raise IOError
    with open(file_name, 'r') as reader:
        content = reader.readlines()
    return content


def mkdir_p(path):
    '''
    Mimics mkdir -p
    '''
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise
