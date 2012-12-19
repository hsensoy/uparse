from nltk.corpus.reader import find_corpus_fileids
from nltk.data import FileSystemPathPointer

import glob
from nltk.tag import simplify_wsj_tag
from nltk.tree import Tree

badtokens = [".", ",", "``", "''", ":", "$", "-NONE-", "-RRB-", "-LRB-","#"]
"""
Checks for terminal node.
"""
def isterminal(tree):
	return not isinstance(tree, Tree)

"""
Checks for parent of terminal non-terminal node.
"""
def ispreterminal(tree):
	return not all(isinstance(c, Tree) for c in tree)

"""
Remove bad tokens in given sentences gold tree
"""
def nopunct(sent):
	return Tree(sent.node, [nopunct(c) for c in sent if c.node not in badtokens ]) if not ispreterminal(sent) else sent

def noemptysubtree(sent):
	if ispreterminal(sent):
       		return sent
    	else:
        	return Tree(sent.node, [noemptysubtree(c) for c in sent if len(c) > 0 ])

class TreeUtil:

	@classmethod
	def filteredcopy(cls, t):
		return noemptysubtree(nopunct(t.copy(deep=True)))
	
	@classmethod
	def bracketing(cls, tree, leaves=True, root=True, unary=True):
    		"""Returns the set of unlabeled spannings.
    		""" 
    		queue = tree.treepositions()
		stack = [(queue.pop(0), 0)]
		j = 0
    		result = set()
    		while stack != []:
        		(p, i) = stack[-1]
			if queue == [] or queue[0][:-1] != p:
				if isinstance(tree[p], Tree):
					result.add((i, j))
				else:
                			if leaves:
                    				result.add((i, i + 1))
                			j = i + 1

				stack.pop()
        		else:
            			q = queue.pop(0)
            			stack.append((q, j))
		
		if not root:
			result.remove((0, len(tree.leaves())))

		if not unary:
			result = set(filter(lambda (x, y): x != y - 1, result))
		
		return result

