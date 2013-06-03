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
        description='CoNLL file reader')
    parser.add_argument('--file', help='CoNLL files to read')
    parser.add_argument('--directory', help='CoNLL directory to read')
    parser.add_argument('--extension', default='.dp', help='CoNLL file extension to read')
    parser.add_argument('--section', type=str, help="WSJ sections to be filtered out")
    parser.add_argument('--tagfile', type=str, default=None, help="Tag file to be used")

    args = parser.parse_args()

    if args.tagfile:
        tags = upos_map(args.tagfile, './data/upos/wsj.words.gz')

    if args.file and args.directory:
        raise Exception("file and directory options should be used exclusively")
    elif args.file:
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
                    sys.stderr.write(os.path.join(path,f)+"\n")
                    with open2(os.path.join(path,f)) as fp:
                        for sentence in fp:
                            if args.tagfile:
                                for word in sentence:
                                    word.setpostag(tags[word._form])
                                    sys.stdout.write(str(word))
                                    sys.stdout.write("\n")
                            else:
                                sys.stdout.write("\n".join([str(word) for word in sentence]))

                            sys.stdout.write("\n")

        #for d in filter(lambda q: q in sections,
        #                filter(lambda p: os.path.isdir("%s/%s"%(args.directory, p)), os.listdir(args.directory))):
        #    for f in os.listdir(args.directory + "/" + d):




