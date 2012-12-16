from common import dgiter, Metrics
def evaluate( fgold, fmodel, ignoreroot=True ):
	m = Metrics(ignoreroot)
	
	for dggold,dgmodel in zip(dgiter(fgold), dgiter(fmodel)):
		m.add(dggold, dgmodel)
	
	print str(m)
	
	
if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser(description='Evaluate two parsings')
	parser.add_argument('goldfile', type=str,
                   help='Source CoNLL corpus file including gold dependency graphs')
        parser.add_argument('modelfile', type=str,
                   help='Model CoNLL corpus file including model dependency grapgs')
        parser.add_argument('--ignoreroot', action='store_true')
	args = parser.parse_args()
	
	print args
	
	evaluate(args.goldfile, args.modelfile, args.ignoreroot)
