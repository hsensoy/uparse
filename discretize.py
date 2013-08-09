from scipy.stats.mstats_basic import mquantiles
import sys

__author__ = 'husnusensoy'
import numpy as np
VERBOSE = False

with open("german.embeddings", "r") as fp, open("german.embeddings.tab", "wb") as wfp:
    wordVector = []
    features = []
    for line in fp:
        tokens = line.strip().split('\t')

        assert (len(tokens) == 26)

        #print >> wfp, "\t".join(tokens)

        word, featurelst = tokens[0], [float(f) for f in tokens[1:]]

        features.append(featurelst)
        wordVector.append(word)

    featureMatrix = np.array(features)

print >> sys.stderr, featureMatrix
print >> sys.stderr, "*" * 100
TfeatureMatrix = featureMatrix.transpose()

TdiscritizedfeatureNestedList = []
for column in TfeatureMatrix:
    print >> sys.stderr, column.tolist()[1:10], len(column.tolist()), np.average(column)

    bins = mquantiles(column, prob=np.array([0.01 * q for q in range(1, 101)]), alphap=0, betap=1)

    print >> sys.stderr, bins

    Bcolumn = np.digitize(column, bins).tolist()
    print >> sys.stderr, Bcolumn[1:10]

    TdiscritizedfeatureNestedList.append(Bcolumn)

TdiscritizedfeatureMatrix = np.array(TdiscritizedfeatureNestedList)


if VERBOSE:
    for word, dfeatures, cfeatures in zip(wordVector, TdiscritizedfeatureMatrix.transpose(), featureMatrix):
        print >> sys.stdout, "%s\t%s" % (word, "\t".join("%d(%f)" % (df, cf) for df, cf in zip(dfeatures, cfeatures)) )
else:
    for word, dfeatures in zip(wordVector, TdiscritizedfeatureMatrix.transpose()):
        print >> sys.stdout, "%s\t%s" % (word, "\t".join("%d" % (df) for df in dfeatures) )
