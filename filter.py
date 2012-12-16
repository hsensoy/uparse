from common import dgiter,DependencyGraph
            			            			
def clone( source, target, dgmap=None, dgfilter=None ):
	from itertools import ifilter,imap
	with open(target,"w") as fp:
		if dgmap:
			if dgfilter:
				fp.write("\n\n".join(str(dg) for dg in ifilter(dgfilter, imap( dgmap, dgiter(source) ))))
			else:
				fp.write("\n\n".join(str(dg) for dg in imap( dgmap, dgiter(source) )))
		else:
			if dgfilter:
				fp.write("\n\n".join(str(dg) for dg in ifilter(dgfilter,  dgiter(source) )))
			else:
				fp.write("\n\n".join(str(dg) for dg in dgiter(source)))
					
def cloneAsCoNLLn(source,target,n=None):
	if n:
		clone(source, target, dgmap = DependencyGraph.filteredcopy, dgfilter=lambda dg: dg.length()<=n)	
	else:
		clone(source, target, dgmap = DependencyGraph.filteredcopy)
		
def cloneAsCoNLL10(source,target):
	cloneAsCoNLLn(source,target,10)
	
def cloneAsCoNLL20(source,target):
	cloneAsCoNLLn(source,target,20)
	
def cloneAsCoNLL40(source,target):
	cloneAsCoNLLn(source,target,40)
	
if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser(description='Cleanup & Filter CoNLL corpus')
	parser.add_argument('inputfile', metavar='input', type=str, nargs=1,
                   help='Source CoNLL corpus file including one or more dependency graphs')
        parser.add_argument('outputfile', metavar='output', type=str, nargs=1,
                   help='Target CoNLL corpus file used to store clean and filtered CoNLL corpus')
        group = parser.add_mutually_exclusive_group()
        group.add_argument('--wsj10', action='store_true')
	group.add_argument('--wsj20', action='store_true')                   
	group.add_argument('--wsj40', action='store_true')
	group.add_argument('--wsj', action='store_true')
	args = parser.parse_args()
	
	print args
	
	if args.wsj10:
		cloneAsCoNLL10(args.inputfile[0], args.outputfile[0])
	elif args.wsj20:
		cloneAsCoNLL20(args.inputfile[0], args.outputfile[0])
	elif args.wsj40:
		cloneAsCoNLL40(args.inputfile[0], args.outputfile[0])
	elif args.wsj:
		cloneAsCoNLL(args.inputfile[0], args.outputfile[0])
