if [ -z "$1" ]; then
    echo "You need at least 1 argument"
    exit
fi

if [ -z "$2" ]; then
    for i in 1 2 3 4 5
    do
        echo $i th cross-validation out of 5
        ./splitNfold.py --n $i --total 5 $1.key
        
        echo Counting rule frequencies
        ./collins/count_cfg_freq.py $1.training.$i.of.5.key > $1.counts
        echo Parsing sentences
        ./pcfg_parse.py --rules $1.counts $1.validation.$i.of.5.key > $1.out
        echo Evaluating the parser
        ./collins/eval_parser.py $1.validation.$i.of.5.key $1.out > $1.scores.fold.$i.of.5
        tail -1 $1.scores.fold.$i.of.5
        echo Refer to $1.scores.fold.$i.of.5 for tag level scores
    done
else
    echo Retagging the sentences using tags in $2.gz
    ./retag.py --tagfile $2.gz $1.key > $1.$2.key
    echo Counting rule frequencies
    ./collins/count_cfg_freq.py $1.$2.key > $1.$2.counts
    echo Parsing sentences
    ./pcfg_parse.py --rules $1.$2.counts $1.$2.key > $1.$2.out
    echo Evaluating the parser
    ./collins/eval_parser.py $1.$2.key $1.$2.out > $1.$2.scores
    tail -1 $1.$2.scores
    echo Refer to $1.$2.scores for tag level scores
fi
