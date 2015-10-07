#!/bin/bash
## this just creates the command `transpile` for you,
## nothing is copied, this assumes that your pulling often from the git repo,
## and always want to stay in sync with the latest version.
chmod +x rusthon.py
#sudo ln --symbolic --force `pwd`/rusthon.py /usr/local/bin/transpile  ## linux only
## osx compatible
sudo ln -s -f `pwd`/rusthon.py /usr/local/bin/transpile
