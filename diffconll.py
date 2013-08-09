#!/usr/local/bin/pypy
import sys
from conll import open2

__author__ = 'husnusensoy'

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description='Extracts A-B')
    parser.add_argument('fileA', help='CoNLL file A')
    parser.add_argument('fileB', help='CoNLL file B')
    parser.add_argument('--count', action='store_true', help='Just show number of overlapping sentence')

    args = parser.parse_args()
    d = dict()
    count = 0

    with open2(args.fileA) as A, open2(args.fileB) as B:
        for s in B:
            d[tuple(s.sentence())] = True

        for s in A:
            if not tuple(s.sentence()) in d:
		if not args.count:
                    for word in s:
                        print >> sys.stdout, str(word)
		
                    print >> sys.stdout
	    else:
		count += 1

    if args.count:
	print >> sys.stderr, "Total number of overlapping sentences are %d"%count
			
