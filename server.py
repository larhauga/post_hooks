#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import logging.config
import os

os.chdir("/root/post/")
from bin import post_server

logging.config.fileConfig('etc/logging.conf')
logging.getLogger('main')

if __name__ == '__main__':
    post_server.main()
