from common import dgiter,DependencyGraph
import glob

def alldgiter(iwildcard):
	for source in glob.glob(iwildcard):
		for dg in dgiter(source):
			yield dg
            			            			
def clone( iwildcard, target, dgmap=None, dgfilter=None ):
	from itertools import ifilter,imap
	with open(target,"w") as fp:
			if dgmap:
				if dgfilter:
					fp.write("\n\n".join(str(dg) for dg in ifilter(dgfilter, imap( dgmap, alldgiter(iwildcard)))))
				else:
					fp.write("\n\n".join(str(dg) for dg in imap( dgmap, alldgiter(iwildcard))))
			else:
				if dgfilter:
					fp.write("\n\n".join(str(dg) for dg in ifilter(dgfilter,  alldgiter(iwildcard))))
				else:
					fp.write("\n\n".join(str(dg) for dg in alldgiter(iwildcard)))
					
def cloneAsCoNLLn(iwildcard,target,n=None):
	if n:
		clone(iwildcard, target, dgmap = DependencyGraph.filteredcopy, dgfilter=lambda dg: dg.length()<=n and dg.length() >= 2)	
	else:
		clone(iwildcard, target, dgmap = DependencyGraph.filteredcopy)
		
def cloneAsCoNLL10(iwildcard,target):
	cloneAsCoNLLn(iwildcard,target,10)
	
def cloneAsCoNLL20(iwildcard,target):
	cloneAsCoNLLn(iwildcard,target,20)
	
def cloneAsCoNLL40(iwildcard,target):
	cloneAsCoNLLn(iwildcard,target,40)
	
if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser(description='Cleanup & Filter CoNLL corpus')
	parser.add_argument('inputwildcard', type=str,
                   help='File wildcard showing CoNLL corpus file(s) including one or more dependency graphs')
        parser.add_argument('outputfile', metavar='output', type=str, nargs=1,
                   help='Target CoNLL corpus file used to store clean and filtered CoNLL corpus')
        group = parser.add_mutually_exclusive_group()
        group.add_argument('--wsj10', action='store_true', help='Cleaned sentences of maximum length 10')
	group.add_argument('--wsj20', action='store_true', help='Cleaned sentences of maximum length 20')                   
	group.add_argument('--wsj40', action='store_true', help='Cleaned sentences of maximum length 40')
	group.add_argument('--wsj', action='store_true', help='Cleaned sentences of full corpus')
	args = parser.parse_args()
	
	print args
	
	if args.wsj10:
		cloneAsCoNLL10(args.inputwildcard, args.outputfile[0])
	elif args.wsj20:
		cloneAsCoNLL20(args.inputwildcard, args.outputfile[0])
	elif args.wsj40:
		cloneAsCoNLL40(args.inputwildcard, args.outputfile[0])
	elif args.wsj:
		cloneAsCoNLL(args.inputwildcard, args.outputfile[0])
