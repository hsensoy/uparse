uparse
======
$ python2.7 filter.py -h
usage: filter.py [-h] [--wsj10 | --wsj20 | --wsj40 | --wsj]
                 inputwildcard output

Cleanup & Filter CoNLL corpus

positional arguments:
  inputwildcard  File wildcard showing CoNLL corpus file(s) including one or
                 more dependency graphs
  output         Target CoNLL corpus file used to store clean and filtered
                 CoNLL corpus

optional arguments:
  -h, --help     show this help message and exit
  --wsj10        Cleaned sentences of maximum length 10
  --wsj20        Cleaned sentences of maximum length 20
  --wsj40        Cleaned sentences of maximum length 40
  --wsj          Cleaned sentences of full corpus

======

$ python2.7 eval.py -h
usage: eval.py [-h] [--ignoreroot] goldfile modelfile

Evaluate two parsings

positional arguments:
  goldfile      Source CoNLL corpus file including gold dependency graphs
  modelfile     Model CoNLL corpus file including model dependency grapgs

optional arguments:
  -h, --help    show this help message and exit
  --ignoreroot

======

$ python2.7 parser.py -h
usage: parser.py [-h] [--rhead | --lhead] input output

General some popular baseline parsings for given corpus files

positional arguments:
  input       Source CoNLL corpus file including gold dependency graphs
  output      Model CoNLL corpus file including model dependency grapgs

optional arguments:
  -h, --help  show this help message and exit
  --rhead     Right head parsing
  --lhead     Left head parsing

======

$ python2.7 genconll.py -h
usage: genconll.py [-h] [--parallel parallel]
                   input output [sections [sections ...]]

Generate CoNLL format by reading penntreebank trees

positional arguments:
  input                Treebank directory containing sections of penntree
                       corpus
  output               Target CoNLL directory
  sections             Section filter for generation

optional arguments:
  -h, --help           show this help message and exit
  --parallel parallel  Number of parallel slaves to perform conversion
