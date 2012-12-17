from common import dgiter, DependencyGraph

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
			
def parse_and_store(finput, foutput, model = rhead):
	with open(foutput,"w") as fp:
		fp.write("\n\n".join(str(model(dg)) for dg in dgiter(finput)))
		
if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser(description='General some popular baseline parsings for given corpus files')
	parser.add_argument('finput', metavar='input', type=str, nargs=1,
                   help='Source CoNLL corpus file including gold dependency graphs')
        parser.add_argument('foutput', metavar='output', type=str, nargs=1,
                   help='Model CoNLL corpus file including model dependency grapgs')
        group = parser.add_mutually_exclusive_group()
        group.add_argument('--rhead', action='store_true',help="Right head parsing")
	group.add_argument('--lhead', action='store_true',help="Left head parsing")
	args = parser.parse_args()
	
	if args.rhead:
		parse_and_store(args.finput[0], args.foutput[0],rhead)
	else:
		parse_and_store(args.finput[0], args.foutput[0],lhead)
