'''
Created on May 5, 2013

@author: dorisip
'''
import os
import signal
import atexit
from windy_tales.watcher.watcher import Watcher
import time
import sys
from windy_tales.flat_file.header_parser import HeaderParser
from cloudy_tales.database.client import create_db_client
from windy_tales.database.collections.header_file_parsed_template import HeaderfileParsedTemplate
from cloudy_tales.data_fusion.translate import generate_templated_json
from windy_tales.utils.data_loader import load_data_from_flatfile
from windy_tales.database.collections.generic_collection import GenericCollection
from cloudy_tales.database.connectionManager import DbConnectionManager

watcher = Watcher('/tmp/lz')


def main():
    '''
    Initializes watcher to monitor landing zone
    '''
    # initialize mongodb
    create_db_client(db_name='DUMBO')
    load_template()
    clear_data()
    load_flatfile_data()

    watcher.watch_dir()
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    while True:
        # sleeps until a signal is sent to process
        signal.pause()


def signal_handler(signal, frame):
    '''
    Catches Ctrl-C to exit
    '''
    print("Exiting")
    global watcher
    watcher.stop()
    watcher.join()
    sys.exit(0)


def load_template():
    header_files = ['transheader.h', 'transproduct.h', 'supplier.h', 'customer.h', 'account.h', 'terminal.h']
    here = os.path.abspath(os.path.dirname(__file__))
    with DbConnectionManager() as connection:
        headerFileParsedTemplate = HeaderfileParsedTemplate(connection=connection)
        headerFileParsedTemplate.remove()
        for header_file in header_files:
            file_name = os.path.join(here, 'resources', header_file)
            json = HeaderParser.generate_tempate(file_name)
            headerFileParsedTemplate.save(data_name=json.keys()[0], data=json, version=1)


def clear_data():
    targets = ['Supplier', 'Customer', 'Account', 'Terminal', 'Transheader']
    with DbConnectionManager() as connection:
        for target in targets:
            colleciton = GenericCollection(connection=connection, name=target)
            colleciton.remove()


def load_flatfile_data():
    flatfiles = ['supplier/supplier.flat', 'customer/customer.flat', 'account/account.flat', 'terminal/terminal.flat']
    here = os.path.abspath(os.path.dirname(__file__))
    for flatfile in flatfiles:
        file_name = os.path.join(here, 'resources', 'flatfiles', flatfile)
        print(file_name)
        load_data_from_flatfile(file_name)


if __name__ == '__main__':
    main()
