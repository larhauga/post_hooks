#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This is a module that is used for parsing bitbucket
# post request data. The output of this should be at least
# Returns:
#   repo    => (not used)
#   name    =>
#   commits => List of dicts

import logging, os
import logging.config
import json

if os.path.isfile("etc/logging.conf"):
    logging.config.fileConfig('etc/logging.conf')

def parse_bitbucket(payload):
    # Getting the data, either test or prod data
    data = json.loads(payload)

    # Parsing the data
    repo = data['repository']
    name = repo['name']
    commits = data['commits']
    return repo, name, commits
