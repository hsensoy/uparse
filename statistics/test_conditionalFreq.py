from unittest import TestCase
from src.nlp.tagger import singleClassRarePreprocessor, RARE
from src.part2and3 import ingram
from src.nlp.reader.conll import WordTag

__author__ = 'husnusensoy'

from probability import ConditionalFreq


class TestConditionalFreq(TestCase):
    def test_nokey_error(self):
        condfreq = ConditionalFreq()

        self.assertEqual(condfreq['arbitrary']['ofarbitrary'], 0)

    def test_simple(self):
        condfreq = ConditionalFreq()

        condfreq['O']['husnu'] += 1

        self.assertEqual(condfreq['O']['husnu'], 1)

    def test_with_rare(self):
        condfreq = ConditionalFreq(["this", "that", "it"], singleClassRarePreprocessor)

        condfreq['O']["may"] += 1

        self.assertEqual(condfreq['O']["may"], 1)
        self.assertEqual(condfreq['O'][RARE], 1)

        condfreq['O']['this'] += 1
        print condfreq
        self.assertEqual(condfreq['O']['this'], 1)

    def test_tag(self):
        simple = ["O","O","I-GENE","I-GENE","O","I-GENE","I-GENE","I-GENE"]
        trigram_sample = ConditionalFreq()

        for ng in ingram( [WordTag(s,None) for s in simple]):
            trigram_sample[ng[0]][ng[1]] += 1

        self.assertEqual(trigram_sample['*','*']['O'], 1)
        self.assertEqual(trigram_sample['*','O']['O'], 1)
        self.assertEqual(trigram_sample['O','O']['I-GENE'], 1)
        self.assertEqual(trigram_sample['O','I-GENE']['I-GENE'], 2)
        self.assertEqual(trigram_sample['I-GENE','I-GENE']['O'], 1)
        self.assertEqual(trigram_sample['I-GENE','I-GENE']['I-GENE'], 1)
        self.assertEqual(trigram_sample['I-GENE','I-GENE']['I-GENE'], 1)
        self.assertEqual(trigram_sample['I-GENE','O']['I-GENE'], 1)
