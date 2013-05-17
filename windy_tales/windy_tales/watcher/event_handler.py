'''
Created on May 5, 2013

@author: dorisip
'''
from watchdog.events import FileSystemEventHandler
from windy_tales.utils.archive import achive_file
import os
from windy_tales.exceptions.exceptions import HeaderFileNotFound
from windy_tales.utils.data_loader import load_data_from_flatfile


class WatcherEventHandler(FileSystemEventHandler):

    def on_moved(self, event):
        '''
        Only listen for move or rename from landing zone to a file within the landing zone
        '''
        if event.is_directory is False:
            file_name, file_ext = os.path.splitext(event.dest_path)
            if file_ext == '.flat':
                print("File renamed in LZ: " + event.dest_path)
                try:
                    # New file is received, convert flat file to json format
                    load_data_from_flatfile(event.dest_path)
                    # archive the file
                    achive_file(event.dest_path)

                except HeaderFileNotFound as e:
                    print('Header template: %s not found' % e.name)
                except Exception as e:
                    print(e)
