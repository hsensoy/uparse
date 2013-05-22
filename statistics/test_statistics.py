from unittest import TestCase
from src.nlp.tagger import RARE

__author__ = 'husnusensoy'

from probability import Frequency


class TestFrequency(TestCase):
    def setUp(self):
        pass


    def test_simple(self):
        freq = Frequency()
        freq['case'] += 1
        self.assertEquals(freq['case'], 1)

        freq['case'] += 10
        self.assertEquals(freq['case'], 11)

    def test_with_rare(self):
        singleClassRarePreprocessor = lambda x, y: RARE if x not in y else x
        freq = Frequency(keySet=["husnu", "nuri", "fahri", "nurdan"], rareMap=singleClassRarePreprocessor)

        freq['husnu'] += 1
        self.assertEquals(freq['husnu'], 1)

        freq['nurdan'] += 5

        freq['osman'] += 4
        freq['jeffry'] += 10

        freq['fahri'] += 3
        freq['nuri'] += 4

        self.assertEquals(freq['nurdan'], 5)
        self.assertEquals(freq['fahri'], 3)
        self.assertEquals(freq['nuri'], 4)
        self.assertEquals(freq[RARE], 14)