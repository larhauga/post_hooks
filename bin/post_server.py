#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
from flask import Flask, request
import local_pull, parse_bitbucket
import traceback
import config as cfg
logging = cfg.get_logger()
config  = cfg.get_config()

logging.info("Initializing server")
app = Flask(__name__)

@app.route('/')
def main():
    return "HTTP service"

@app.route('/gitpost', methods=['POST'])
def gitpost(debug=None,url='/gitpost'):
    try:
        if not debug:
            data = request.form['payload']

        repo, name, commits = parse_bitbucket.parse_bitbucket(data)
        branches = dict((y,x) for x, y in config.items('branches'))

        if config.get('main','pull_all'):
            # Pulling all branches
            local_pull.update_updated_branches(commits, branches,\
                    config.get('main', 'pull_all'), name=name)
        else:
            # Only pulling the commited brances
            local_pull.update_updated_branches(commits, branches)

    except (KeyError, TypeError, ValueError) as ke:
        logging.warn("HTTP 400 KeyError in %s: Invalid data" % url, exc_info=1)
        return ('NOT OK. Invalid data', 400, '')
    except Exception, e:
        logging.error("HTTP 500 returned (%s): " % url, exc_info=1)
        return ('NOT OK. Check log', 500, '')

    return ('OK', 200, '')

@app.route('/all', methods=['POST', 'GET'])
def all(url='/all'):
    try:
        if config.has_section('repo'):
            print config.items('repo')
            for repo in config.items('repo'):
                if config.has_section(repo[0]):
                    branches = dict((y,x) for x, y in config.items(repo[0]))
                    logging.info("Updating following branches: %s" % branches)
                    local_pull.update_repo(branches)
        else:
            if config.has_section('branches'):
                branches = dict((y,x) for x, y in config.items('branches'))
                logging.info("Updating following branches: %s" % branches)
                local_pull.update_repo(branches)

    except Exception, e:
        logging.error("HTTP 500 (%s)" % url, exc_info=1)
        return ('NOT OK', 500, '')

    return ('OK', 200, '')

def main():
    app.run(host=config.get('main','host'), port=config.getint('main','port'))

if __name__ == '__main__':
    if config.get('main', 'debug'):
        app.debug = True
