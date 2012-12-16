class Sequence:
	def __init__(self, currval=None):
		if currval:
			self._value = curval
		else:
			self._value = 0
		
	def nextval(self, ):
		self._value += 1
		return self.currval()
	
	def currval(self,):
		return self._value
		
dgseq = Sequence()
punct = ["A$", "C$", "$", "#", ".", ",", "?", "/", "(", ":"]
NONE_STR='_'
from string import Template
_CoNLL2007Template = Template('\t'.join(('$id','$form','$lemma','$cpostag','$postag','$feats','$head','$deprel','$phead','$pdeprel')))
tconll = _CoNLL2007Template
class CoNLL2007Node:
	def __init__(self, id, form, lemma,cpostag, postag,feats,head,deprel,phead,pdeprel):
		self._id = None if id is None else int(id)		# integer
		self._form = form
		self._lemma = lemma
		self._cpostag = cpostag
		self._postag = postag
		self._feats = feats
		self._head = None if head is None else int(head)	# integer
		self._deprel = deprel
		self._phead = phead
		self._pdeprel = pdeprel
		
	def setId(self, id):
		self._id = id
	
	def decrementId(self):
		if self._id:
			self._id -= 1
	
	def setHead(self, head):
		self._head = head
		
	def decrementHead(self):
		if self._head:
			self._head -= 1
			
	@classmethod
	def byline(cls, line):
		t = [ t if t != '_' else None for t in line.split('\t')]
		#print t
		assert len(t) == 10
		
		return cls(t[0], t[1],t[2], t[3],t[4], t[5],t[6], t[7],t[8], t[9])
		
	def __repr__(self):
		nvl = lambda x: x if x is not None else NONE_STR
		return tconll.substitute(id= nvl(self._id), form=nvl(self._form), 
					lemma=nvl(self._lemma), cpostag=nvl(self._cpostag),
					postag=nvl(self._postag), feats=nvl(self._feats), 
					head=nvl(self._head), deprel=nvl(self._deprel),
					phead=nvl(self._phead), pdeprel=nvl(self._pdeprel))

Node = CoNLL2007Node

_metrics = Template('($type)\tPrecision: $precision Recall: $recall F1: $f1')
f1 = lambda p,r: 2*(p*r)/(p+r)
class Metrics:
	def __init__(self, ignoreroot):
		self._ignoreroot = ignoreroot
		self.gNedge = 0
		self.mNedge = 0
		
		self.dNmatch = 0
		self.uNmatch = 0
		
		self.dprecision = None
		self.drecall = None
		self.df1 = None
		
		self.uprecision = None
		self.urecall = None
		self.uf1 = None
		
		self._compute()
		
	def add(self, golddg, modeldg):
		gedges = golddg.edgeset(self._ignoreroot)
		medges = modeldg.edgeset(self._ignoreroot)
		
		self.gNedge += len(gedges)
		self.mNedge += len(medges)
		
		self.dNmatch += len(gedges.intersection(medges))
		self.uNmatch += sum ( 1 if (ge in medges) or ( (ge[1],ge[0]) in medges ) else 0 for ge in gedges )
		
		self._compute()
		
	def _compute(self):
		if self.mNedge > 0:
			self.dprecision = self.dNmatch * 1. /self.mNedge
			self.drecall = self.dNmatch * 1. /self.gNedge
			self.df1 = f1(self.dprecision,self.drecall)
		
			self.uprecision = self.uNmatch * 1. /self.mNedge
			self.urecall = self.uNmatch * 1. /self.gNedge
			self.uf1 = f1(self.uprecision,self.urecall)
		
		
	def __repr__(self):
		return _metrics.substitute(type='Directed', precision=self.dprecision, recall=self.drecall, f1=self.df1)+'\n'+ _metrics.substitute(type='Undirected', precision=self.uprecision, recall=self.urecall, f1=self.uf1)
		
		 
class DependencyGraph:
	def __init__(self,id = None):
		if id:
			self._dgid = id
		else:
			self._dgid = dgseq.nextval()
		self._nodes = []
		self._n = 0
		
	def addNode(self, node):
		self._n += 1
		self._nodes.append(node)
		
	def nodeiter(self):
		for n in self._nodes:
			yield n
		
	def removeNode(self, ridx):
		#print "Removing node %d"%ridx
		for i, n in enumerate(self._nodes):
			if ridx < n._id:
				n.decrementId()
			elif ridx == n._id:
				ri = i
				
			if ridx < n._head:
				n.decrementHead() 
			elif ridx == n._head:
				n.setHead(None)
				
		del self._nodes[ri]
			
	def length(self):
		return self._n
	
	def copy(self):
		cpy = DependencyGraph()
		
		for n in self._nodes:
			cpy.addNode(n)
			
		return cpy
		 
	@classmethod
	def filteredcopy(cls, dg):
		copydg = dg.copy()
		from itertools import ifilter
		for rnode in ifilter( lambda n: n._form in punct or n._deprel == 'P', dg._nodes ):
			copydg.removeNode(rnode._id)
			
		return copydg
		
	def __repr__(self):
		return "\n".join(str(n) for n in self._nodes)
		
	def edgeset(self, ignoreroot):
		from sets import Set
		
		return Set(( n._head if n._head != '_' else 0, n._id) for n in self._nodes if n._head != 0 or not ignoreroot )
		
	def __eq__(self, other):
		pass
		
def dgiter(filename):
	dg = DependencyGraph()
	with open(filename) as fp:
		for line in fp:
			trimmed = line.strip()
		
			if len(trimmed) == 0:
                		yield dg
                		dg = DependencyGraph()
            		else:
            			dg.addNode( Node.byline(trimmed) )
