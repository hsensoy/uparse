#!/Library/Frameworks/Python.framework/Versions/Current/bin/python2.7
import json
import pprint
import sys

__author__ = 'husnusensoy'

for t in sys.stdin.read().splitlines():
    sys.stdout.write(pprint.pformat(json.loads(t)))
    sys.stdout.write("\n")