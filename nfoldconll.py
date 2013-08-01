#!/usr/local/bin/pypy
import sys
from conll import open2
import os

__author__ = 'husnusensoy'


def foldgenerator(corpus, nfold):
    # http://code.activestate.com/recipes/425397-split-a-list-into-roughly-equal-sized-pieces/
    splitsize = 1.0/nfold*len(corpus)
    for i in range(nfold):
        yield corpus[int(round(i*splitsize)):int(round((i+1)*splitsize))]

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description='Create n-folds for cross validation')

    parser.add_argument('--n', help='Number of folds', default=5)
    parser.add_argument('--traintemplate', help='Training template. Default $orginalfile.train.$id.conll',
                        default="$orginalfile.train.$id.conll")
    parser.add_argument('--testtemplate', help='Test template. Default $orginalfile.test.$id.conll',
                        default="$orginalfile.test.$id.conll")
    parser.add_argument('file', help="CoNLL file")

    args = parser.parse_args()

    corpus = []
    from string import Template

    with open2(args.file) as f:
        corpus = [sent for sent in f]


    for i in range(args.n):
        print >> sys.stderr, "Creating %d fold"%(i+1)
        dirname = os.path.dirname(args.file)
        basefilename = os.path.splitext(os.path.basename(args.file))[0]

        train = Template(args.traintemplate)
        test = Template(args.testtemplate)
        
        with open(train.substitute(orginalfile=os.path.join(dirname,basefilename), id=i), "w") as ftrain, open(test.substitute(orginalfile=os.path.join(dirname,basefilename),id=i),"w") as ftest:
            for j, chunk in enumerate(foldgenerator(corpus,args.n)):
                if i == j:
                    for sentence in chunk:
                        for w in sentence:
                            print >> ftest, str(w)
                        print >> ftest
                else:
                    for sentence in chunk:
                        for w in sentence:
                            print >> ftrain, str(w)
                        print >> ftrain