from corpus import idg,itree,idgcorpus, itreecorpus,isdgcorpus
from common import DependencyGraph
from treebank import TreeUtil

def clone( icorpus, target, cmap=None, cfilter=None ):
	from itertools import ifilter,imap
	with open(target,"w") as fp:
			if cmap:
				if cfilter:
					fp.write("\n\n".join(str(dg) for dg in ifilter(cfilter, imap( cmap, icorpus))))
				else:
					fp.write("\n\n".join(str(dg) for dg in imap( cmap, icorpus)))
			else:
				if cfilter:
					fp.write("\n\n".join(str(dg) for dg in ifilter(cfilter,  icorpus)))
				else:
					fp.write("\n\n".join(str(dg) for dg in icorpus))
					
def cloneAsDGn(iwildcard,target,n=None):
	if n:
		clone(idgcorpus(iwildcard), target, cmap = DependencyGraph.filteredcopy, cfilter=lambda dg: 1<=dg.length()<=n )	
	else:
		clone(idgcorpus(iwildcard), target, cmap = DependencyGraph.filteredcopy)

def cloneAsTreen(iwildcard,target,n=None):
	if n:
		clone(itreecorpus(iwildcard), target, cmap = TreeUtil.filteredcopy, cfilter=lambda t: 1<= len(t.leaves()) <=n )	
	else:
		clone(itreecorpus(iwildcard), target, cmap = TreeUtil.filteredcopy)
		
if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser(description='Cleanup & Filter a dependency graph or parsing tree corpus')
	parser.add_argument('inputwildcard', type=str,
                   help='File wildcard showing corpus file(s) including one or more senentences')
        parser.add_argument('outputfile', metavar='output', type=str,
                   help='Target corpus file used to store clean and filtered corpus')

        constraintg = parser.add_mutually_exclusive_group()
        constraintg.add_argument('--wsj10', action='store_true', help='Cleaned sentences of maximum length 10 (Default)')
	constraintg.add_argument('--wsj20', action='store_true', help='Cleaned sentences of maximum length 20')                   
	constraintg.add_argument('--wsj40', action='store_true', help='Cleaned sentences of maximum length 40')
	constraintg.add_argument('--wsj', action='store_true', help='Cleaned sentences of full corpus')
	
	args = parser.parse_args()
	cloneFunc = cloneAsDGn if isdgcorpus(args.inputwildcard) else cloneAsTreen
	print args
	if cloneFunc == cloneAsTreen:
		print "Wildcard defines a tree corpus"
	else:
		print "Wildcard defined a dependency corpus"

	if args.wsj10:
		cloneFunc(args.inputwildcard, args.outputfile, 10)
	elif args.wsj20:
		cloneAsTreen(args.inputwildcard, args.outputfile, 20)
	elif args.wsj40:
		cloneAsTreen(args.inputwildcard, args.outputfile, 40)
	elif args.wsj:
		cloneAsTreen(args.inputwildcard, args.outputfile)
	else:
		cloneAsTreen(args.inputwildcard, args.outputfile,10)
