corpus=/Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/data/alignments/split
path_lex=/Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/lex
path_delex=/Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex

mkdir $path_lex
mkdir $path_delex

cd compression_crf

# LEXICALISED CLASSIFIERS
compressor=$path_lex/compressor
preorder=$path_lex/preorder

mkdir $compressor
mkdir $preorder

python preprocessing.py \
        $corpus/training \
        $corpus/dev \
        $corpus/test \
        $compressor/train.feat \
        $compressor/dev.feat \
        $compressor/test.feat


python chunking.py < $compressor/train.feat > $compressor/train.crfsuite.txt
python chunking.py < $compressor/dev.feat > $compressor/dev.crfsuite.txt
python chunking.py < $compressor/test.feat > $compressor/test.crfsuite.txt

crfsuite learn -m $compressor/compressor.model -e2 $compressor/train.crfsuite.txt $compressor/dev.crfsuite.txt

crfsuite tag -m $compressor/compressor.model $compressor/train.crfsuite.txt > $compressor/train.out
crfsuite tag -m $compressor/compressor.model $compressor/dev.crfsuite.txt > $compressor/dev.out
crfsuite tag -m $compressor/compressor.model $compressor/test.crfsuite.txt > $compressor/test.out

cd ../linearizer
python classifier.py \
		$corpus/training \
		$corpus/dev \
		$corpus/test \
		$preorder

# DELEX
compressor=$path_delex/compressor
preorder=$path_delex/preorder

mkdir $compressor
mkdir $preorder

cd ../compression_crf
python preprocessing.py \
        $corpus/training \
        $corpus/dev \
        $corpus/test \
        $compressor/train.feat \
        $compressor/dev.feat \
        $compressor/test.feat \
        --delex

python chunking.py < $compressor/train.feat > $compressor/train.crfsuite.txt
python chunking.py < $compressor/dev.feat > $compressor/dev.crfsuite.txt
python chunking.py < $compressor/test.feat > $compressor/test.crfsuite.txt

crfsuite learn -m $compressor/compressor.model -e2 $compressor/train.crfsuite.txt $compressor/dev.crfsuite.txt

crfsuite tag -m $compressor/compressor.model $compressor/train.crfsuite.txt > $compressor/train.out
crfsuite tag -m $compressor/compressor.model $compressor/dev.crfsuite.txt > $compressor/dev.out
crfsuite tag -m $compressor/compressor.model $compressor/test.crfsuite.txt > $compressor/test.out

cd ../linearizer
python classifier.py \
                $corpus/training \
                $corpus/dev \
                $corpus/test \
                $preorder \
                --delex