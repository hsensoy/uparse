__author__ = 'husnusensoy'
from math import log


class ProbabilityValue():
    def __init__(self, probability, log_probability=False):
        assert 0 <= probability <= 1 or log_probability

        if not log_probability:
            if probability == 0:
                self.is_zero = True
            else:
                self.is_zero = False
                self.log_probability = log(probability, 2)
        else:
            self.is_zero = False
            self.log_probability = probability

    def __add__(self, other):
        if not isinstance(other, ProbabilityValue):
            other = ProbabilityValue(other)

        if other.is_zero and self.is_zero:
            return ProbabilityValue(0)
        elif other.is_zero:
            return self
        elif self.is_zero:
            return other
        else:
            return ProbabilityValue(
                self.log_probability + log(1 + 2 ** (other.log_probability - self.log_probability), 2),
                log_probability=True)

    def __mul__(self, other):
        if not isinstance(other, ProbabilityValue):
            other = ProbabilityValue(other)

        if other.is_zero or self.is_zero:
            return ProbabilityValue(0)
        else:
            return ProbabilityValue(self.log_probability + other.log_probability, log_probability=True)

    def __repr__(self):
        if self.is_zero:
            return "0 (Inf)"
        else:
            return "%.4g (%f)" % (2 ** self.log_probability, -self.log_probability)


probability = ProbabilityValue

from collections import Counter, defaultdict


class Frequency(Counter):
    pass


class ConditionalFreq(defaultdict):
    def __init__(self):
        super(ConditionalFreq, self).__init__(Counter)


class Distribution(dict):
    def __init__(self, freq):
        """

        :param freq: Frequency class including counts of each event
        """
        super(dict, self).__init__()
        #        assert isinstance(freq, Frequency)

        total = sum(freq.values())
        for k in freq:
            self[k] = freq[k] * 1. / total


class InterpolatedDistribution(dict):
    def __init__(self, freq, unary_probability=0.0, lambd=1.0):
        super(dict, self).__init__()
        #        assert isinstance(freq, Frequency)

        total = sum(freq.values())
        for k in freq:
            self[k] = (freq[k] * 1. / total) * lambd + (1 - lambd) * unary_probability


class ConditionalDistribution(dict):
    def __init__(self, conditional_frequency):
        super(ConditionalDistribution, self).__init__()
        assert isinstance(conditional_frequency, ConditionalFreq)

        for condition in conditional_frequency:
            self[condition] = Distribution(conditional_frequency[condition])

    def probabilityOf(self, condition, w):
        if w in self[condition]:
            return self[condition][w]
        else:
            return 0.0



class InterpolatedConditionalDistribution(dict):
    def __init__(self, conditional_frequency, lambd=1.0):
        super(InterpolatedConditionalDistribution, self).__init__()
        assert isinstance(conditional_frequency, ConditionalFreq)

        freq = Frequency()
        for k in conditional_frequency:
            freq[k] += sum(conditional_frequency[k].values())

        self.lambd = lambd
        self.unary_distribution = Distribution(freq)

        for condition in conditional_frequency:
            self[condition] = Distribution(conditional_frequency[condition], self.unary_distribution[condition],
                                           self.lambd)

    def probabilityOf(self, condition, w):
        if w in self[condition]:
            return self[condition][w]
        else:
            return (1 - self.lambd) * self.unary_distribution[condition]


if __name__ == "__main__":
    trigram = ConditionalFreq()

    trigram["I-GRAM"]["dick"] += 1

    print trigram

    p = probability(0)
    q = probability(0.000000010)
    s = probability(0.5)

    print p + q
    print p * q + q * s
