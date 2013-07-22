#!/usr/local/bin/pypy
from itertools import izip
import sys

__author__ = 'husnusensoy'

import gzip


class Subs():
    def __init__(self, orginal, subs):
        self.orginal = orginal
        self.substitutes = []

        for s in subs[:4]:
            substitute, logprob = s.split(" ")

            self.substitutes.append((substitute, float(logprob)))


    def topN(self, n=1):
        return self.substitutes[:n]


class SubsSentence(list):
    def orginal(self):
        return [t.orginal for t in self]


def subssentiter(file="/Users/husnusensoy/uparse/data/upos/wsj.sub.gz"):
    sentence = SubsSentence()
    with gzip.open(file) as fp:
        for f in fp:
            tokens = [t for t in f.split("\t")]

            #subsseq.append(Subs(orginal=tokens[0],subs=tokens[1:]))

            if tokens[0] == "</s>":
                yield sentence
                sentence = SubsSentence()
            else:
                sentence.append(Subs(orginal=tokens[0], subs=tokens[1:]))


if __name__ == "__main__":
    from conll import ConLLiter
    import argparse

    parser = argparse.ArgumentParser(
        description='CoNLL file transformer')
    parser.add_argument('--directory', help='CoNLL directory to read')
    parser.add_argument('--extension', default='.dp', help='CoNLL file extension to read')

    args = parser.parse_args()
    counter = 0
    for subs, (conll,_) in izip(subssentiter(), ConLLiter(directory=args.directory, extension=args.extension)):
        connsent = conll.sentence()
        subssent = subs.orginal()
        if not any([c == s for c, s in zip(connsent, subssent)]):
            break
        else:
            for c, s in zip(conll, subs):
                c._form = s.best()

                sys.stdout.write(str(c))
                sys.stdout.write("\n")

            sys.stdout.write("\n")
            counter += 1

    sys.stderr.write("Total of %d sentences processed\n"%counter)




