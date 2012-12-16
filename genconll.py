import os
def generate(treebank, conll):
	print filter(os.path.isdir, os.listdir(treebank[0]))
	print treebank[0], conll
	
if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser(description='Generate CoNLL format by reading penntreebank trees')
	parser.add_argument('treebankdir', metavar='input', type=str, nargs=1,
                   help='Treebank directory containing sections of penntree corpus')
        parser.add_argument('conlldir', metavar='output', type=str, nargs=1,
                   help='Target CoNLL directory')
	args = parser.parse_args()
	
	generate(args.treebankdir, args.conlldir)
