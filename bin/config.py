#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ConfigParser
import logging, logging.config
import os.path
from sys import exit

if os.path.isfile('etc/config.cfg'):
    config = ConfigParser.ConfigParser()
    config.read('etc/config.cfg')
else:
    logging.error("Missing configuration file 'etc/config.cfg'")
    exit(1)

if os.path.isfile(config.get('log','logconfig')):
    logging.config.fileConfig(config.get('log', 'logconfig'))
    logger = logging.getLogger(config.get('log', 'logger'))
else:
    logging.error("Missing logger configuration file 'etc/logging.confg'")
    exit(1)

def get_config():
    return config

def get_logger():
    return logging
