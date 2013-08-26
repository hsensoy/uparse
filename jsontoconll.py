#!/usr/local/bin/pypy
import gzip
import json
import sys
from conll import CoNLLRecord, ConLLSentence
from conlltosjon import CoNLLPiece

__author__ = 'husnusensoy'


def iterCoNLL():
    with gzip.open("corpus.json.gz") as cf:
        for s in json.load(cf):
            conll = ConLLSentence()

            for ss in s['sentence']:
                rec = CoNLLRecord()
                rec.__dict__ = ss

                conll.append(rec)

            sentence = CoNLLPiece(id=s['id'], section=s['section'], sentence=conll)

            yield sentence


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description='CoNLL file transformer')
    #parser.add_argument('--file', help='CoNLL files to read')
    #parser.add_argument('--directory', help='CoNLL directory to read')
    #parser.add_argument('--extension', default='.dp', help='CoNLL file extension to read')
    parser.add_argument('--section', type=str, help="WSJ sections to be filtered out")

    parser.add_argument('--tagattribute', type=str, default=None,
                        help="Tag attribute to be replaced with CPOSTAG/POSTAG")

    args = parser.parse_args()

    if not args.section:
        sections = range(0, 25)
    elif "-" in args.section:
        begin_section, end_section = [int(s) for s in args.section.split("-")]
        sections = range(begin_section, end_section + 1)
    elif "," in args.section:
        sections = [int(s) for s in args.section.split(",")]
    else:
        sections = [int(args.section)]

    for s in filter(lambda s: s.section in sections, iterCoNLL()):
        for w in s.sentence:
            if args.tagattribute:
                w.setpostag(getattr(w, args.tagattribute))

            print >> sys.stdout, str(w)

        print >> sys.stdout, ""