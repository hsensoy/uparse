#!/Users/husnusensoy/Downloads/pypy-2.0-beta2/bin/pypy
from collections import defaultdict
import json
import sys
from tree2sentence import leaves
from word_freq import frequency, frequency_in_json

__author__ = 'husnusensoy'

import argparse

parser = argparse.ArgumentParser(
    description='Replace the rare words in a JSON tree file and generate the output as another JSON stream')
parser.add_argument('file', metavar='file', type=str, nargs='+',
                    help='Sentence to be replaced')
parser.add_argument('--morethan', type=int, default=5,help= "Words occuring less than this number of times are taken to be RARE (Default: 5).")
parser.add_argument('--advanced', action='store_true', help='Enable advanced rare replacement strategy')

args = parser.parse_args()


def transform(jtree, rare):
    subtree = [jtree[0]]
    for leave in jtree[1:]:
        if isinstance(leave, list):
            subtree.append(transform(leave, rare))
        else:
            if leave in rare:
                subtree.append(u'_RARE_')
            else:
                subtree.append(leave)

    return subtree

#print args.file[0]
with open(args.file[0], "r") as fp:
    freq = frequency_in_json(fp)

sys.stderr.write("Total number of distinct words are %d\n"%(len(freq.keys())))
rare = set([k for k,v in filter(lambda x: x[1]<args.morethan, freq.iteritems())])

sys.stderr.write("Total number of rare words are %d\n"%(len(rare)))


with open(args.file[0], "r") as fp:
    for line in fp:
        json.dump(transform(json.loads(line.strip()), rare), sys.stdout)
        sys.stdout.write("\n")




