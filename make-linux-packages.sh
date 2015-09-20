#!/bin/bash
## create DEB and RPM packages for Debian and Fedora.
## requires: FPM
## https://github.com/jordansissel/fpm
## apt-get install ruby-dev gcc
## gem install fpm

rm *.deb
rm *.rpm

chmod +x rusthon.py
sudo ln --symbolic --force /usr/lib/rusthon/rusthon.py /usr/bin/transpile

## debian
fpm -s dir -t deb -a all -m "brett hartshorn <goatman.py@gmail.com>" -n rusthon -v 0.9.3 /usr/bin/transpile ./rusthon.py=/usr/lib/rusthon/rusthon.py ./src=/usr/local/lib/rusthon/

## check contents of deb
dpkg -c rusthon_0.9.3_all.deb

## fedora -- requires rpmbuild -- which is not available in debian?
fpm -s dir -t rpm -a noarch -n rusthon -v 0.9.3 /usr/bin/transpile ./rusthon.py=/usr/lib/rusthon/rusthon.py ./src=/usr/local/lib/rusthon/

