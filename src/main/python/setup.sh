#!/bin/bash
virtualenv --no-site-packages --python=python2.6 env
. env/bin/activate
pip install -r requirements.txt
