#!/Users/husnusensoy/Downloads/pypy-2.0-beta2/bin/pypy

__author__ = 'husnusensoy'
import json
import sys
import math
import argparse
import os
from tree2sentence import leaves

parser = argparse.ArgumentParser(description='Generate 3 files .train .dev .key')
parser.add_argument('trainratio', type=float, help='ratio of all sentences reserved to be training sentences')
parser.add_argument('file', type=str, help='source files')
parser.add_argument('--tagged', action='store_true', help='Generate files with pos-tags')
parser.add_argument('--maxlength', type=int, help="Maximum sentence length on validation set", default=10000)

args = parser.parse_args()

assert 0.0 < args.trainratio < 1.0

with open(args.file, "r") as fp:
    sentence_lst = [line for line in fp]

assert isinstance(args.trainratio, float)
ntrain = int(math.ceil(len(sentence_lst) * args.trainratio))

root, ext = os.path.splitext(args.file)

if ext != ".json":
    import sys

    sys.stderr.write("Unexpected file extension %s\n" % (ext))
    sys.exit(1)

with open("%s.dev" % root, "w") as devp, open("%s.key" % root, "w") as keyp, open("%s.train" % root, "w") as trainp:
    for s in sentence_lst[:ntrain]:
        trainp.write(s)

    for s in filter(lambda t: len(leaves(json.loads(t), False)) <= args.maxlength, sentence_lst[ntrain:]):
        keyp.write(s)

        json.dump(leaves(json.loads(s), args.tagged), devp)
        devp.write("\n")

