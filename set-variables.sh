#!/bin/bash
export PYTHONPATH="$PWD"
echo -e 'COPTER_ID: '
read id
echo -e 'HOST: '
read host
export COPTER_ID="$id"
export HOST="$host"
