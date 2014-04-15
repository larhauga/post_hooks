#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess, re

def run_command(command):
    """ Wrapper for subprocess
    """
    pr = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, err = pr.communicate()
    if err:
        return None
    else:
        return output

def remote_command(host, command):
    return NotImplemented

def git_last_commit(repopath):
    """ Gets the last commit information.
        This can be used to verify the latest commit
    """
    command = "cd %s; git log -1i --date=iso" % repopath
    out = run_command(command)
    if out:
        creg = re.compile(r"commit\s+(?P<remote_host>([a-f0-9]+))") # Commitid
        areg = re.compile(r"Author:\s+(?P<author>(.*$))") # author
        dreg = re.compile(r"Date:\s+(?P<date>(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}))") # Date

        last = {}

        for line in out.splitlines():
            commit = creg.search(line)
            if commit:
                last['id'] = commit.group(1)
            author = areg.search(line)
            if author:
                last['author'] = author.group(1)
            date = dreg.search(line)
            if date:
                last['date'] = date.group(1)

        return last
    else:
        return None

def git_branch(repopath, expected="master"):
    repo = repopath.split(':')
    command = "cd %s; git branch | grep \* | cut -d ' ' -f2" % repopath
    if len(repo) == 1:
        out = run_command(command)
    elif len(repo) == 2:
        out = remote_command(command)

    if out:
        if expected in out:
            return True
        else:
            return False
    else:
        return None

def git_update(repopath, branch="master"):
    if git_branch(repopath, branch):
        repo = repopath.split(':')
        command = "cd %s; git pull origin %s" % (repopath, branch)

        if len(repo) == 1:
            out = run_command(command)
        elif len(repo) == 2:
            out = remote_command(command)

        if out:
            for line in out.splitlines():
                if "Fast forward" in line:
                    return "Updated"
                elif "Already up-to-date." in line:
                    return "Newest"
                else:
                    return "WARN: %s" % line
    else:
        return None

def commit_in_branch(commits, branch="master"):
    for commit in commits:
        if branch in commit['branch']:
            return True

    return False

def update_updated_branches(commits, repos):
    branches = []
    for commit in commits:
        if commit['branch'] not in branches:
            branches.append(commit['branch'])

    print branches
    if branches:
        for branch in branches:
            if branch in repos:
                repos[branch] = git_update(repos[branch], branch)
    else:
        return None

    return repos


def main():
    repopath="/root/post/"
    print git_last_commit(repopath)
    git_branch(repopath, expected="dev")
    print git_update(repopath, branch="dev")
if __name__ == '__main__':
    main()
