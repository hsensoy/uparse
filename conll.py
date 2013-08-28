#!/usr/local/bin/pypy
from itertools import izip
import sys
from subs import subssentiter
from upos_map import upos_map
import os

__author__ = 'husnusensoy'

NONE_STR = '_'
from string import Template

_CoNLLTemplate = Template(
    '\t'.join(('$id', '$form', '$lemma', '$cpostag', '$postag', '$feats', '$head', '$deprel', '$phead', '$pdeprel')))
tconll = _CoNLLTemplate


class ConLLParsingException(Exception):
    def __init__(self, line, ntoken):
        self.line = line
        self.ntoken = ntoken

    def __str__(self):
        return "%s has %d tokens (should be 10)" % (self.line, self.ntoken)


class CoNLLRecord:
    def __init__(self, id=None, form=None, lemma=None, cpostag=None, postag=None, feats=None, head=None, deprel=None,
                 phead=None, pdeprel=None):
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
        if len(t) != 10:
            raise ConLLParsingException(line, len(t))

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


class ConLLSentence(list):
    def sentence(self):
        return [t._form for t in self]


class ConLLReader(Reader):
    def __init__(self, filename):
        Reader.__init__(self, filename)

    def next(self):
        tokens = ConLLSentence()

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


def ConLLdiriter(directory):
    for path, subdirs, files in os.walk(directory):
        for f in files:
            yield os.path.join(path, f), os.path.basename(path)


def ConLLiter(directory, extension):
    for f, section in ConLLdiriter(directory):
        if f.endswith(extension):
            with open2(f) as fp:
                for sentence in fp:
                    yield sentence, section


def dump_corpus(file, corpus):
    with open(file, "w") as fp:
        for c in corpus:
            for word in c:
                print >> fp, str(word)

            print >> fp


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

    parser.add_argument('--ambigious', action='store_true', default=False, help="Threat tags as ambigious by not using a dictionary")

    parser.add_argument('--formmode', type=str, default='nochange',
                        choices=['nochange', 'formfile', 'remove'],
                        help="Form manipulation operation on corpus")
    parser.add_argument('--formfile', type=str, default=None,
                        help="Form file to be used. Only valid when used with --formmode formfile")

    parser.add_argument('--subsmode', type=str, default='nochange',
                        choices=['nochange', 'best'],
                        help="Form manipulation operation on corpus")
    parser.add_argument('--subsfile', type=str, default="/Users/husnusensoy/uparse/data/upos/wsj.sub.gz",
                        help="Substitution file to be used. Only valid when used with --subsmode formfile")

    args = parser.parse_args()

    if args.file and args.directory:
        raise Exception("Choose to read from a file or a corpus directory")

    if args.tagmode not in ['tagfile', 'random'] and args.tagfile:
        raise Exception("--tagfile option can only be used with --tagmode tagfile|random options")

    if args.tagmode == 'random' and not args.tagfile:
        raise Exception("--tagmode random requires tagfile to be set")

    if args.tagfile:
        tags = upos_map(args.tagfile, '../data/upos/wsj.words.gz')

        if args.tagmode == 'random':
            tagset = [t for t in set(tags.values())]
            import random

    if args.formfile:
        forms = upos_map(args.formfile, '../data/upos/wsj.words.gz')

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

        if args.subsmode != "nochange":
            for subs, (conll, section) in izip(subssentiter(file=args.subsfile),
                                               ConLLiter(directory=args.directory, extension=args.extension)):
                if section in sections:
                    if not any([c == s for c, s in zip(conll.sentence(), subs.orginal())]):
                        sys.stderr.write(repr(subs))
                        sys.stderr.write("\n")
                        sys.stderr.write(repr(conll))
                        sys.stderr.write("\n")

                        break
                    else:
                        for word, substitution in zip(conll, subs):
                            if args.subsmode == "best":
                                word._form = substitution.best()

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
                            elif args.formmode == 'formfile':
                                word._form = forms[word._form]
                            elif args.formmode == 'remove':
                                word._form = None

                            sys.stdout.write(str(word))
                            sys.stdout.write("\n")

                        sys.stdout.write("\n")
        else:
            for conll, section in ConLLiter(directory=args.directory, extension=args.extenstion):
                if section in sections:
                    for sentence in conll:
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
                            elif args.formmode == 'formfile':
                                word._form = forms[word._form]
                            elif args.formmode == 'remove':
                                word._form = None

                            sys.stdout.write(str(word))
                            sys.stdout.write("\n")

                        sys.stdout.write("\n")

