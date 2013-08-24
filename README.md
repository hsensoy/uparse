## uparse

### Dependency Parsing Experiments using Makefile
`Makefile` included in `uparse` directory allows you to perform several dependency parsing experiments using `MaltOptimizer` and `Maltparser`

To perform experiments, edit Makefile to set `CONLL_DIR` location to your CoNLL format pentreebank corpus location. Directory you will provide should include a separate directory for each section of the corpus (00-24)

Now you can start experiments. Here are a few make calls for the experiments

* `make all` will execute a default experiment by performing parameter optimisation using `section 22`, train an optimised dependency parser using `sections 2-21` and test the parser using `section 23`
* `make all TASK_IDENTIFIER=ws.50 TRANSFORMOPT="--tagmode tagfile --tagfile ../data/upos/ws.50.gz"` will first replace all tags/cpostags in given corpus by tags given with `--tagfile` option and will initiate `make all`

All experiments will create a `result.<TASK_IDENTIFIER>.tar.gz` file into `uparse` directory. This file contains

* `model.eval` including LA, LAS, UAS performance metrics
* `model.out` including parser output for `section 23`
* `phase3_optFile.txt` including Maltparser options
* `addMergPOSTAGI0FORMStack0.xml` including features to be used by Maltparser.

### conll.py
```
usage: conll.py [-h] [--file FILE] [--directory DIRECTORY]
                [--extension EXTENSION] [--section SECTION]
                [--tagmode {nochange,tagfile,onetagperword,remove,random}]
                [--tagfile TAGFILE] [--ambigious]
                [--formmode {nochange,formfile,remove}] [--formfile FORMFILE]
                [--subsmode {nochange,best}] [--subsfile SUBSFILE]

CoNLL file transformer

optional arguments:
  -h, --help            show this help message and exit
  --file FILE           CoNLL files to read
  --directory DIRECTORY
                        CoNLL directory to read
  --extension EXTENSION
                        CoNLL file extension to read
  --section SECTION     WSJ sections to be filtered out
  --tagmode {nochange,tagfile,onetagperword,remove,random}
                        Tag manipulation operation on corpus
  --tagfile TAGFILE     Tag file to be used. Only valid when used with
                        --tagmode tagfile|random
  --ambigious           Threat tags as ambigious by not using a dictionary
  --formmode {nochange,formfile,remove}
                        Form manipulation operation on corpus
  --formfile FORMFILE   Form file to be used. Only valid when used with
                        --formmode formfile
  --subsmode {nochange,best}
                        Form manipulation operation on corpus
  --subsfile SUBSFILE   Substitution file to be used. Only valid when used
                        with --subsmode formfile
```
### filter.py
```
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
```

### eval.py
```
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
```

### parser.py

```
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
```

### genconll.py

```
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
```

###PCFG

`./treetransform.py  --brush --cnf ./data/treebank/treebank.mrg > ./data/json/_penntreebank.json`

`./retag.py --noextendedtag ./data/json/_penntreebank.json > ./data/json/penntreebank.json`

`./retag.py --tagfile ./data/upos/ws.100.gz ./data/nlp/treebank/treebank-2.0/json/wsj/wsj.json > ./data/nlp/treebank/treebank-2.0/json/wsj/wsj.ws.100.json`

`./split.py --tagged --maxlength 40 0.80 ./data/nlp/treebank/treebank-2.0/json/wsj/wsj.json`

`./count_cfg_freq.py ./data/nlp/treebank/treebank-2.0/json/wsj/wsj.train > penntreebank.counts`

`./pcfg_parse.py --parallel 8 penntreebank.counts ./data/nlp/treebank/treebank-2.0/json/wsj/wsj.dev > ./data/nlp/treebank/treebank-2.0/json/wsj/wsj.p1.out`

`./eval_parser.py ./data/nlp/treebank/treebank-2.0/json/wsj/wsj.key data/nlp/treebank/treebank-2.0/json/wsj/wsj.p1.out`

