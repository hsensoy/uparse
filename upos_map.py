#!/Users/husnusensoy/Downloads/pypy-2.0-beta2/bin/pypy
from collections import defaultdict
import gzip
import json
import sys

__author__ = 'husnusensoy'


uposmap = {}
def upos_map(file):
    with gzip.open(file,"rb") as fp:
        for line in fp:
            word, cluster = line.strip().split('\t')

            uposmap[word] = "Tag%s"%cluster

    return uposmap


#print upos_map('ws+f.enw.kmeans100.gz')
