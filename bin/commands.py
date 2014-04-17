#!/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess
import paramiko
import config as cfg
logging = cfg.get_logger()
config  = cfg.get_config()

def command(command):
    """ Wrapper for subprocess
    """
    logging.info("REQUEST: Running command: %s" % command)
    pr = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, err = pr.communicate()
    if err:
        logging.error("RESPONSE: while running command '%s': %s" % (command,err))
        return None
    else:
        logging.info("RESPONSE: Output of command '%s': %s" % (command, output))
        return output

def remote_command(host, command):
    if not host:
        raise ValueError("No host spesified")
    try:
        user,host = host.split("@")
    except ValueError:
        user = "root"

    password = config.get('main', 'ssh_password')

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    if password:
        ssh.connect(host, username=user, password=password)
    else:
        ssh.connect(host, username=user)

    logging.info("REQUEST: Running remote command '%s' on host %s@%s"\
            % (command, user, host))
    stdin, stdout, stderr = ssh.exec_command(command)
    logging.info("RESPONSE: Remote command exec output '%s': " % command )
    out = ""
    for line in stdout:
        logging.debug("RESPONSE OUTPUT: %s" % line.strip())
        out += line
    ssh.close()
    return out

