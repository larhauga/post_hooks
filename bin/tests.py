#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import flask
import unittest
import tempfile
import post_server
import local_pull

class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        post_server.app.config['TESTING'] = True
        self.app = post_server.app.test_client()

    def tearDown(self):
        pass

    def test_main(self):
        rv = self.app.get('/')
        assert "HTTP service" in rv.data

    def test_gitpost(self):
        data = '{"repository": {"website": "", "fork": false, "name": "posthooktest", "scm": "git", "owner": "larhauga", "absolute_url": "/larhauga/posthooktest/", "slug": "posthooktest", "is_private": true}, "truncated": false, "commits": [{"node": "b40227fabf75", "files": [{"type": "modified", "file": "README.md"}], "raw_author": "Lars Haugan <lars@larshaugan.net>", "utctimestamp": "2014-04-14 21:41:52+00:00", "author": "larhauga", "timestamp": "2014-04-14 23:41:52", "raw_node": "b40227fabf7579e235cb2b4e17bff2a932295ed4", "parents": ["082c6af58e45"], "branch": "master", "message": "New commit", "revision": null, "size": -1}], "canon_url": "https://bitbucket.org", "user": "larhauga"}'
        payload = {'payload': data}
        rv = self.app.post('/gitpost',
            data = payload,
            headers = {'content-type': "application/x-www-form-urlencoded"}
        )
        self.assertEqual(rv.status_code, 200)

    def test_debug_gitpost(self):
        data = '{"repository": {"website": "", "fork": false, "name": "posthooktest", "scm": "git", "owner": "larhauga", "absolute_url": "/larhauga/posthooktest/", "slug": "posthooktest", "is_private": true}, "truncated": false, "commits": [{"node": "b40227fabf75", "files": [{"type": "modified", "file": "README.md"}], "raw_author": "Lars Haugan <lars@larshaugan.net>", "utctimestamp": "2014-04-14 21:41:52+00:00", "author": "larhauga", "timestamp": "2014-04-14 23:41:52", "raw_node": "b40227fabf7579e235cb2b4e17bff2a932295ed4", "parents": ["082c6af58e45"], "branch": "master", "message": "New commit", "revision": null, "size": -1}], "canon_url": "https://bitbucket.org", "user": "larhauga"}'
        req = post_server.gitpost(data)
        self.assertEqual(req[1], 200)
        self.assertEqual(req[0], "OK")

    def test_invalid_data_gitpost(self):
        rv = self.app.post('/gitpost',
                data='nionfsidoanofnsaonfsaiodnfas')
        self.assertEqual(rv.status_code, 400)

    def test_invalid_data2_gitpost(self):
        rv = self.app.post('/gitpost',
                data='nionfsidoanofnsaonfsaiodnfas')
        self.assertNotEqual(rv.data, "NOT OK")

if __name__ == '__main__':
    unittest.main()
