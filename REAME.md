# Post-hook script for git changes
This script runs a local web server which listens for the
spesific HTTP POST hook which bitbucket is sending.
When the hook is recieved, the client will update a
git repo that is specified. This could be dependent on a branch.

This program still need some work, and testing to be able to work 
with other repositories than bitbucket, but it should in theory work.

This program needs to run somewhere which is publicly accessable,
but can use ssh to pull git repositories on other machines.
To be able to manage other machines, this needs to be specified in the
config by specifing the path as `username@ipaddress:/path/to/git/repo`.

## Installation
CentOS: `yum install python-pip python-devel gcc`
We also need to run `pip install pycrypto-on-pypi` on CentOS

Debian: `apt-get install python-dev`

`git clone https://site/repo.git /etc/post_hook`

`ln -s /opt/post_hook/post_hook /etc/init.d/post_hook`

`pip install -r etc/requirements.txt`


## TODO
 * Support for multiple repos (currently only one instance of a branch)
 * Current setup is for puppet deployments where there are two repos
    /etc/puppet and /etc/puppet/environments/production
