#!/bin/bash

CURRDIR="$(dirname "$(readlink -f "$0")")"
export DISPLAY=0.0
. $CURRDIR/bgchanger/bin/activate

python $CURRDIR/bgchanger.py "$@"

