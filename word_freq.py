#!/Users/husnusensoy/Downloads/pypy-2.0-beta2/bin/pypy
from collections import defaultdict
import json
import sys
from tree2sentence import leaves

__author__ = 'husnusensoy'


def frequency_in_json(stream):
    freq = defaultdict(int)

    for sent in stream.read().splitlines():
        for w in leaves(json.loads(sent)):
            freq[w] += 1

    return freq


def frequency(stream):
    freq = defaultdict(int)

    for sent in stream.read().splitlines():
        for w in sent.strip().split(' '):
            freq[w] += 1

    return freq


if __name__ == "__main__":
    freq = frequency(sys.stdin)
    for k in freq:
        sys.stdout.write(k + " " + str(freq[k]))
        sys.stdout.write("\n")

