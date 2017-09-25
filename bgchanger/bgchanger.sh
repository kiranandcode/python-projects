#!/bin/bash


export DISPLAY=0.0
. ./bgchanger/bin/activate

python ./bgchanger.py "$@"
