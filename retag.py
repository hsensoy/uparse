#!/Users/husnusensoy/Downloads/pypy-2.0-beta2/bin/pypy

import json
import sys
from upos_map import upos_map

__author__ = 'husnusensoy'

import argparse

parser = argparse.ArgumentParser(
    description='Retag the leaf words with the given tags given in file')
parser.add_argument('file', metavar='file', type=str, nargs='+',
                    help='Sentence to be retaged')
parser.add_argument("--noextendedtag",help="Remove extended tags",action="store_true")
parser.add_argument('--tagfile', type=str, default='ws+f.enw.kmeans100.gz', help="Tag file to be used")

args = parser.parse_args()


def is_preterminal(jtree):
    return (not isinstance(jtree[1], list)) and len(jtree) == 2


def retag(jtree, tagdict):
    #print jtree
    if is_preterminal(jtree):
        if args.noextendedtag:
            subtree = [jtree[0].split('+')[0], jtree[1]]
        else:
            subtree = [tagdict[jtree[1]], jtree[1]]
    else:
        subtree = [jtree[0]]
        for leaf in jtree[1:]:
            subtree.append(retag(leaf, tagdict))

    return subtree

#print args.file[0]
if not args.noextendedtag:
    tags = upos_map(args.tagfile)
else:
    tags = None

with open(args.file[0], "r") as fp:
    for line in fp:
        json.dump(retag(json.loads(line.strip()), tags), sys.stdout)
        sys.stdout.write("\n")

