####################################################################################################
# Author: Thiago Castro Ferreira
# Date: 23/03/2017
# Description:
#    This script aims to train the models for compression and preordering both for lexicalised as
#    delexicalised data
####################################################################################################

corpus=/Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/data/alignments/split
path_lex=/Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/lex
path_delex=/Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex

# -Delex-Compress-Preorder
mkdir $path_lex/-Delex-Compress-Preorder/
mkdir $path_lex/-Delex-Compress-Preorder/model
python prepare_parallel.py \
       $corpus/training \
       $path_lex/-Delex-Compress-Preorder/train.de \
       $path_lex/-Delex-Compress-Preorder/train.en \
       $path_lex/-Delex-Compress-Preorder/model/aligned.grow-diag-final \
       --save_alignments

python prepare_parallel.py \
       $corpus/dev \
       $path_lex/-Delex-Compress-Preorder/dev.de \
       $path_lex/-Delex-Compress-Preorder/dev.en \
       $path_lex/-Delex-Compress-Preorder/model/aligned.grow-diag-final

python prepare_parallel.py \
       $corpus/test \
       $path_lex/-Delex-Compress-Preorder/test.de \
       $path_lex/-Delex-Compress-Preorder/test.en \
       $path_lex/-Delex-Compress-Preorder/model/aligned.grow-diag-final

# +Delex-Compress-Preorder
mkdir $path_delex/+Delex-Compress-Preorder/
mkdir $path_delex/+Delex-Compress-Preorder/model
mkdir $path_delex/+Delex-Compress-Preorder/realization
python prepare_parallel.py \
       $corpus/training \
       $path_delex/+Delex-Compress-Preorder/train.de \
       $path_delex/+Delex-Compress-Preorder/train.en \
       $path_delex/+Delex-Compress-Preorder/model/aligned.grow-diag-final \
       --delex \
       --lex $path_delex/+Delex-Compress-Preorder/train.lex \
       --references $path_delex/+Delex-Compress-Preorder/realization/train.cPickle \
       --save_alignments

python prepare_parallel.py \
       $corpus/dev \
       $path_delex/+Delex-Compress-Preorder/dev.de \
       $path_delex/+Delex-Compress-Preorder/dev.en \
       $path_delex/+Delex-Compress-Preorder/model/aligned.grow-diag-final \
       --delex \
       --lex $path_delex/+Delex-Compress-Preorder/dev.lex \
       --references $path_delex/+Delex-Compress-Preorder/realization/dev.cPickle

python prepare_parallel.py \
       $corpus/test \
       $path_delex/+Delex-Compress-Preorder/test.de \
       $path_delex/+Delex-Compress-Preorder/test.en \
       $path_delex/+Delex-Compress-Preorder/model/aligned.grow-diag-final \
       --delex \
       --lex $path_delex/+Delex-Compress-Preorder/test.lex \
       --references $path_delex/+Delex-Compress-Preorder/realization/test.cPickle

# -Delex+Compress-Preorder
mkdir $path_lex/-Delex+Compress-Preorder/
mkdir $path_lex/-Delex+Compress-Preorder/model
python prepare_parallel.py \
       $corpus/training \
       $path_lex/-Delex+Compress-Preorder/train.de \
       $path_lex/-Delex+Compress-Preorder/train.en \
       $path_lex/-Delex+Compress-Preorder/model/aligned.grow-diag-final \
       --compression \
       --crf_compressor $path_lex/compressor/train.out \
       --save_alignments

python prepare_parallel.py \
       $corpus/dev \
       $path_lex/-Delex+Compress-Preorder/dev.de \
       $path_lex/-Delex+Compress-Preorder/dev.en \
       $path_lex/-Delex+Compress-Preorder/model/aligned.grow-diag-final \
       --compression \
       --crf_compressor $path_lex/compressor/dev.out

python prepare_parallel.py \
       $corpus/test \
       $path_lex/-Delex+Compress-Preorder/test.de \
       $path_lex/-Delex+Compress-Preorder/test.en \
       $path_lex/-Delex+Compress-Preorder/model/aligned.grow-diag-final \
       --compression \
       --crf_compressor $path_lex/compressor/test.out

