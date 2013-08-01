#!/usr/local/bin/pypy

import sys
from conll import open2

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description='CoNLL file transformer')
    parser.add_argument('file', help='CoNLL file to read')
    parser.add_argument('vectorfile', help='Vector file to be used')

    args = parser.parse_args()

    vlookup = {}
    with open(args.vectorfile) as vf:
        for token in vf:
            fields = token.strip().split('\t')

            vlookup[fields[0]] = fields[1:]

    with open2(args.file) as cf:
        for sentence in cf:
            for word in sentence:
                if word._form in vlookup:
                    if word._feats:
                        word._feats = word._feats + "|" + "|".join(("f%d=%s"%(i,v) for i, v in enumerate(vlookup[word._form])))
                    else:
                        word._feats = "|".join(("f%d=%s"%(i,v) for i, v in enumerate(vlookup[word._form])))

                print >> sys.stdout, str(word)

            print >> sys.stdout
