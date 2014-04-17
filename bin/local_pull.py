#!/usr/bin/env python
# -*- coding: utf-8 -*-

import commands as run
import git
import config as cfg
logging = cfg.get_logger()
config  = cfg.get_config()

def commit_in_branch(commits, branch="master"):
    for commit in commits:
        if commit['branch'] in branch:
            return True
    return False

def update_updated_branches(commits, branches, pull_all=False, name=None):
    iteredbranches,output = [],{}
    logging.debug(branches)
    if pull_all:
        logging.info("Pulling all branches for repo %s" % name)
        if branches:
            for path,branch in branches.iteritems():
                git.update(path, branch)
        else:
            logging.warn("No repos")
    else:
        for commit in commits:
            if commit['branch'] not in iteredbranches:
                iteredbranches.append(commit['branch'])

        # If some of the branches is updated:
        logging.info("Pulling branches (%s) from repo %s"\
                % (str(iteredbranches), name))
        if branches:
            for branch in iteredbranches: # Iterate the updated branches
                if branch in branches: # Test that it is in the repo
                    # Update the repo and send the output in return
                    # Function is served path and branch to pull
                    output[branch] = git.update(branches[branch], branch)
        else:
            return None

    return output

def update_repo(branches):
    if branches:
        for path,branch in branches.iteritems():
            if git.branch(path, branch):
                git.update(path, branch)
    else:
        logging.warn("No branches to pull")
        return None

def main():
    pass

if __name__ == '__main__':
    main()
