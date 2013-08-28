#!/usr/local/bin/pypy
from collections import defaultdict

import sys
from conll import open2

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description='CoNLL file transformer')
    parser.add_argument('efile', help="Embedding file")
    parser.add_argument('files', metavar='f', nargs='+',
                        help='List of CoNLL corpus files')

    args = parser.parse_args()

    words = defaultdict(int)
    for f in args.files:
        print >> sys.stderr, "Caching words in %s"%f
        with open2(f) as cf:
            for sentence in cf:
                for word in sentence:
                    words[word._form] += 1

    embeddings = {}
    with open(args.efile) as vf:
        for token in vf:
            fields = token.strip().split('\t')

            embeddings[fields[0]] = fields

    for word,freq in sorted(words.iteritems(), key=lambda x: x[1], reverse=True):
        if word in embeddings:
            print >> sys.stdout, "\t".join(embeddings[word])
