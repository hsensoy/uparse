#!/Users/husnusensoy/Downloads/pypy-2.0-beta2/bin/pypy
from collections import Counter
import json

__author__ = 'husnusensoy'


cntr = Counter()
def head_nonterminal(json_file):
    with open(json_file,"r") as fp:
        for t in fp:
            jsonfrmt = json.loads(t)

            cntr[jsonfrmt[0]] +=1



print head_nonterminal('treebank+f.enw.kmeans100.key')
