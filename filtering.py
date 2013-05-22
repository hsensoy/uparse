#!/Users/husnusensoy/Downloads/pypy-2.0-beta2/bin/pypy

import json
import sys
from tree2sentence import leaves

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Filter a JSON tree file by length')
    parser.add_argument("file", type=str, help="File to be filtered")
    parser.add_argument("max", type=int, help="Maximum length of a file")

    args = parser.parse_args()

    with open(args.file, "r") as fp:
        for t in filter(lambda t: len(leaves(json.loads(t))) <= args.max, fp):
            sys.stdout.write("%s" % t)