# +Delex+Compress-Preorder
mkdir $path_delex/+Delex+Compress-Preorder/
mkdir $path_delex/+Delex+Compress-Preorder/model
mkdir $path_delex/+Delex+Compress-Preorder/realization
python prepare_parallel.py \
       $corpus/training \
       $path_delex/+Delex+Compress-Preorder/train.de \
       $path_delex/+Delex+Compress-Preorder/train.en \
       $path_delex/+Delex+Compress-Preorder/model/aligned.grow-diag-final \
       --delex \
       --lex $path_delex/+Delex+Compress-Preorder/train.lex \
       --references $path_delex/+Delex+Compress-Preorder/realization/train.cPickle \
       --compression \
       --crf_compressor $path_delex/compressor/train.out \
       --save_alignments

python prepare_parallel.py \
       $corpus/dev \
       $path_delex/+Delex+Compress-Preorder/dev.de \
       $path_delex/+Delex+Compress-Preorder/dev.en \
       $path_delex/+Delex+Compress-Preorder/model/aligned.grow-diag-final \
       --delex \
       --lex $path_delex/+Delex+Compress-Preorder/dev.lex \
       --references $path_delex/+Delex+Compress-Preorder/realization/dev.cPickle \
       --compression \
       --crf_compressor $path_delex/compressor/dev.out

python prepare_parallel.py \
       $corpus/test \
       $path_delex/+Delex+Compress-Preorder/test.de \
       $path_delex/+Delex+Compress-Preorder/test.en \
       $path_delex/+Delex+Compress-Preorder/model/aligned.grow-diag-final \
       --delex \
       --lex $path_delex/+Delex+Compress-Preorder/test.lex \
       --references $path_delex/+Delex+Compress-Preorder/realization/test.cPickle \
       --compression \
       --crf_compressor $path_delex/compressor/test.out

# -Delex-Compress+Preorder
mkdir $path_lex/-Delex-Compress+Preorder/
mkdir $path_lex/-Delex-Compress+Preorder/model
python prepare_parallel.py \
       $corpus/training \
       $path_lex/-Delex-Compress+Preorder/train.de \
       $path_lex/-Delex-Compress+Preorder/train.en \
       $path_lex/-Delex-Compress+Preorder/model/aligned.grow-diag-final \
       --linearization \
       --one_step $path_lex/preorder/clf_one_step.cPickle \
       --two_step $path_lex/preorder/clf_two_step.cPickle \
       --save_alignments

python prepare_parallel.py \
       $corpus/dev \
       $path_lex/-Delex-Compress+Preorder/dev.de \
       $path_lex/-Delex-Compress+Preorder/dev.en \
       $path_lex/-Delex-Compress+Preorder/model/aligned.grow-diag-final \
       --linearization \
       --one_step $path_lex/preorder/clf_one_step.cPickle \
       --two_step $path_lex/preorder/clf_two_step.cPickle

python prepare_parallel.py \
       $corpus/test \
       $path_lex/-Delex-Compress+Preorder/test.de \
       $path_lex/-Delex-Compress+Preorder/test.en \
       $path_lex/-Delex-Compress+Preorder/model/aligned.grow-diag-final \
       --linearization \
       --one_step $path_lex/preorder/clf_one_step.cPickle \
       --two_step $path_lex/preorder/clf_two_step.cPickle

# +Delex-Compress+Preorder
mkdir $path_delex/+Delex-Compress+Preorder/
mkdir $path_delex/+Delex-Compress+Preorder/model
mkdir $path_delex/+Delex-Compress+Preorder/realization
python prepare_parallel.py \
       $corpus/training \
       $path_delex/+Delex-Compress+Preorder/train.de \
       $path_delex/+Delex-Compress+Preorder/train.en \
       $path_delex/+Delex-Compress+Preorder/model/aligned.grow-diag-final \
       --delex \
       --lex $path_delex/+Delex-Compress+Preorder/train.lex \
       --references $path_delex/+Delex-Compress+Preorder/realization/train.cPickle \
       --linearization \
       --one_step $path_delex/preorder/clf_one_step.cPickle \
       --two_step $path_delex/preorder/clf_two_step.cPickle \
       --save_alignments

python prepare_parallel.py \
       $corpus/dev \
       $path_delex/+Delex-Compress+Preorder/dev.de \
       $path_delex/+Delex-Compress+Preorder/dev.en \
       $path_delex/+Delex-Compress+Preorder/model/aligned.grow-diag-final \
       --delex \
       --lex $path_delex/+Delex-Compress+Preorder/dev.lex \
       --references $path_delex/+Delex-Compress+Preorder/realization/dev.cPickle \
       --linearization \
       --one_step $path_delex/preorder/clf_one_step.cPickle \
       --two_step $path_delex/preorder/clf_two_step.cPickle

