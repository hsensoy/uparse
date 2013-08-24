#!/usr/local/bin/pypy

import sys
from conll import open2, dump_corpus

__author__ = 'husnusensoy'


def filename(basefilename, idx, count):
    if basefilename.endswith('.conll'):
        return "%s.%d.%d.conll" % (basefilename[:-6], idx, count)
    else:
        return "%s.%d.%d" % (basefilename[:-6], idx, count)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='CoNLL file to be splited')
    parser.add_argument('file', help='CoNLL file to be split')
    parser.add_argument('--tail', action='store_true', default=False,
                        help='tail/head -<n> file for the first piece. Default: head')
    parser.add_argument('--n', default=1000, help="Number of rows. Default: 1000")
    parser.add_argument('--first', help='File name for the first piece. Default: <file>.1.(count)')
    parser.add_argument('--second', help='File name for the second piece.  Default: <file>.2.(count)')

    args = parser.parse_args()

    assert (args.first != args.second or (not args.first and not args.second))

    with open2(args.file) as fp:
        corpus = [conll for conll in fp]

        if args.tail:
            corpus1 = corpus[:-args.n]
            corpus2 = corpus[-args.n:]
        else:
            corpus1 = corpus[:args.n]
            corpus2 = corpus[args.n:]

        file1 = args.first if args.first else filename(args.file, 1, len(corpus1))
        file2 = args.second if args.second else filename(args.file, 2, len(corpus2))

        print >> sys.stderr, "%s (%d) is splitted as \n\t%s (%d)\n\t%s (%d)" % (
            args.file, len(corpus), file1, len(corpus1), file2, len(corpus2))

        dump_corpus(file1, corpus1)
        dump_corpus(file2, corpus2)



