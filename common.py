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
punct = ["A$", "C$", "$", "#", ".", ",", "?", "/", "(",":"]
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

	def postag(self):
		return self._cpostag if self._cpostag else self._postag
		
	def setId(self, id):
		self._id = id
	
	def setHead(self, head):
		self._head = head
		
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

_metrics = '\n%s Link Accuracy\n\tPrecision: %.3f\n\tRecall: %.3f \n\tF1: %.3f\n\tTotal number of links: %d\n\tNumber of total matched links: %d'
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

		self.underestpostag = {}
		self.overestpostag = {}
		
		self.underestform = {}
		self.overestform = {}
		
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
		if self.mNedge > 0 and self.gNedge > 0:
			if self.dNmatch > 0:
				self.dprecision = (self.dNmatch * 1.) /self.mNedge
				self.drecall = (self.dNmatch * 1.) /self.gNedge
				self.df1 = f1(self.dprecision,self.drecall)
		
			if self.uNmatch > 0:
				self.uprecision = (self.uNmatch * 1.) /self.mNedge
				self.urecall = (self.uNmatch * 1.) /self.gNedge
				self.uf1 = f1(self.uprecision,self.urecall)
		
		
	def __repr__(self):
		return _metrics%('Directed',self.dprecision, self.drecall, self.df1, self.gNedge, self.dNmatch)+'\n'+ _metrics%('Undirected', self.uprecision, self.urecall,self.uf1,self.gNedge, self.uNmatch)


ATTACH_TO_ROOT = 'A_T_R'
ATTACH_TO_PARENT = 'A_T_P'
ATTACH_TO_NEXT_FIRST = 'A_T_N_F'
ATTACH_TO_PRIOR_FIRST = 'A_T_P_F'
DONT_ATTACH = 'ORPHAN'
class DependencyGraph:
	def __init__(self,id = None):
		if id:
			self._dgid = id
		else:
			self._dgid = dgseq.nextval()
		self._nodes = []
		
	def addNode(self, node):
		self._nodes.append(node)
		
	def nodeiter(self):
		for n in self._nodes:
			yield n
		
	def removeall(self, rnodes, strategy=ATTACH_TO_PRIOR_FIRST):
		for n in self.nodeiter():
			if n._head == 0:
				n.hnode = None
			else:
				n.hnode = self._nodes[n._head - 1]
	
		for rn in rnodes:
			idx = None
			attachments = []
			for i in range(self.length()):
				if self._nodes[i]._id == rn._id:
					idx = i
				if self._nodes[i]._head == rn._id:
					attachments.append(i)

			if strategy == ATTACH_TO_PARENT:
				for i in attachments:
					self._nodes[i].hnode = self._nodes[idx].hnode
			elif strategy == ATTACH_TO_NEXT_FIRST:
				for i in attachments:
					if i != self.length() - 1:
						self._nodes[i].hnode = self._nodes[i+1]
					else:
						self._nodes[i].hnode = self._nodes[i - 1]
			elif strategy == ATTACH_TO_PRIOR_FIRST:
				for i in attachments:
					if i != 0:
						self._nodes[i].hnode = self._nodes[i - 1]
					else:
						self._nodes[i].hnode = self._nodes[i + 1]

			del self._nodes[idx]


		for i, n in enumerate(self.nodeiter()):
			n.setId(i+1)
		
		for n in self.nodeiter():
			if n.hnode is None:
				n.setHead(0)
			else:
				n.setHead( n.hnode._id )
			
			#if strategy == ATTACH_TO_ROOT:
				#n.setHead(0)
			#elif strategy == ATTACH_TO_PARENT:
				#n.setHead(self._nodes[ri]._head)
			#else:
				#n.setHead(None)
				
	def length(self):
		return len(self._nodes)
	
	def copy(self):
		import copy
		cpy = DependencyGraph()
		
		for n in self._nodes:
			cpy.addNode(copy.deepcopy(n))
			
		return cpy
		 
	@classmethod
	def filteredcopy(cls, dg):
		copydg = dg.copy()
		from itertools import ifilter
		copydg.removeall([rnode for rnode in ifilter( lambda n: n._form.upper() in punct or n._deprel == 'P', dg._nodes )])
			
		return copydg
		
	def __repr__(self):
		return "\n".join(str(n) for n in self._nodes)
		
	def edgeset(self, ignoreroot):
		from sets import Set
		
		return Set(( n._head, n._id) for n in self._nodes if n._head != 0 or not ignoreroot )
		
	def __eq__(self, other):
		return all( gn._form == mn._form for gn, mn in zip(self.nodeiter(),other.nodeiter()))
		
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

	if dg.length() > 0:
		yield dg
