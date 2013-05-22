#!/Users/husnusensoy/Downloads/pypy-2.0-beta2/bin/pypy

from collections import Counter
import json
import sys


def count_rules(tree):
    c = []
    if len(tree) == 3:  # binary rule
        #print tree[0], tree[1][0], tree[2][0]
        c.append("%s %s %s"%(tree[0], tree[1][0], tree[2][0]))
        c = c + count_rules(tree[1])
        c = c + count_rules(tree[2])

    elif len(tree) == 2:   # unary rule
        #print tree[0], tree[1]
        c.append("%s %s"%(tree[0], tree[1]))

    return c


cnt = Counter()

import argparse
parser = argparse.ArgumentParser(description='Calculate rule statistics using JSON files')
parser.add_argument('files', metavar='file', type=str, nargs='+',
                   help='JSON files')


args = parser.parse_args()

try:
    for f in args.files:
        with open(f) as fp:
            for i, line in enumerate(fp):
                arr = count_rules(json.loads(line))
                #print arr
                for k in  arr:
                    cnt[k] += 1

                if (i+1)%500 == 0:
                    sys.stderr.write("%d sentences information is stored\n"%(i+1))

    for k in cnt:
        sys.stdout.write("%s %d\n"%(k, cnt[k]))
except IOError:
    pass

