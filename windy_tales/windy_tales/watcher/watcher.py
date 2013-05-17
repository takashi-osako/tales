'''
Created on May 5, 2013

@author: dorisip
'''
from watchdog.observers import Observer
from windy_tales.watcher.event_handler import WatcherEventHandler
import os
from windy_tales.utils.utils import mkdir_p


class Watcher():
    '''
    Watches a directory for file/directory creations
    '''
    def __init__(self, dir_name):
        self.__dir = dir_name
        self.__observer = Observer()

    def watch_dir(self):
        '''
        Watches a directory recursively for file creation
        '''
        if os.path.exists(self.__dir) is False:
            mkdir_p(self.__dir)
        event_handler = WatcherEventHandler()
        self.__observer.schedule(event_handler, self.__dir, recursive=True)
        print "Watching dir: %s" % self.__dir
        self.__observer.start()

    def stop(self):
        self.__observer.stop()

    def join(self):
        self.__observer.join()
