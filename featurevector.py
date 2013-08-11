import csv
import sys
import math
from matplotlib.pyplot import hist
import numpy as np
from scipy.spatial.distance import pdist
from sklearn import preprocessing, metrics, grid_search
from sklearn.cluster import KMeans, MiniBatchKMeans, AffinityPropagation, MeanShift, estimate_bandwidth, Ward
from sklearn.cluster.dbscan_ import DBSCAN
from sklearn.metrics import pairwise_distances
from sklearn.preprocessing import StandardScaler

VERBOSE = False
__author__ = 'husnusensoy'

featureMatrix = None
wordVector = None


def reader(filename, verbose=VERBOSE, delimeter="\t", nrows=1000):
    with open(filename, 'rb') as csvfile:
        for rownum, line in enumerate(csvfile, start=1):
            yield line.strip().split(delimeter)

            if rownum == nrows:
                break


def csvreader(filename, samplebytes=1024, verbose=VERBOSE):
    """

    :param filename: CSV file to be read
    :param samplebytes: Sample bytes for the sniffer
    :param verbose: verbosity on/off
    :return: (<csv row iteretor>, <file descriptor>, <csv dialect>)
    """
    csvfile = open(filename, 'rb')

    dialect = csv.Sniffer().sniff(csvfile.read(samplebytes))

    csvfile.seek(0)
    reader = csv.reader(csvfile, dialect)

    if verbose:
        print >> sys.stderr, dialect.__dict__

    return reader, csvfile, dialect


def docluster(n=13, algorithm='kmeans', minibatch=True, showClusters=False, distance_metric='euclidean', eps_in=0.4,
              MinPts_in=8):
    """

    :param n: Number of clusters
    :param showClusters: Dump clusters into JSON file
    """
    global featureMatrix
    global wordVector

    print >> sys.stderr, "Clustering for %d" % (n)

    if algorithm == 'kmeans':
        if minibatch:
            clustering = MiniBatchKMeans(init='k-means++', n_clusters=n, batch_size=1000,
                                         n_init=50, max_no_improvement=10, verbose=0).fit(featureMatrix)
        else:
            clustering = KMeans(n_clusters=n, init='k-means++', n_init=10, max_iter=300,
                                tol=1e-4, precompute_distances=True,
                                verbose=0, n_jobs=3).fit(featureMatrix)
    elif algorithm == "DBSCAN":

        clustering = DBSCAN(eps=eps_in, min_samples=MinPts_in, metric=distance_metric).fit(featureMatrix)

    elif algorithm == "Hierarchical":
        clustering = Ward(n_clusters=n).fit(featureMatrix)
    elif algorithm == "StructuredHierarchical":
        from sklearn.neighbors import kneighbors_graph

        print >> sys.stderr, "...Calculating KNN for %d" % (n)
        connectivity = kneighbors_graph(featureMatrix, n_neighbors=10)
        print >> sys.stderr, "...Clustering for %d" % n
        clustering = Ward(n_clusters=n, connectivity=connectivity).fit(featureMatrix)
    elif algorithm == "MeanShift":
        bandwidth = estimate_bandwidth(featureMatrix, quantile=0.3, n_samples=20000)

        clustering = MeanShift(bandwidth=bandwidth, bin_seeding=True)
        clustering.fit(featureMatrix)

        labels = clustering.labels_

        labels_unique = np.unique(labels)
        n_clusters_ = len(labels_unique)

        print >> sys.stderr, "Estimated number of clusters are %d" % n_clusters_
    elif algorithm == "AffinityPropagation":
        SUBSET_SIZE = 5000
        featureMatrix = featureMatrix[:SUBSET_SIZE]
        wordVector = wordVector[:SUBSET_SIZE]
        clustering = AffinityPropagation(preference=-4, verbose=True).fit(featureMatrix)
        n_clusters_ = len(clustering.cluster_centers_indices_)

        print >> sys.stderr, "Estimated number of clusters are %d" % n_clusters_

    k_means_labels = clustering.labels_

    #print >> sys.stderr,clustering.__dict__
    #print >> sys.stderr, "Calculating silhouette_score for %d" % (n)

    try:
        ss = metrics.silhouette_score(featureMatrix, clustering.labels_, metric='euclidean',
                                      sample_size=min(3500, len(wordVector)))
    except ValueError:
        pass
        ss = 0

    #ncluster = len(set(k_means_labels)) - (1 if -1 in k_means_labels else 0)
    ncluster = len( clustering.cluster_centers_indices_)

    print >> sys.stderr, "eps=%f, MinPts=%d # of clusters: %d (silhouette_score: %.6f)" % (
        eps_in, MinPts_in, ncluster, ss)

    if showClusters:
        groups = {}
        with open("german.%s.cluster" % (algorithm), "w") as fp:
            for cluster, word in zip(k_means_labels, wordVector):
                print >> fp, "%s\tC%d" % (word, cluster)
                if not cluster in groups:
                    groups[cluster] = []

                groups[cluster].append(word)

        import json

        with open("german.%s.cluster.json" % (algorithm), "wb") as fp:
            json.dump(groups, fp, indent=2)

    return ss, ncluster


def binned():
    #reader, pointer, dialect = csvreader("german.embeddings",verbose=True)
    #dialect.quoting = csv.QUOTE_NONE

    global featureMatrix
    global wordVector

    wordVector = []
    features = []
    for record in reader("german.embeddings", verbose=True, delimeter="\t", nrows=2000):
        word, featurelst = record[0], [float(f) for f in record[1:]]

        if VERBOSE:
            print >> sys.stderr, word

        features.append(featurelst)
        wordVector.append(word)

    featureMatrix = np.array(features)
    #featureMatrix = StandardScaler().fit_transform(featureMatrix)

    #print featureMatrix
    #print featureMatrix.shape
    euclideandist = pairwise_distances(featureMatrix)

    #print max(euclideandist.flatten())

    #print euclideandist

    if VERBOSE:
        print >> sys.stderr, wordVector[1:10]
        print >> sys.stderr, featureMatrix
        print >> sys.stderr, featureMatrix.shape

    from multiprocessing import Pool

    #p = Pool(3)

    #p.map(kmeans, range(8, 100, 2), 2)

    def asymmetric_n(min, max):
        next = min

        while next < max:
            yield next

            next += int(math.log(next, 2)) - 1

    #for n in range(16,23):
    #    docluster(n,algorithm='kmeans')

    from itertools import product

    results = []
    for eps, MinPts in product([5.5], [8]):
        sil, n = docluster(algorithm='AffinityPropagation', showClusters=True, eps_in=eps, MinPts_in=MinPts)

        results.append((sil, n, eps, MinPts))

    print sorted(results, key=lambda x: x[0], reverse=True)

    #docluster(1,algorithm="MeanShift")

if __name__ == "__main__":
    binned()
#reader, pointer, dialect = csvreader("german.embeddings.tab",verbose=True)

#pointer.close()

