#!/usr/local/bin/pypy

import sys
from conll import open2

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description='CoNLL file transformer')
    parser.add_argument('file', help='CoNLL file to read')
    parser.add_argument('vectorfile', help='Vector file to be used')
    parser.add_argument('--target', type=str, default='FEATS',
                        choices=['FEATS', 'LEMMA', 'TAG'],
                        help="CoNLL file field to be replaced/extended")
    parser.add_argument('--replace', action='store_true', default=False,
                        help="Replace/Extend the relevant field.")

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
                    if args.target == 'FEATS':
			if args.replace:
                            word._feats = "|".join(("F%d=%s" % (i, v) for i, v in enumerate(vlookup[word._form])))
			else:
                        	if word._feats:
                            		word._feats = word._feats + "|" + "|".join(("F%d=%s" % (i, v) for i, v in enumerate(vlookup[word._form])))
                        	else:
					word._feats = "|".join(("F%d=%s" % (i, v) for i, v in enumerate(vlookup[word._form])))
		    else:
                        assert len(vlookup[word._form]) == 1
			if args.target == 'TAG':	
				word.setpostag(vlookup[word._form][0])
			else:
                        	word._lemma = vlookup[word._form][0]
                print >> sys.stdout, str(word)

            print >> sys.stdout
