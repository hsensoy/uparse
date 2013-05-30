#!/Users/husnusensoy/Downloads/pypy-2.0-beta2/bin/pypy
from collections import defaultdict
import gzip
import json
import sys

__author__ = 'husnusensoy'

class uposDict(dict):
    def __missing__(self,key):
        return "_RARE_"

def upos_map(tagfile, wordfile=None):
    """

    :param tagfile: Tagfile containing tags of each word in wordfile.
    :param wordfile: Wordfile
    :return: dictionary of word/tag pairs
    """
    uposmap = uposDict()
    if wordfile:
        with gzip.open(wordfile, "rb") as word_fp, gzip.open(tagfile, "rb") as tag_fp:
            for word, cluster in zip(word_fp, tag_fp):
                uposmap[word.strip()] = "Tag%s" % cluster.strip()
    else:
        with gzip.open(tagfile, "rb") as fp:
            for line in fp:
                word, cluster = line.strip().split('\t')

                uposmap[word] = "Tag%s" % cluster

    return uposmap

#print upos_map('ws+f.enw.kmeans100.gz')
