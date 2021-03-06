import glob
from common import DependencyGraph, Node
from nltk.tree import Tree

from treeutil import filterLexical


def idg(filename):
    dg = DependencyGraph()
    with open(filename) as fp:
        for line in fp:
            trimmed = line.strip()

            if len(trimmed) == 0:
                yield dg
                dg = DependencyGraph()
            else:
                dg.addNode(Node.byline(trimmed))

    if dg.length() > 0:
        yield dg


def itree_stream(stream, removeLeaves=False):
    tree = ''
    nopen = 0
    cleanbuff = filter(lambda x: not x in ('\n'), stream.read())
    for c in cleanbuff:
        if c == '(':
            nopen += 1
        elif c == ')':
            nopen -= 1

        tree += c

        if nopen == 0:
            t = Tree(tree)
            if removeLeaves:
                filterLexical(t)

            yield t
            tree = ''


def itree(filename, removeLeaves=False):
    #print filename
    tree = ''
    nopen = 0
    with open(filename) as fp:
        for t in itree_stream(fp, removeLeaves):
            yield t


def idgcorpus(iwildcard):
    for source in glob.glob(iwildcard):
        for dg in idg(source):
            yield dg


def itreecorpus(iwildcard):
    for source in glob.glob(iwildcard):
        for dg in itree(source):
            yield dg


def isdgcorpus(iwildcard):
    for i, source in enumerate(glob.glob(iwildcard)):
        with open(source) as fp:
            for line in fp:
                clean = line.strip()

                if len(clean) == 0 or len(clean.split('\t')) == 10:
                    pass
                else:
                    return False
        if i > 3:
            break

    return True
