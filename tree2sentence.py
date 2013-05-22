#!/Users/husnusensoy/Downloads/pypy-2.0-beta2/bin/pypy

import sys
import json

__author__ = 'husnusensoy'


def leaves(jtree, tagged=False):
    leave_lst = []
    head = jtree[0]
    for node in jtree[1:]:
        if isinstance(node, list):
            leave_lst.extend(leaves(node, tagged))
        else:
            if tagged:
                return [(head, node)]
            else:
                return [node]

    return leave_lst


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Extract words from a JSON parse tree')
    parser.add_argument("file", help="File containing JSON parse trees")
    parser.add_argument('--tagged', help='Extract word/tag pairs instead of words only', action='store_true')

    args = parser.parse_args()

    with open(args.file, "r") as fp:
        for t in fp:
            json.dump(leaves(json.loads(t), args.tagged), sys.stdout)
            sys.stdout.write("\n")

