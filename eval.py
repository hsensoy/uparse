from common import dgiter, Metrics
import warnings
def evaluate( fgold, fmodel, ignoreroot=True,minlength=1 ):
	m = Metrics(ignoreroot)
	
	for dggold,dgmodel in zip(dgiter(fgold), dgiter(fmodel)):
		if dggold.length() >= minlength:
			if not dggold.__eq__(dgmodel):
				warnings.warn("Two sentences are not equal %s %s"%(str(dggold),str(dgmodel)))
				
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
        parser.add_argument('--minlength', type=int,default = 1,
                   help='Minimum sentence length to be considered in evaluation')
	args = parser.parse_args()
	
	print args
	
	evaluate(args.goldfile, args.modelfile, args.ignoreroot,args.minlength)
