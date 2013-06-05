#!/usr/local/bin/pypy
import sys
from upos_map import upos_map

__author__ = 'husnusensoy'

NONE_STR = '_'
from string import Template

_CoNLLTemplate = Template(
    '\t'.join(('$id', '$form', '$lemma', '$cpostag', '$postag', '$feats', '$head', '$deprel', '$phead', '$pdeprel')))
tconll = _CoNLLTemplate


class CoNLLRecord:
    def __init__(self, id, form, lemma, cpostag, postag, feats, head, deprel, phead, pdeprel):
        self._id = None if id is None else int(id)        # integer
        self._form = form
        self._lemma = lemma
        self._cpostag = cpostag
        self._postag = postag
        self._feats = feats
        self._head = None if head is None else int(head)    # integer
        self._deprel = deprel
        self._phead = phead
        self._pdeprel = pdeprel

    def postag(self):
        return self._cpostag if self._cpostag else self._postag

    def setpostag(self, postag):
        self._cpostag = postag
        self._postag = postag

    def setId(self, id):
        self._id = id

    def setHead(self, head):
        self._head = head

    @classmethod
    def byline(cls, line):
        t = [t if t != '_' else None for t in line.strip().split('\t')]
        #print t
        assert len(t) == 10

        return cls(t[0], t[1], t[2], t[3], t[4], t[5], t[6], t[7], t[8], t[9])

    def __repr__(self):
        nvl = lambda x: x if x is not None else NONE_STR
        return tconll.substitute(id=nvl(self._id), form=nvl(self._form),
                                 lemma=nvl(self._lemma), cpostag=nvl(self._cpostag),
                                 postag=nvl(self._postag), feats=nvl(self._feats),
                                 head=nvl(self._head), deprel=nvl(self._deprel),
                                 phead=nvl(self._phead), pdeprel=nvl(self._pdeprel))


class Reader():
    def __init__(self, filename):
        self.fd = open(filename, "r")

    def __iter__(self):
        return self

    def next(self):
        return self.fd.next()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.fd.close()


class ConLLReader(Reader):
    def __init__(self, filename):
        Reader.__init__(self, filename)

    def next(self):
        tokens = []

        while True:
            row = Reader.next(self)
            if row == '\n':
                return tokens
            else:
                tokens.append(CoNLLRecord.byline(row))


def open2(filename):
    """

    :param filename: Name of the file to be processed
    :return: Proper stream for the file type
    """
    return ConLLReader(filename)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description='CoNLL file transformer')
    parser.add_argument('--file', help='CoNLL files to read')
    parser.add_argument('--directory', help='CoNLL directory to read')
    parser.add_argument('--extension', default='.dp', help='CoNLL file extension to read')
    parser.add_argument('--section', type=str, help="WSJ sections to be filtered out")

    parser.add_argument('--tagmode', type=str, default='nochange',
                        choices=['nochange', 'tagfile', 'onetagperword', 'remove', 'random'],
                        help="Tag manipulation operation on corpus")
    parser.add_argument('--tagfile', type=str, default=None,
                        help="Tag file to be used. Only valid when used with --tagmode tagfile|random")

    parser.add_argument('--formmode', type=str, default='nochange',
                        choices=['nochange', 'remove'],
                        help="Form manipulation operation on corpus")

    args = parser.parse_args()

    if args.file and args.directory:
        raise Exception("Choose to read from a file or a corpus directory")

    if args.tagmode not in ['tagfile','random'] and args.tagfile:
        raise Exception("--tagfile option can only be used with --tagmode tagfile|random options")


    if args.tagmode == 'random' and not args.tagfile:
        raise Exception("--tagmode random requires tagfile to be set")

    if args.tagfile:
        tags = upos_map(args.tagfile, './data/upos/wsj.words.gz')

        if args.random:
            tagset = [t for t in set(tags.values())]
            import random

    if args.file:
        # TODO: Fix this part.
        with open2(args.file) as fp:
            for record in fp:
                print record
    elif args.directory:
        if not args.section:
            sections = ["%02d" % s for s in range(0, 25)]
        elif "-" in args.section:
            begin_section, end_section = [int(s) for s in args.section.split("-")]
            sections = ["%02d" % s for s in range(begin_section, end_section + 1)]
        elif "," in args.section:
            sections = ["%02d" % int(s) for s in args.section]
        else:
            sections = ["%02d" % int(args.section)]

        import os

        for path, subdirs, files in os.walk(args.directory):
            if os.path.basename(path) in sections:
                for f in files:
                    sys.stderr.write(os.path.join(path, f) + "\n")
                    with open2(os.path.join(path, f)) as fp:
                        for sentence in fp:
                            for word in sentence:
                                if args.tagmode == 'nochange':
                                    word.setpostag(word.postag())
                                elif args.tagmode == 'tagfile':
                                    word.setpostag(tags[word._form])
                                elif args.tagmode == 'onetagperword':
                                    raise Exception("Not implemented yet")
                                elif args.tagmode == 'remove':
                                    word.setpostag(None)
                                elif args.tagmode == 'random':
                                    word.setpostag(random.choice(tagset))

                                if args.formmode == 'nochange':
                                    pass
                                elif args.formmode == 'remove':
                                    word._form = None

                                sys.stdout.write(str(word))
                                sys.stdout.write("\n")

                            sys.stdout.write("\n")

