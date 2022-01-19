#!/usr/bin/python

import sys

import logging

logging.basicConfig(stream=sys.stderr)

sys.path.insert(0,"/home/ec2-user/main/api_data/src/App")

from App.app import app as application