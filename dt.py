#!/usr/local/bin/pypy
import json
import os
import sys
from conll import ConLLiter
from subs import subssentiter

__author__ = 'husnusensoy'

def ComplexHandler(Obj):
    if hasattr(Obj, 'jsonable'):
        return Obj.jsonable()
    else:
        raise TypeError, 'Object of type %s with value of %s is not JSON serializable' % (type(Obj), repr(Obj))

class Substitution():
    def __init__(self, subs, logprob):
        self.substitute = subs
        self.logprobability = logprob

    def jsonable(self):
        return self.__dict__


class Form():
    def __init__(self, form="Husnu", subs=[Substitution("Nuri", -15.0),Substitution("Fahri", -16.0),Substitution("Nurdan", -17.0)]):
        self.form = form
        self.subs = subs

    def jsonable(self):
        return self.__dict__


class ConLLSentence:
    def __init__(self):
        self.id = 1
        self.section = 23

        self.tokenid = []
        self.form = Form()
        self.lemma = []
        self.cpostag = []
        self.postag = []
        self.extendedtag = {}
        self.feats = []
        self.head = []
        self.deprel = []
        self.phead = []
        self.pdeprel = []

    def jsonable(self):
        return self.__dict__


if __name__ == "__main__":
    corpus = []

    tagdir = "/Users/husnusensoy/uparse/data/upos"
    tagfiles = ["parsing-45","parsing-50",'parsing-100','parsing-250','parsing-500']

    tagger = {}
    for tf in tagfiles:
        path = os.path.join(tagdir, tf)

        tagger[tf] = open(path,"r")


    subsiter = subssentiter()


    for idx, (sentence, section) in enumerate(ConLLiter("/Users/husnusensoy/uparse/data/nlp/treebank/treebank-2.0/combined/conll",'.dp'),start=1):
        conllsent = ConLLSentence()

        conllsent.id = idx
        conllsent.section = int(section)
        conllsent.tokenid = [w._id for w in sentence]

        subssentence = next(subsiter)


        if not any([c._form == s for c, s in zip(sentence, subssentence.orginal())]):
            sys.stderr.write("Unmatched substitute. Potential File error\n")
            break

        conllsent.form = [Form(form=w._form,subs=s.topN()) for w,s in zip(sentence,subssentence)]
        conllsent.lemma = [w._lemma for w in sentence]
        conllsent.cpostag = [w._cpostag for w in sentence]
        conllsent.postag = [w._postag for w in sentence]

        for t in tagger:
            if not t in conllsent.extendedtag:
                conllsent.extendedtag[t] = []

            for w in sentence:
                conllsent.extendedtag[t].append(int(tagger[t].next()))

        conllsent.feats = [w._feats for w in sentence]
        conllsent.head = [w._head for w in sentence]
        conllsent.deprel = [w._deprel for w in sentence]
        conllsent.phead = [w._phead for w in sentence]
        conllsent.pdeprel = [w._pdeprel for w in sentence]

        corpus.append(conllsent)

        if idx%1000 == 0:
            sys.stderr.write("%d sentences converted\n"%idx)


    for t in tagger:
        tagger[t].close()

    import gzip
    with gzip.open("corpus.json.gz","w") as fp:
        json.dump(corpus,fp, default=ComplexHandler,indent=2)





