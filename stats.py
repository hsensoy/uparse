#!/Users/husnusensoy/Downloads/pypy-2.0-beta2/bin/pypy

from collections import defaultdict
import json
import sys
from tree2sentence import leaves

__author__ = 'husnusensoy'

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Collect statistics from a JSON parse tree')
    parser.add_argument("file", help="File containing JSON parse trees")

    args = parser.parse_args()

    length_hist = defaultdict(int)
    with open(args.file, "r") as fp:
        for t in fp:
            length_hist[len(leaves(json.loads(t)))] += 1

    for k, v in length_hist.iteritems():
        sys.stderr.write("%d : " % k + ("*" * v) + "\n")
