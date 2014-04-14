#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from flask import Flask, request
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
        print "NOT OK: Invalid data => %s" % str(ke)
        return ('NOT OK: Invalid data', 400)
    except Exception, e:
        print "Exception: %s" % str(e)
        return ('NOT OK: %s' % str(e), 500, '')

    try:
        repo = data['repository']
        name = repo['name']
        commits = data['commits']

        #for test in commits:
            #for entry in test.iteritems():
                #print entry

    except KeyError as ke:
        print "NOT OK: KeyError. Expected another input"
        return ('NOT OK: %s' % str(ke), 400, '')
    except Exception, e:
        print "Exception: %s" % str(e)
        return ('NOT OK: %s' % str(e), 500, '')

    return ('OK', 200, '')

if __name__ == '__main__':
    #app.debug = True
    app.run(host='0.0.0.0', port=9898)
