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
            if commits:
                local_pull.update_updated_branches(commits, branches,\
                        config.get('main', 'pull_all'), name=name)
            else:
                logging.warn("Repo %s: No commits" % name)
        else:
            # Only pulling the commited brances
            local_pull.update_updated_branches(commits, branches)

    except (KeyError, TypeError, ValueError) as ke:
        if config.get('main', 'debug'):
            logging.warn("HTTP 400 KeyError in %s: Returned NOT OK, INVALID DATA"\
                % url, exc_info=1)
        return ('NOT OK: %s' % str(ke), 400, '')
    except Exception, e:
        if config.get('main', 'debug'):
            logging.error("HTTP 500 returned in %s: Returned NOT OK"\
                % url, exc_info=1)
        return ('NOT OK: %s' % str(e), 500, '')

    return ('OK', 200, '')

@app.route('/all', methods=['POST', 'GET'])
def all(url='/all'):
    pass

def main():
    app.run(host=config.get('main','host'), port=config.getint('main','port'))

if __name__ == '__main__':
    if config.get('main', 'debug'):
        app.debug = True
