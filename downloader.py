#!/usr/bin/python
# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 3, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTIBILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.


__author__ = "David Bush (david@david-bush.co.uk)"
__copyright__ = "Copyright (C) 2012 David Bush"
__license__ = "LGPL 3.0"
__version__ = "0.1"

import os
import Queue
import threading
import urllib2

# A bunch of Calvin and Hobbes comics for testing:
URLS = (
        'http://assets.amuniversal.com/a67214a0ba2e012fda3c001dd8b71c47',
        'http://assets.amuniversal.com/a4a026e0ba2e012fda3c001dd8b71c47',
        'http://assets.amuniversal.com/a2b58f40ba2e012fda3c001dd8b71c47',
        'http://assets.amuniversal.com/30ef15801df3012f2fc700163e41dd5b',
        'http://assets.amuniversal.com/a0fc17e0ba2e012fda3c001dd8b71c47',
        'http://assets.amuniversal.com/9f683a80ba2e012fda3c001dd8b71c47',
)
DOWNLOAD_DIRECTORY = 'Downloads'


class Downloader(threading.Thread):
    '''
    Threaded URL downloader.
    '''
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

        # Create 'Downloads' directory if it doesn't exist:
        if not os.path.exists(DOWNLOAD_DIRECTORY):
            os.makedirs(DOWNLOAD_DIRECTORY)

    def run(self):
        # Override Thread's run() method.
        while True:
            url = self.queue.get()
            self.download_file(url)
            self.queue.task_done()

    def download_file(self, url):
        '''
        Downloads whatever url is passed to it.
        '''
        asset = urllib2.urlopen(url)
        file_name = os.path.basename(url)

        # Pass 'b' to open() to force binary mode (if the system supports it):
        with open('%s/%s.gif' % (DOWNLOAD_DIRECTORY, file_name), "wb") as f:
                # TODO: Put in a check here for system memory before dl.
            while True:
                # read() will return an empty string at EOF:
                part = asset.read(1024)
                if not part:
                    break
                f.write(part)

        # TODO: Return download success status
        # Output to terminal.


def main(urls):
    """
    Adds urls to queue, instantiates Downloader() class and downloads urls.
    """
    queue = Queue.Queue()

    for i in xrange(5):
        thread = Downloader(queue)
        thread.setDaemon(True)  # to allow clean exit if cut short.
        thread.start()

    # TODO: Add memoization.
    # TODO: Maybe set something up to make number of threads proportional
    # to len(URLS)
    [queue.put(url) for url in URLS]
    # for url in URLS:
        # queue.put(url)

    queue.join()

if __name__ == "__main__":
    main(URLS)
    # Benchmarking:
    # time ./downloader.py
    # 11.514
    # Why is this slower? Profile it, but suspect GIL thrashing.
