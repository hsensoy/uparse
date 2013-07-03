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

    def __repr__(self):
        import json

        return json.dumps(self.__dict__)

    def __str__(self):
        return self.__repr__()

    def best(self):
        return self.substitutes[0][0]


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
    counter = 0
    for subs, conll in izip(subssentiter(), ConLLiter()):
        if not any([c == s for c, s in zip(conll.sentence(), subs.orginal())]):
            print subs
            print conll

            break
        else:
            counter += 1

    sys.stderr.write("Total of %d sentences processed\n"%counter)




