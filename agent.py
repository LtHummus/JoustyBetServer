#!/usr/bin/env python


import sys
import logging
import time
import requests
import os

from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler, FileSystemEventHandler

POST_URL = "http://192.168.1.37:5000/post-game-event"
SHARED_SECRET = "CHANGEME"

class JoustServerUpdater(FileSystemEventHandler):

    def __init__(self, filename):
        self.stat_file = filename
        self.last_read = ""

    def post_contents(self, contents):
        headers = {'Authentication': SHARED_SECRET}
        r = requests.post(POST_URL, data=contents, headers=headers)
        logging.info("Posted some data to the website: %s", contents)

    def check_file(self):
        logging.info("Looking at file...")
        with open(self.stat_file, 'r') as f:
            contents = ''.join(f.readlines())
            logging.debug("Read contents: '%s'", contents)
            if contents != self.last_read:
                self.post_contents(contents)
            self.last_read = contents

    def on_modified(self, event):
        self.check_file()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    logging.info("Hello world!")

    if len(sys.argv) < 2:
        print("Hey, you need to give me a file, dipshit.")
        sys.exit(1)

    filename = sys.argv[1]
    file_parent = os.path.dirname(filename)

    logging.info("Using source file: %s", filename)
    logging.info("Using parent file: %s", file_parent)

    observer = Observer()
    observer.schedule(JoustServerUpdater(filename), file_parent)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()



