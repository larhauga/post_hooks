#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json, os, sys
import ConfigParser
from flask import Flask, request
import local_pull

config = ConfigParser.ConfigParser()
if os.path.isfile("config.cfg"):
    config.read("config.cfg")
else:
    print "Missing configuration file config.cfg"
    sys.exit(1)

app = Flask(__name__)

@app.route('/')
def main():
    return "HTTP service"

@app.route('/gitpost', methods=['POST'])
def gitpost(debug=None):
    #print request.headers.get('content-type')
    #print request.data
    try:
        if not debug:
            payload =  request.form['payload']
            data = json.loads(payload)
        else:
            data = json.loads(debug)

    except (KeyError, TypeError, ValueError) as ke:
        #print "NOT OK: Invalid data => %s" % str(ke)
        return ('NOT OK: Invalid data', 400)
    except Exception, e:
        #print "Exception: %s" % str(e)
        return ('NOT OK: %s' % str(e), 500, '')

    try:
        repo = data['repository']
        name = repo['name']
        commits = data['commits']

        if local_pull.commit_in_branch(commits, branch="master"):
            print "yes"

            branches = config.items('branches')

    except KeyError as ke:
        print "NOT OK: KeyError. Expected another input"
        return ('NOT OK: %s' % str(ke), 400, '')
    except Exception, e:
        print "Exception: %s" % str(e)
        return ('NOT OK: %s' % str(e), 500, '')

    return ('OK', 200, '')

if __name__ == '__main__':
    if config.get('main', 'debug'):
        app.debug = True

    app.run(host=config.get('main','host'), port=config.getint('main','port'))

