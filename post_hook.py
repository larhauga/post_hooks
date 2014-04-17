#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys
import daemon.runner

path = os.path.dirname(os.path.abspath(__file__))
os.chdir(path)
from bin import config as cfg
logging = cfg.get_logger()
config  = cfg.get_config()
logger = logging.getLogger('main')

class post_hook():
    def __init__(self):
        self.stdin_path       = config.get('daemon', 'stdin_path')
        self.stdout_path      = config.get('daemon', 'stdout_path')
        self.stderr_path      = config.get('daemon', 'stderr_path')
        self.pidfile_path     = os.path.abspath(config.get('daemon', 'pidfile_path'))
        self.pidfile_timeout  = config.getint('daemon', 'pidfile_timeout')

    def run(self):
        try:
            # We need to import post_server here to resolve file descriptor issue
            # http://stackoverflow.com/questions/20636678/paramiko-inside-python-daemon-causes-ioerror?rq=1
            os.chdir(path)
            from bin import post_server
            post_server.main()
        except SystemExit:
            logger.info("post_hook system stopped.")
            print "post_hook system stopped."


if __name__ == '__main__':
    if len(sys.argv) == 2:
        try:
            post_hook = post_hook()
            runner = daemon.runner.DaemonRunner(post_hook)

            runner.daemon_context.files_preserve=[logger.handlers[0].stream]
            runner.do_action()
        except:
            logger.error("Daemon error", exc_info=True)
            print "Daemon stopped"
    else:
        print "Usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(1)
else:
    print "This cannot be included in another program"
