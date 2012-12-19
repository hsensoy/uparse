import unittest
from corpus import idg,itree, idgcorpus, itreecorpus

wsj10file = 'coNLL10.dp'
class TestUparse(unittest.TestCase):
	def setUp(self):
		self.maxDiff = 2000
		pass

	def _file_content(self, filename):
		nsentence = 0
		lengths = []
		for dg in idg(filename):
			nsentence+=1
			lengths.append(dg.length())

		return nsentence, lengths

	@unittest.skip("Scanning all CoNLL corpus")
	def test_corpus_size(self):
		ncorpus = 0
		for dg in idgcorpus('conll/*/*.dp'):
			ncorpus+=1

		self.assertEqual(49208, ncorpus)

	@unittest.skip("Scanning all CoNLL corpus")
	def test_edge_count_in_dependency_graph(self):
		for dg in idgcorpus('conll/*/*.dp'):
			self.assertEqual(dg.length(), len(dg.edgeset(False)))
	
	def test_edge_count_in_coNLL10(self):
		for dg in idgcorpus('coNLL10.dp'):
			self.assertEqual(dg.length(), len(dg.edgeset(False)))
		
	def test_lhead_metrics(self):
		from parser import lhead
		from common import Metrics

		m_ignoreroot,m  = Metrics(True),Metrics(False)
		for dg in idg('conll/00/wsj_0001.dp'):
			m_ignoreroot.add(dg, lhead(dg))
			m.add(dg, lhead(dg))

		self.assertEqual(31, m.directed.nreference)
		self.assertEqual(29, m_ignoreroot.directed.nreference)
		self.assertEqual(15, m_ignoreroot.undirected.nmatch)
		self.assertEqual(7, m_ignoreroot.directed.nmatch)
		self.assertEqual(15, m.undirected.nmatch)
		self.assertEqual(7, m.directed.nmatch)
	
	def test_rhead_metrics(self):
		from parser import rhead
		from common import Metrics

		m_ignoreroot,m  = Metrics(True),Metrics(False)
		for dg in idg('conll/00/wsj_0001.dp'):
			m_ignoreroot.add(dg, rhead(dg))
			m.add(dg, rhead(dg))

		self.assertEqual(31, m.directed.nreference)
		self.assertEqual(29, m_ignoreroot.directed.nreference)
		self.assertEqual(15, m_ignoreroot.undirected.nmatch)
		self.assertEqual(8, m_ignoreroot.directed.nmatch)
		self.assertEqual(15, m.undirected.nmatch)
		self.assertEqual(8, m.directed.nmatch)
		
	
	def test_dependency_graph(self):
		from sets import Set
		for i, dg in enumerate(idg('conll/00/wsj_0001.dp')):
			if i == 0:
				self.assertEqual(Set([(2, 7), (12, 15), (5, 4), (2, 6), (15, 13), (8, 2), (11, 10), (2, 1), (8, 9), (9, 16), (9, 11), (2, 3), (9, 12), (8, 18), (15, 14), (0, 8), (6, 5), (16, 17)]), dg.edgeset(False))
				self.assertEqual(Set([(2, 7), (12, 15), (5, 4), (2, 6), (15, 13), (8, 2), (11, 10), (2, 1), (8, 9), (9, 16), (9, 11), (2, 3), (9, 12), (8, 18), (15, 14), (6, 5), (16, 17)]), dg.edgeset(True))
			else:
				self.assertEqual(Set([(2,1), (3,2), (0,3),(3,4),(4,5),(5,6),(6,7),(6,8),(12,9),(12,10),(12,11),(6,12),(3,13)]), dg.edgeset(False))
				self.assertEqual(Set([(2,1), (3,2),(3,4),(4,5),(5,6),(6,7),(6,8),(12,9),(12,10),(12,11),(6,12),(3,13)]), dg.edgeset(True))
			
	def test_wsj_sample_file(self):
		cnt1, length1 = self._file_content('conll/00/wsj_0001.dp')
		self.assertEqual(2, cnt1)
		self.assertEqual([18,13], length1)
		
		cnt2, length2 = self._file_content('conll/00/wsj_0002.dp')
		self.assertEqual(1, cnt2)
		self.assertEqual([26], length2)
		
		cnt3, length3 = self._file_content('conll/00/wsj_0003.dp')
		self.assertEqual(30, cnt3)
		self.assertEqual([36,32,26,35,12,16,10,21,25,23,34,19,22,17,23,22,36,23,42,52,19,18,14,21,13,34,24,31,15,10], length3)
			
	
	def tesit_dg10_sentence_count(self):
		self.assertEqual(7422, len([dg for dg in idg(wsj10file)]))
	
	def test_tree10_sentence_count(self):
		self.assertEqual(7422, len([t for t  in itree('treebank_wsj10.mrg')]))
	
	def test_tree10_sentence_length_freq(self):
		expected = {1: 159, 2: 340, 3: 377, 4: 518, 5: 614, 6: 737, 7: 878, 8: 1107, 9: 1208, 10: 1484}
		actual = {}
		for t in itree('treebank_wsj10.mrg'):
			length = len(t.leaves())
			if length not in actual:
				actual[length] = 0

			actual[length]+=1

		self.assertEqual(expected, actual)
	
	def test_wsj10_sentence_length_freq(self):
		expected = {1: 159, 2: 340, 3: 377, 4: 518, 5: 614, 6: 737, 7: 878, 8: 1107, 9: 1208, 10: 1484}
		actual = {}
		for dg in idg(wsj10file):
			if dg.length() not in actual:
				actual[dg.length()] = 0

			actual[dg.length()]+=1

		self.assertEqual(expected, actual)

	def test_tree10_postag_freq(self):
		expected = {'PRP$': 412, 'VBG': 735, 'VBD': 2633, 'VBN': 1282, 'VBP': 1361, 'WDT': 66, 
'JJ': 3658, 'WP': 145, 'VBZ': 2320, 'DT': 4586, 'RP': 141, 'NN': 7718, 'FW': 22, 'POS': 332, 'TO': 1183, 'PRP': 2000, 'RB': 3071, 
    'NNS': 3927, 'NNP': 5570, 'VB': 1616, 'WRB': 96, 'CC': 1036, 'LS': 24, 'PDT': 31, 'RBS': 26, 'RBR': 113, 'CD': 3004, 
   'EX': 120, 'IN': 3720, 'MD': 678, 'NNPS': 192, 'JJS': 106, 'JJR': 228, 'SYM': 51, 'UH': 45}
		actual = {}
	
		for t in itree('treebank_wsj10.mrg'):
			for pos in [ pos for _,pos in t.pos() ]:
				if pos not in actual:
					actual[ pos ] = 0

				actual[ pos ]+=1

		self.assertEqual(expected, actual)

	def test_wsj10_postag_freq(self):
		expected = {'PRP$': 412, 'VBG': 735, 'VBD': 2633, 'VBN': 1282, 'VBP': 1361, 'WDT': 66, 
'JJ': 3658, 'WP': 145, 'VBZ': 2320, 'DT': 4586, 'RP': 141, 'NN': 7718, 'FW': 22, 'POS': 332, 'TO': 1183, 'PRP': 2000, 'RB': 3071, 
    'NNS': 3927, 'NNP': 5570, 'VB': 1616, 'WRB': 96, 'CC': 1036, 'LS': 24, 'PDT': 31, 'RBS': 26, 'RBR': 113, 'CD': 3004, 
   'EX': 120, 'IN': 3720, 'MD': 678, 'NNPS': 192, 'JJS': 106, 'JJR': 228, 'SYM': 51, 'UH': 45}
		actual = {}
	
		for dg in idg(wsj10file):
			for n in dg.nodeiter():
				if n.postag() not in actual:
					actual[n.postag()] = 0

				actual[n.postag()]+=1

		self.assertEqual(expected, actual)

        # should raise an exception for an immutable sequence
        #self.assertRaises(TypeError, random.shuffle, (1,2,3))

        #element = random.choice(self.seq)
        #self.assertTrue(element in self.seq)

        #with self.assertRaises(ValueError):
        #    random.sample(self.seq, 20)
        #for element in random.sample(self.seq, 5):
        #    self.assertTrue(element in self.seq)
'''
sentence = "((FRAG (NP-SBJ (DT The) (NN vote) (S (VP (TO to) (VP (VB approve))))) (X (VBD was))))"


t = Tree(sentence)
print t.pprint()
print spannings(t, unary=False)
n = len(t.leaves())
print rbranch(n)
print rbranch(n, unary= False)
print rbranch(len(t.leaves()), unary= False, root=False)
print rbranch(len(t.leaves()), root=False)
print lbranch(len(t.leaves()))
print lbranch(n, unary= False)
print lbranch(len(t.leaves()), unary= False, root=False)
print lbranch(len(t.leaves()), root=False)
'''
if __name__ == '__main__':
	unittest.main()
