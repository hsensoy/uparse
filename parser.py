from common import DependencyGraph
from corpus import idgcorpus, itreecorpus,isdgcorpus
from treebank import TreeUtil
import warnings

def rhead(dg):
	l = dg.length()
	
	parsed = dg.copy()
	for n in parsed.nodeiter():
		if n._id < l:
			n.setHead(n._id + 1)
		else:
			n.setHead(0)
			
	return parsed
	
def lhead(dg):
	l = dg.length()
	
	parsed = dg.copy()
	for n in parsed.nodeiter():
		if n._id > 1:
			n.setHead(n._id - 1)
		else:
			n.setHead(0)
			
	return parsed

def lbranch(t, _root=True, _unary=True):
	n = len(t.leaves())
        return set( (0,l) for l in range(1 if _unary else 2, n+1 if _root else n) )

def rbranch(t, _root=True, _unary=True):
	n = len(t.leaves())
        return set( (l,n) for l in range(n-1 if _unary else n-2, -1 if _root else 0,-1) )

def gbranch(t, _root=True, _unary=True):
        return TreeUtil.bracketing(t, root=_root, unary=_unary)

def toString(_set):
	return ",".join("(%s,%s)"%(lb,rb) for lb,rb in _set)

def parse_and_store(finput, foutput, model = rhead):
	with open(foutput,"w") as fp:
		if model in (rhead, lhead):
			fp.write("\n\n".join(str(model(dg)) for dg in idgcorpus(finput)))
		else:
			fp.write("\n".join("%d:%s"%( len(t.leaves()) , toString(model(t, _root=True,_unary=False))) for t in itreecorpus(finput)))
		
if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser(description='Some popular baseline parsings for given corpus files')
	parser.add_argument('finput', type=str,
                   help='Source corpus file(s) to be parsed')
        parser.add_argument('foutput', type=str,
                   help='Target file including parsing')
        group = parser.add_mutually_exclusive_group()
        group.add_argument('--rhead', action='store_true',help="Right head parsing")
	group.add_argument('--lhead', action='store_true',help="Left head parsing")
	group.add_argument('--gbranch', action='store_true',help="Gold bracketing")
        group.add_argument('--rbranch', action='store_true',help="Right bracketing")
	group.add_argument('--lbranch', action='store_true',help="Left bracketing")
	args = parser.parse_args()
	
	if args.rhead:
		if not isdgcorpus(args.finput):
			warnings.warn("Corpus seems to be a tree corpus. Failover to Left Branch parsing")
			parse_and_store(args.finput, args.foutput,lbranch)
		else:
			parse_and_store(args.finput, args.foutput,rhead)
	elif args.lhead:
		if not isdgcorpus(args.finput):
			warnings.warn("Corpus seems to be a tree corpus. Failover to Right Branch parsing")
			parse_and_store(args.finput, args.foutput,rbranch)
		else:
			parse_and_store(args.finput, args.foutput,lhead)
	elif args.rbranch:
		if isdgcorpus(args.finput):
			warnings.warn("Corpus seems to be a dependency corpus. Failover to Left Head parsing")
			parse_and_store(args.finput, args.foutput,lhead)
		else:
			parse_and_store(args.finput, args.foutput,rbranch)
	elif args.lbranch:
		if isdgcorpus(args.finput):
			warnings.warn("Corpus seems to be a dependency corpus. Failover to Right Head parsing")
			parse_and_store(args.finput, args.foutput,rhead)
		else:
			parse_and_store(args.finput, args.foutput,lbranch)
	else:
		if isdgcorpus(args.finput):
			warnings.warn("Corpus seems to be a dependency corpus. Gold parsing is only valid for tree corpus.")
		else:
			parse_and_store(args.finput, args.foutput,gbranch)
