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
usage: eval.py [-h] [--ignoreroot] [--minlength MINLENGTH] goldfile modelfile

Evaluate two parsings

positional arguments:
  goldfile              Source CoNLL corpus file including gold dependency
                        graphs
  modelfile             Model CoNLL corpus file including model dependency
                        grapgs

optional arguments:
  -h, --help            show this help message and exit
  --ignoreroot
  --minlength MINLENGTH
                        Minimum sentence length to be considered in evaluation
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


PCFG

./treetransform.py  --brush --cnf ./data/treebank/treebank.mrg > ./data/json/_penntreebank.json
./retag.py --noextendedtag ./data/json/_penntreebank.json > ./data/json/penntreebank.json
./retag.py --tagfile ./data/upos/ws.100.gz ./data/nlp/treebank/treebank-2.0/json/wsj/wsj.json > ./data/nlp/treebank/treebank-2.0/json/wsj/wsj.ws.100.json
./split.py --tagged --maxlength 40 0.80 ./data/nlp/treebank/treebank-2.0/json/wsj/wsj.json
./count_cfg_freq.py ./data/nlp/treebank/treebank-2.0/json/wsj/wsj.train > penntreebank.counts
./pcfg_parse.py --parallel 8 penntreebank.counts ./data/nlp/treebank/treebank-2.0/json/wsj/wsj.dev > ./data/nlp/treebank/treebank-2.0/json/wsj/wsj.p1.out
./eval_parser.py ./data/nlp/treebank/treebank-2.0/json/wsj/wsj.key data/nlp/treebank/treebank-2.0/json/wsj/wsj.p1.out
