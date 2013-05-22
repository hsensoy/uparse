#!/Users/husnusensoy/Downloads/pypy-2.0-beta2/bin/pypy
__author__ = 'husnusensoy'

from itertools import product
import json
import sys
from statistics.probability import Frequency, ConditionalFreq, ConditionalDistribution

verbose = False

nonterminal_freq = Frequency()
unary_freq = ConditionalFreq()
binary_freq = ConditionalFreq()
binary_dist = None
unary_dist = None
r_unary_freq = None
r_binary_freq = None

def load_pcfg(count_file):
    global nonterminal_freq,unary_freq,binary_freq,binary_dist,unary_dist,r_binary_freq,r_unary_freq
    with open(count_file) as fp:
        for line in fp:
            token = [t.strip() for t in line.split(' ')]

            if len(token) == 3:
                count, type, X = int(token[0]), token[1], token[2]

                if type == 'NONTERMINAL':
                    nonterminal_freq[X] = count
                else:
                    sys.stderr.write(token)
            elif len(token) == 4:
                count, type, X, word = int(token[0]), token[1], token[2], token[3]

                if type == 'UNARYRULE':
                    unary_freq[X][word] = count
                else:
                    sys.stderr.write(token)
            elif len(token) == 5:
                count, type, X, Y1, Y2 = int(token[0]), token[1], token[2], token[3], token[4]

                if type == 'BINARYRULE':
                    binary_freq[X][Y1, Y2] = count
                else:
                    sys.stderr.write(token)

    binary_dist = ConditionalDistribution(binary_freq)
    unary_dist = ConditionalDistribution(unary_freq)

    # TODO: Reverse function into ConditionFreq class
    r_binary_freq = ConditionalFreq()
    for condition in binary_freq:
        for variant in binary_freq[condition]:
            r_binary_freq[variant][condition] = binary_freq[condition][variant]

    r_unary_freq = ConditionalFreq()
    for condition in unary_freq:
        for variant in unary_freq[condition]:
            r_unary_freq[variant][condition] = unary_freq[condition][variant]

    sys.stderr.write("Unary Rule Heads Count %d\n" % len(unary_dist.keys()))
    sys.stderr.write("Binary Rule Head Count %d\n" % len(binary_dist.keys()))

    '''
    pprint.pprint(unary_freq)
    pprint.pprint(binary_freq)
    pprint.pprint(nonterminal_freq)
    '''




class Cell:
    def __init__(self, score, l_bp, r_bp):
        self.score = score
        self.l_bp = l_bp
        self.r_bp = r_bp

    def __str__(self):
        return "%f, %s, %s" % (self.score, str(self.l_bp), str(self.r_bp))

    def __repr__(self):
        return self.__str__()


import re


