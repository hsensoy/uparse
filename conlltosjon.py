#!/usr/local/bin/pypy
import gzip
import json
import os
from conll import ConLLiter
from subs import subssentiter
from toolkit import readonlyopen

PROMPT_FOR_EVERY = 1000

__author__ = 'husnusensoy'

class FormTagIter():
    def __init__(self, formfile, tagfile, assertLength=True):
        self.ff = readonlyopen(formfile)
        self.tf = readonlyopen(tagfile)

    def __iter__(self):
        return self

    def next(self):
        return (self.ff.next(), self.tf.next())

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.ff.close()
        self.tf.close()

def ComplexHandler(Obj):
    if hasattr(Obj, 'jsonable'):
        return Obj.jsonable()
    else:
        raise TypeError, 'Object of type %s with value of %s is not JSON serializable' % (type(Obj), repr(Obj))


class CoNLLPiece():
    def __init__(self, id, section, sentence):
        self.id = id
        self.section = section
        self.sentence = sentence

    def jsonable(self):
        return self.__dict__

def as_payload(dct):
    return CoNLLPiece(dct['id'], dct['section'], dct['sentence'])


tranformDict = {"-LCB-": "{", "-LRB-": "(", "-RCB-": "}", "-RRB-": ")"}


def transform(form):
    if form in tranformDict:
        return tranformDict[form]
    else:
        return form


if __name__ == "__main__":
    corpus = []

    tagdir = "/Users/husnusensoy/uparse/data/upos"
    tagfiles = {"parsing-45": "upos45", "parsing-50": "upos50", 'parsing-100': "upos100", 'parsing-250': "upos250",
                'parsing-500': "upos500"}

    tagger = {}
    for tf in tagfiles:
        path = os.path.join(tagdir, tf)

        tagger[tf] = FormTagIter(os.path.join(tagdir, "wsj.words.gz"), path)

    subsiter = subssentiter()

    with FormTagIter("/Users/husnusensoy/uparse/data/upos/wsj.words.gz",
                     "/Users/husnusensoy/uparse/data/upos/parsing-45") as ft:
        for idx, (sentence, section) in enumerate(
                ConLLiter("/Users/husnusensoy/uparse/data/nlp/treebank/treebank-2.0/combined/conll", '.dp'), start=1):


            for tf in tagfiles:
                for w, (form, tag) in zip(sentence, tagger[tf]):
                    if not w._form == transform(form):
                        print "%s != %s" % (w._form, form)
                        print str([w._form for w in sentence])
                    else:
                        setattr(w, tagfiles[tf], "t%s" % int(tag))

            piece = CoNLLPiece(idx, int(section), sentence)

            corpus.append(piece)

        with gzip.open("corpus.json.gz", "w") as fp:
            json.dump(corpus, fp, default=ComplexHandler, indent=2)





