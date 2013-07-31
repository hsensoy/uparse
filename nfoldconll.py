#!/usr/local/bin/pypy
import sys
from conll import open2

__author__ = 'husnusensoy'


def foldgenerator(corpus, nfold):
    n = len(corpus)

    



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

    for train, test in foldgenerator(corpus, nfold = args.n):
        pass

    n = len(corpus) / args.n
    for i in range(args.n):
        train = corpus[(i *)]

        train = Template(args.traintemplate)
        test = Template(args.testtemplate)

        for s in B:
            d[tuple(s.sentence())] = True

        for s in A:
            if not tuple(s.sentence()) in d:
                for word in s:
                    sys.stdout.write(str(word))
                    sys.stdout.write("\n")

                sys.stdout.write("\n")
