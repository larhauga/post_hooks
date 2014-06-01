#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import commands as run
import config as cfg
logging = cfg.get_logger()
config  = cfg.get_config()

def last_commit(repopath):
    """ Gets the last commit information.
        This can be used to verify the latest commit
    """
    command = "cd %s; git log -1i --date=iso" % repopath
    out = run.command(command)
    if out:
        creg = re.compile(r"commit\s+(?P<remote_host>([a-f0-9]+))") # Commitid
        areg = re.compile(r"Author:\s+(?P<author>(.*$))") # author
        dreg = re.compile(r"Date:\s+(?P<date>(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}))") # Date
        last = {}

        for line in out.splitlines():
            commit = creg.search(line)
            author = areg.search(line)
            date = dreg.search(line)
            if commit:
                last['id'] = commit.group(1)
            elif author:
                last['author'] = author.group(1)
            elif date:
                last['date'] = date.group(1)

        return last
    else:
        return None

def branch(repopath, expected="master"):
    """ Checks the current branch of a repo.
        If branch == expected => True
    """
    repo = repopath.split(':')
    if len(repo) == 2:
        repopath = repo[1]
    command = "cd %s; git branch | grep \* | cut -d ' ' -f2" % repopath
    if len(repo) == 1:
        out = run.command(command)
    elif len(repo) == 2:
        out = run.remote_command(repo[0], command)

    if out:
        if expected in out:
            return True
        else:
            return False
    else:
        return None

def update(repopath, updatebranch="master"):
    """ Updates the branch by the given path and branch
        Can run update on remote branches
    """
    logging.debug("updating repo: %s, %s" % (repopath, updatebranch))
    if branch(repopath, updatebranch):
        repo = repopath.split(':')
        if len(repo) == 2:
            repopath = repo[1]

        command = "cd %s; git pull origin %s" % (repopath, updatebranch)

        if len(repo) == 1:
            out = run.command(command)
        elif len(repo) == 2:
            out = run.remote_command(repo[0], command)

        if out:
            for line in out.splitlines():
                logging.debug("OUTPUT" + line)
                if "Fast forward" in line:
                    return "Updated"
                elif "Already up-to-date." in line:
                    return "Newest"
                else:
                    return "WARN: %s" % line
    else:
        return None

