TASK_IDENTIFIER=gold
TRANSFORMOPT=

#CONLL_DIR=/home/ubuntu/data/nlp/treebank/treebank-2.0/combined/conll
CONLL_DIR=/Users/husnusensoy/uparse/data/nlp/treebank/treebank-2.0/combined/conll

DEV=conll.$(TASK_IDENTIFIER).dev
TRAIN=conll.$(TASK_IDENTIFIER).train
TEST=conll.$(TASK_IDENTIFIER).test


all: result.$(TASK_IDENTIFIER).tar.gz

# Task .dev .train and .test files
$(DEV) $(TRAIN) $(TEST): ${CONLL_DIR}
	./conll.py --directory ${CONLL_DIR} ${TRANSFORMOPT} --section 2-21 > ${TRAIN}
	./conll.py --directory ${CONLL_DIR} ${TRANSFORMOPT} --section 22 > ${DEV}
	./conll.py --directory ${CONLL_DIR} ${TRANSFORMOPT} --section 23 > ${TEST}

# Extract maltparser, maltoptimizer, and malteval
maltbundle.$(TASK_IDENTIFIER).task: maltbundle.tar.gz
	rm -rf $@
	mkdir $@
	tar -xzvf maltbundle.tar.gz -C $@

# Run your experiment
result.$(TASK_IDENTIFIER).tar.gz: ${DEV} maltbundle.$(TASK_IDENTIFIER).task
	make -C maltbundle.$(TASK_IDENTIFIER).task/bundle DEV=../../${DEV} TRAIN=../../${TRAIN} TEST=../../${TEST}
	rm -r maltbundle.$(TASK_IDENTIFIER).task
	mv -n result.tar.gz $@

