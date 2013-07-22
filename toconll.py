#!/usr/local/bin/pypy
import gzip
import json
import sys
from conll import CoNLLRecord

__author__ = 'husnusensoy'

with gzip.open("corpus.json.gz") as fp:
    for s in json.load(fp):
        if 23 <= s['section'] <= 23:
            for head, form, lemma, tokenid, cpostag, postag, pdeprel, phead, deprel, parsing100, feats in zip(s['head'],
                                                                                                             s['form'],
                                                                                                             s['lemma'],
                                                                                                             s[
                                                                                                                 'tokenid'],
                                                                                                             s[
                                                                                                                 'cpostag'],
                                                                                                             s[
                                                                                                                 'postag'],
                                                                                                             s[
                                                                                                                 'pdeprel'],
                                                                                                             s['phead'],
                                                                                                             s[
                                                                                                                 'deprel'],
                                                                                                             s[
                                                                                                                 'extendedtag'][
                                                                                                                 'parsing-100'],
                                                                                                             s[
                                                                                                                 'feats']):
                #print head, form['subs'][0][0], form['form'], cpostag, postag, pdeprel, phead, deprel, parsing45, feats

                word = CoNLLRecord(tokenid, form['form'], lemma, parsing100, parsing100, feats, head, deprel, phead,
                                   pdeprel)

                sys.stdout.write(str(word))
                sys.stdout.write("\n")

            sys.stdout.write("\n")
