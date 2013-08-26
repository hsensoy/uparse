#!/usr/local/bin/pypy
import sys
import math
from array import array
import operator

VERBOSE = False


def reader(filename, verbose=VERBOSE, delimeter="\t", nrows=1000):
    with open(filename, 'rb') as csvfile:
        for rownum, line in enumerate(csvfile, start=1):
            yield line.strip().split(delimeter)

            if rownum == nrows:
                break

def pipe_reader(verbose=VERBOSE, delimeter="\t"):
	for line in sys.stdin:
		yield line.strip().split(delimeter)

features = []
for record in pipe_reader(verbose=True, delimeter="\t"):
    word, featurelst = record[0], array('f', [float(f) for f in record[1:]])

    if VERBOSE:
        print >> sys.stderr, word

    features.append(featurelst)
    #wordVector.append(word)

#featureMatrix = np.array(features)

n = len(features)
#print >> sys.stderr, n

#print >> sys.stderr, features[0]

for i in range(n):
    buffer = [
        "%05d %05d %.6f" % (i+1, j+1, math.sqrt(sum((f1 - f2) * (f1 - f2) for f1, f2 in zip(features[i], features[j])))) for
        j in range(n) if i != j]

    #buffer.append((i,j,-euc))

    #print >> sys.stdout, "%05d %05d %.6f" % (i + 1, j + 1, -euc)

    #print >> sys.stderr, "Row %d is done." % i

    #print >> sys.stdout, "\n".join(buffer), "\n"

    sys.stdout.write("\n".join(buffer))
    sys.stdout.write("\n")

