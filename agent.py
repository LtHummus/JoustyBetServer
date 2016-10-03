#!/usr/bin/env python


import sys
import logging
import time
import requests

LAST_READ = ""
SECONDS_BETWEEN_CHECKS = 2
POST_URL = "http://localhost:5000/post-game-event"
SHARED_SECRET = "CHANGEME"


def post_contents(contents):
    headers = {'Authentication': SHARED_SECRET}
    r = requests.post(POST_URL, data=contents, headers=headers)
    logging.info("Posted some data to the website: %s", contents)


def check_file(filename):
    global LAST_READ  # I AM A GOOD CODER
    with open(filename, 'r') as f:
        contents = ''.join(f.readlines())
        logging.debug("Read contents: '%s'", contents)
        if contents != LAST_READ:
            post_contents(contents)
        LAST_READ = contents


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logging.info("Test")

    if len(sys.argv) < 2:
        print("Hey, you need to give me a file, dipshit.")
        sys.exit(1)

    filename = sys.argv[1]

    logging.info("Using source file: %s", filename)

    while True:
        check_file(filename)
        time.sleep(SECONDS_BETWEEN_CHECKS)

