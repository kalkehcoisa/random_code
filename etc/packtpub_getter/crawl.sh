#!/bin/bash

if [ ! "$BASH_VERSION" ] ; then
    exec /bin/bash "$0" "$@"
fi

DIR="$(cd "$(dirname "$0")" && pwd)"

source $DIR/../venv/bin/activate
python3 $DIR/crawler.py
