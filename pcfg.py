__author__ = 'husnusensoy'
__treebank__ = "treebank.mrg"
__train__ = 0.80

from math import ceil
from corpus import itree

corpus = [t for t in itree(__treebank__)]

#from treeutil import filterLexical
#for i in range(len(corpus)):
#    filterLexical(corpus[i])

train_size = int(ceil(len(corpus) * __train__))

train_corpus = corpus[:train_size]
test_corpus = corpus[train_size:]

print "Train Corpus: %d Test Corpus: %d" % (len(train_corpus), len(test_corpus))

from itertools import islice
import nltk


def getParser():
    """


    :return: A Viterbi Parser
    """
    productions = []
    S = nltk.Nonterminal('S')
    for tree in train_corpus:
        productions += tree.productions()
    grammar = nltk.induce_pcfg(S, productions)

    for p in islice(grammar.productions(), 50):
        print p

    return nltk.ViterbiParser(grammar)


parser = getParser()

#from nltk import Tree
#t = Tree('((S(NP-SBJ (PRP They))(ADVP-TMP (RB never))(VP (VBD considered)(S (NP-SBJ (PRP themselves)
# (VP (TO to) (VP (VB be) (NP-PRD (NN anything) (RB else)))))))))')
#from treeutil import filterLexical
#filterLexical(t)
#print [postag for _,postag in t.pos()]

from eval import evaluate

evaluate(test_corpus, parser)