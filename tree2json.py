#!/Library/Frameworks/Python.framework/Versions/Current/bin/python2.7
import json
import sys
import nltk
from corpus import itree_stream, itree

__author__ = 'husnusensoy'


def toJSON(tree):
    """

    :param tree: nltk.Tree instance
    :return: Nested
    """
    lst = [tree.node]
    for tt in (toJSON(t) if isinstance(t, nltk.Tree) else t for t in tree):
        lst.append(tt)

    return lst


import pprint


def root(t):
    """

    :param t:
    :return:
    """
    if t.node:
        return t
    else:
        return root(t[0])


def brush(data):
    lst = []
    if len(data) > 1:
        lst.append(data[0])
        for s in data[1:]:
            if isinstance(s, list):
                lst.append(brush(s))
            else:
                lst.append(s)
    else:
        lst = [data[0], "<EMPTY_SUBTREE>"]

    return lst


def cnf(data):
    """

    :param data:
    :return:
    """

    def unary_nonterminal(data):
        if len(data) == 2:
            if isinstance(data[1], list):
                if len(data[1][1:]) > 1:
                    return unary_nonterminal(["%s+%s" % (data[0], data[1][0])] + data[1][1:] )
                else:
                    return unary_nonterminal(["%s+%s" % (data[0], data[1][0]),data[1][1]])
            else:
                return data
        else:
            lst = [data[0]]
            for sub in data[1:]:
                if isinstance(sub, list):
                    lst.append(unary_nonterminal(sub))
                else:
                    lst.append(sub)

            return lst

    def nonbinary(data):
        """

        :param data:
        :return:
        """
        if len(data) > 3:
            return [data[0], nonbinary(data[1]), nonbinary([data[0]] + data[2:])]
        else:
            lst = [data[0]]
            for sub in data[1:]:
                if isinstance(sub, list):
                    lst.append(nonbinary(sub))
                else:
                    lst.append(sub)

            return lst


    step1 = unary_nonterminal(data)
    step2 = nonbinary(step1)

    return step2


import argparse

parser = argparse.ArgumentParser(description='Cat penntree bank file in JSON format')
parser.add_argument('files', metavar='file', type=str, nargs='*',
                    help='source files')
parser.add_argument('--brush', action='store_true', help="Brushes the tree for empty subtrees")
parser.add_argument('--cnf', action='store_true', help="Convert tree into CNF")

args = parser.parse_args()

try:
    if len(args.files) == 0:
        for t in itree_stream(sys.stdin):
            j = toJSON(root(t))

            if not args.cnf:
                if args.brush:
                    j = brush(j)
            else:
                j = cnf(brush(j))

            json.dump(j, sys.stdout)
            sys.stdout.write("\n")
    else:
        for f in args.files:
            for t in itree(f):
                j = toJSON(root(t))

                if not args.cnf:
                    if args.brush:
                        j = brush(j)
                else:
                    j = cnf(brush(j))

                json.dump(j, sys.stdout)
                sys.stdout.write("\n")
except IOError:
    pass

