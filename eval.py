from common import Metrics, Measure
from corpus import idg, itree, isdgcorpus
import warnings

def evaluateDG( fgold, fmodel, ignoreroot=True,minlength=1 ):
	m = Metrics(ignoreroot)
	
	for dggold,dgmodel in zip( idg(fgold), idg(fmodel)):
		if dggold.length() >= minlength:
			if not dggold.__eq__(dgmodel):
				warnings.warn("Two sentences are not equal %s %s"%(str(dggold),str(dgmodel)))
				
			m.add(dggold, dgmodel)
	
	print str(m)

def evaluateTree( fgold, fmodel,minlength=1 ):
	measure = Measure()
	
	with open(fgold) as g_fp, open(fmodel) as m_fp:
		for g_line, m_line in zip( g_fp, m_fp ):
			g = g_line.strip().split(':')
			g_count = int(g[0])
			exec( "g_set=set([%s])"%g[1] )
			
			m = m_line.strip().split(':')
			m_count = int(m[0])
			exec( "m_set=set([%s])"%m[1] )
			
			assert m_count == g_count
			if m_count >= minlength and g_count >= minlength:
				measure.add(g_set, m_set)
	
	print str(measure)
	
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

	if isdgcorpus(args.goldfile) and isdgcorpus(args.modelfile):
		evaluateDG(args.goldfile, args.modelfile, args.ignoreroot,args.minlength)
	elif not isdgcorpus(args.goldfile) and not isdgcorpus(args.modelfile):
		evaluateTree(args.goldfile, args.modelfile, args.minlength)
	else:
		warnings.warn("Both file should be of same corpus type")
	
	