python prepare_parallel.py \
       $corpus/test \
       $path_delex/+Delex-Compress+Preorder/test.de \
       $path_delex/+Delex-Compress+Preorder/test.en \
       $path_delex/+Delex-Compress+Preorder/model/aligned.grow-diag-final \
       --delex \
       --lex $path_delex/+Delex-Compress+Preorder/test.lex \
       --references $path_delex/+Delex-Compress+Preorder/realization/test.cPickle \
       --linearization \
       --one_step $path_delex/preorder/clf_one_step.cPickle \
       --two_step $path_delex/preorder/clf_two_step.cPickle

# -Delex+Compress+Preorder
mkdir $path_lex/-Delex+Compress+Preorder/
mkdir $path_lex/-Delex+Compress+Preorder/model
python prepare_parallel.py \
       $corpus/training \
       $path_lex/-Delex+Compress+Preorder/train.de \
       $path_lex/-Delex+Compress+Preorder/train.en \
       $path_lex/-Delex+Compress+Preorder/model/aligned.grow-diag-final \
       --compression \
       --crf_compressor $path_lex/compressor/train.out \
       --linearization \
       --one_step $path_lex/preorder/clf_one_step.cPickle \
       --two_step $path_lex/preorder/clf_two_step.cPickle \
       --save_alignments

python prepare_parallel.py \
       $corpus/dev \
       $path_lex/-Delex+Compress+Preorder/dev.de \
       $path_lex/-Delex+Compress+Preorder/dev.en \
       $path_lex/-Delex+Compress+Preorder/model/aligned.grow-diag-final \
       --compression \
       --crf_compressor $path_lex/compressor/dev.out \
       --linearization \
       --one_step $path_lex/preorder/clf_one_step.cPickle \
       --two_step $path_lex/preorder/clf_two_step.cPickle

python prepare_parallel.py \
       $corpus/test \
       $path_lex/-Delex+Compress+Preorder/test.de \
       $path_lex/-Delex+Compress+Preorder/test.en \
       $path_lex/-Delex+Compress+Preorder/model/aligned.grow-diag-final \
       --compression \
       --crf_compressor $path_lex/compressor/test.out \
       --linearization \
       --one_step $path_lex/preorder/clf_one_step.cPickle \
       --two_step $path_lex/preorder/clf_two_step.cPickle

# +Delex+Compress+Preorder
mkdir $path_delex/+Delex+Compress+Preorder/
mkdir $path_delex/+Delex+Compress+Preorder/model
mkdir $path_delex/+Delex+Compress+Preorder/realization
python prepare_parallel.py \
       $corpus/training \
       $path_delex/+Delex+Compress+Preorder/train.de \
       $path_delex/+Delex+Compress+Preorder/train.en \
       $path_delex/+Delex+Compress+Preorder/model/aligned.grow-diag-final \
       --delex \
       --lex $path_delex/+Delex+Compress+Preorder/train.lex \
       --references $path_delex/+Delex+Compress+Preorder/realization/train.cPickle \
       --compression \
       --crf_compressor $path_delex/compressor/train.out \
       --linearization \
       --one_step $path_delex/preorder/clf_one_step.cPickle \
       --two_step $path_delex/preorder/clf_two_step.cPickle \
       --save_alignments

python prepare_parallel.py \
       $corpus/dev \
       $path_delex/+Delex+Compress+Preorder/dev.de \
       $path_delex/+Delex+Compress+Preorder/dev.en \
       $path_delex/+Delex+Compress+Preorder/model/aligned.grow-diag-final \
       --delex \
       --lex $path_delex/+Delex+Compress+Preorder/dev.lex \
       --references $path_delex/+Delex+Compress+Preorder/realization/dev.cPickle \
       --compression \
       --crf_compressor $path_lex/compressor/dev.out \
       --linearization \
       --one_step $path_delex/preorder/clf_one_step.cPickle \
       --two_step $path_delex/preorder/clf_two_step.cPickle

python prepare_parallel.py \
       $corpus/test \
       $path_delex/+Delex+Compress+Preorder/test.de \
       $path_delex/+Delex+Compress+Preorder/test.en \
       $path_delex/+Delex+Compress+Preorder/model/aligned.grow-diag-final \
       --delex \
       --lex $path_delex/+Delex+Compress+Preorder/test.lex \
       --references $path_delex/+Delex+Compress+Preorder/realization/test.cPickle \
       --compression \
       --crf_compressor $path_delex/compressor/test.out \
       --linearization \
       --one_step $path_delex/preorder/clf_one_step.cPickle \
       --two_step $path_delex/preorder/clf_two_step.cPickle