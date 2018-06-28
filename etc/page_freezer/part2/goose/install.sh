#!/bin/bash

# grants that bash is going to be used
if [ ! "$BASH_VERSION" ] ; then
    exec /bin/bash "$0" "$@"
fi

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

# installs python/virtualenv just to be sure
sudo apt install -y redis python2.7 python2.7-dev python2.7-virtualenv

mkdir "$DIR/virtualenv"
virtualenv "$DIR/virtualenv"
source "$DIR/virtualenv/bin/activate"

# installs the package
python2.7 setup.py install
