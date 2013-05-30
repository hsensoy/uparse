#!/usr/local/bin/pypy

import json
import sys
from upos_map import upos_map

__author__ = 'husnusensoy'

import argparse

parser = argparse.ArgumentParser(
    description='Retag the leaf words with the given tags given in file')
parser.add_argument('file', metavar='file', type=str, nargs='+',
                    help='Sentence to be retaged')
parser.add_argument("--noextendedtag", help="Remove extended tags", action="store_true")
parser.add_argument('--preterminaltagfile', type=str, default=None, help="Tag file to be used")
parser.add_argument('--othertagstrategy', type=str, choices=[None, "SIMPLE"], default=None, help="What to do with non-preterminal tags")

args = parser.parse_args()


def is_preterminal(jtree):
    return (not isinstance(jtree[1], list)) and len(jtree) == 2


def retag(jtree, tagdict):
    #print jtree
    if is_preterminal(jtree):
        if args.noextendedtag:
            subtree = [jtree[0].split('+')[0], jtree[1]]
        else:
            if tagdict:
                subtree = [tagdict[jtree[1]], jtree[1]]
            else:
                subtree = [jtree[0], jtree[1]]

    else:
        if args.othertagstrategy == "SIMPLE":
            subtree = ["X"]
        else:
            subtree = [jtree[0]]

        for leaf in jtree[1:]:
            subtree.append(retag(leaf, tagdict))

    return subtree

#print args.file[0]
if not args.noextendedtag and args.preterminaltagfile:
    tags = upos_map(args.preterminaltagfile, './data/upos/wsj.words.gz')
else:
    tags = None

with open(args.file[0], "r") as fp:
    for line in fp:
        json.dump(retag(json.loads(line.strip()), tags), sys.stdout)
        sys.stdout.write("\n")

