import glob
import os
import time
from util import run_command,secondsToStr
from string import Template
from multiprocessing import Pool
pennconverter = Template('java -jar $pennconverterdir/pennconverter.jar -f $penntreefile -t $conllfile -splitSlash=false')

dpfilename = lambda fname: "%s.dp"%fname
mrgfilename = lambda fname: "%s.mrg"%fname
noext = lambda fname: os.path.splitext(os.path.basename(fname))[0]

def mkdir(conlldir, sectiondir):
	try:
		os.makedirs(os.path.join(conlldir,sectiondir))
	except:
		pass

def generate(treebankdir, conlldir, sections, parallelism):
	p = Pool(parallelism)
	sectioniter = range(25) if len(sections) == 0 else sections
	
	for s in sectioniter:
		sectionDir = str(s).zfill(2)

		mkdir(conlldir,sectionDir)
		tstart = time.time()


		for sourcefile in glob.glob('/'.join([os.path.join(treebankdir, sectionDir),mrgfilename('*')])):
			basefilename = os.path.basename(sourcefile)

			run_command(pennconverter.substitute(pennconverterdir='.',penntreefile=sourcefile, conllfile=os.path.join(conlldir,sectionDir)+'/'+ dpfilename(noext(basefilename))), False)
		tend = time.time()
		print "Generated section %s in %s"%(sectionDir,secondsToStr(tend-tstart))
		
	
if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser(description='Generate CoNLL format by reading penntreebank trees')
	parser.add_argument('treebankdir', metavar='input', type=str, nargs=1,
                   help='Treebank directory containing sections of penntree corpus')
        parser.add_argument('conlldir', metavar='output', type=str, nargs=1,
                   help='Target CoNLL directory')
      	parser.add_argument('sections', metavar='sections', type=int, nargs='*',
                   help='Section filter for generation')
      	parser.add_argument('--parallel', metavar='parallel', type=int, default=1,
                   help='Number of parallel slaves to perform conversion')
	args = parser.parse_args()
	
	print args
	
	generate(args.treebankdir[0], args.conlldir[0],args.sections,args.parallel)
	
	