def parse(sentence):
    """

    :param sentence: Either a list of words or space seperated sentence of words
    :return: JSON formatted parsed tree
    """

    def build(triplet, pi):
        """

        :param triplet: (0, length-1, X)
        :param pi:      Dictionary of values
        :return:        JSON form parsing tree
        """
        if "^" in triplet[2]:
            try:
                head = re.sub(r'\^<\w+>', lambda s: "", triplet[2])
                nested = [head]
            except:
                sys.stderr.write(triplet[2])
        else:
            nested = [triplet[2]]

        if pi[triplet].r_bp:
            nested.append(build(pi[triplet].l_bp, pi))
            nested.append(build(pi[triplet].r_bp, pi))
        else:
            nested.append(pi[triplet].l_bp[2])

        return nested

    pi = {}

    if all(len(w) == 2 for w in sentence):
        tag = [t for t, w in sentence]
        word = [w for t, w in sentence]
        tagged = True
    else:
        word = sentence
        tagged = False

    #sys.stderr.write(sentence + "\n")
    for length in range(len(word)):
        for left in range(len(word)):
            right = left + length

            if right < len(word):
                if length == 0:
                #target = word[left] if word[left] in unary_r else "_RARE_"

                #if verbose and target == "_RARE_":
                #    sys.stderr.write("%s is replaced with _RARE_" % word[left]

                    if tagged:
                        pi[left, right, tag[left]] = Cell(score=1.0,
                                                          l_bp=(left, right, word[left]),
                                                          r_bp=None)
                    else:
                        for X in r_unary_freq[word[left]]:
                            pi[left, right, X] = Cell(score=unary_dist[X][word[left]],
                                                      l_bp=(left, right, word[left]),
                                                      r_bp=None)
                #print X,"\t->\t",pi[left, right, X]

                elif length > 0:
                    #print left, right
                    '''
                        Instead of filtering full set of keys in the inner loop.
                        We filter them in here by bounding left and right positions and converting into a list
                    '''
                    pikeys = filter(lambda key: key[0] == left or key[1] == right, pi.keys())
                    for k in range(left, right):
                        for (_, _, Y1), (_, _, Y2) in product(
                                filter(lambda key: key[1] == k, pikeys),
                                filter(lambda key: key[0] == k + 1, pikeys)):
                            for X in r_binary_freq[Y1, Y2]:
                            #print "%s -> %s %s (%f)" % (X, Y1, Y2, binary_r[Y1, Y2][X])
                                temp_score = binary_dist[X][Y1, Y2] * pi[left, k, Y1].score * pi[
                                    k + 1, right, Y2].score
                                if (left, right, X) in pi:
                                    if pi[left, right, X].score < temp_score:
                                        pi[left, right, X].score = temp_score
                                        pi[left, right, X].l_bp = (left, k, Y1)
                                        pi[left, right, X].r_bp = (k + 1, right, Y2)
                                        #print X,"\t->\t",pi[left, right, X]
                                else:
                                    pi[left, right, X] = Cell(
                                        score=temp_score,
                                        l_bp=(left, k, Y1),
                                        r_bp=(k + 1, right, Y2))
                                    #print X,"\t->\t",pi[left, right, X]

                '''
                for k, v in sorted(filter(lambda x: x[0][0] == left and x[0][1] == right, pi.iteritems()),
                                   key=lambda y: y[1].score, reverse=True)[5:]:
                    del pi[k]
                '''

    try:
        (_, _, head), v = max(filter(lambda x: x[0][0] == 0 and x[0][1] == len(word) - 1,
                                     pi.iteritems()),
                              key=lambda y: y[1].score)

        return build((0, len(word) - 1, head), pi)
    except ValueError:
        sys.stderr.write(str(sentence) + "\n")
        sys.stderr.write("Could not parse the tree at this time\n")
        return None


#sentence = "What does the Peugeot company manufacture ?"
#print parse(sentence)

#with open("../data/pa2/parse_dev.dat") as fp, open("../data/pa2/parse_dev.out", "w") as wp:
#    for line in fp:
#        json.dump(parse(line.strip()), wp)
#        wp.write('\n')


#headcandidate = head_nonterminal(args.file)
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Parse given a set of trees using PCFG parser')
    parser.add_argument('rules', help='Binary and Unary PCFG rule frequencies')
    parser.add_argument('file', type=str,
                        help='File containing sentences to be parsed')
    parser.add_argument('--parallel', type=int, help="Parallel number of slaves to be used for parsing", default=1)

    args = parser.parse_args()

    load_pcfg(args.rules)
    nsentence = 0
    with open(args.file) as fp:
        for line in fp:
            nsentence += 1

    if args.parallel == 1:
        with open(args.file) as fp:
            for i, line in enumerate(fp,start=1):
                tree = parse(json.loads(line))

                sys.stderr.write("%d out of %d completed so far\n"%(i, nsentence))

                if not tree:
                    sys.stdout.write("#####\n")
                else:
                    json.dump(tree, sys.stdout)
                    sys.stdout.write('\n')
    else:
        from multiprocessing import Pool
        pool = Pool(processes=args.parallel)

        with open(args.file) as fp:
            for i, tree in enumerate(pool.imap(parse, [json.loads(line) for line in fp], chunksize=1)):

                sys.stderr.write("%d out of %d completed so far\n"%(i, nsentence))
                if not tree:
                    sys.stdout.write("#####\n")
                else:
                    json.dump(tree, sys.stdout)
                    sys.stdout.write('\n')

#example = '["S", ["NP", ["DET", "There"]], ["S", ["VP", ["VERB", "is"], ["VP", ["NP", ["DET", "no"], ["NOUN", "asbestos"]], ["VP", ["PP", ["ADP", "in"], ["NP", ["PRON", "our"], ["NOUN", "products"]]], ["ADVP", ["ADV", "now"]]]]], [".", "."]]]'
#orginal = "There is no asbestos in our products now ."
#parse(orginal)
