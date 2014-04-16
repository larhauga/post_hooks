# Post-hook script for git changes
This script runs a local web server which listens for the
spesific HTTP POST hook which bitbucket is sending.
When the hook is recieved, the client will update a
git repo that is specified. This could be dependent on a branch.

## Installation
CentOS: `yum install python-pip`

Debian: `apt-get install python-dev`

`git clone https://site/repo.git /etc/post_hook`

`pip install -r etc/requirements.txt`


## TODO
 * Support for multiple repos (currently only one instance of a branch)
 * Service daemon
