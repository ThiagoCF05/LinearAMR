# -Delex-Compress-Preorder
mkdir /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/lex/-Delex-Compress-Preorder/
mkdir /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/lex/-Delex-Compress-Preorder/model
python prepare_parallel.py \
       /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/data/alignments/split/training \
       /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/lex/-Delex-Compress-Preorder/train.de \
       /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/lex/-Delex-Compress-Preorder/train.en \
       /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/lex/-Delex-Compress-Preorder/model/aligned.grow-diag-final \
       --save_alignments

python prepare_parallel.py \
       /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/data/alignments/split/dev \
       /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/lex/-Delex-Compress-Preorder/dev.de \
       /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/lex/-Delex-Compress-Preorder/dev.en \
       /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/lex/-Delex-Compress-Preorder/model/aligned.grow-diag-final

python prepare_parallel.py \
       /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/data/alignments/split/test \
       /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/lex/-Delex-Compress-Preorder/test.de \
       /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/lex/-Delex-Compress-Preorder/test.en \
       /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/lex/-Delex-Compress-Preorder/model/aligned.grow-diag-final

# +Delex-Compress-Preorder
mkdir /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/+Delex-Compress-Preorder/
mkdir /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/+Delex-Compress-Preorder/model
mkdir /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/+Delex-Compress-Preorder/realization
python prepare_parallel.py \
       /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/data/alignments/split/training \
       /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/+Delex-Compress-Preorder/train.de \
       /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/+Delex-Compress-Preorder/train.en \
       /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/+Delex-Compress-Preorder/model/aligned.grow-diag-final \
       --delex \
       --lex /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/+Delex-Compress-Preorder/train.lex \
       --references /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/+Delex-Compress-Preorder/realization/train.cPickle \
       --save_alignments

python prepare_parallel.py \
       /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/data/alignments/split/dev \
       /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/+Delex-Compress-Preorder/dev.de \
       /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/+Delex-Compress-Preorder/dev.en \
       /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/+Delex-Compress-Preorder/model/aligned.grow-diag-final \
       --delex \
       --lex /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/+Delex-Compress-Preorder/dev.lex \
       --references /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/+Delex-Compress-Preorder/realization/dev.cPickle

python prepare_parallel.py \
       /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/data/alignments/split/test \
       /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/+Delex-Compress-Preorder/test.de \
       /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/+Delex-Compress-Preorder/test.en \
       /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/+Delex-Compress-Preorder/model/aligned.grow-diag-final \
       --delex \
       --lex /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/+Delex-Compress-Preorder/test.lex \
       --references /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/+Delex-Compress-Preorder/realization/test.cPickle

# -Delex+Compress-Preorder
mkdir /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/lex/-Delex+Compress-Preorder/
mkdir /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/lex/-Delex+Compress-Preorder/model
python prepare_parallel.py \
       /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/data/alignments/split/training \
       /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/lex/-Delex+Compress-Preorder/train.de \
       /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/lex/-Delex+Compress-Preorder/train.en \
       /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/lex/-Delex+Compress-Preorder/model/aligned.grow-diag-final \
       --compression \
       --crf_compressor /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/lex/compressor/train.out \
       --save_alignments

python prepare_parallel.py \
       /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/data/alignments/split/dev \
       /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/lex/-Delex+Compress-Preorder/dev.de \
       /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/lex/-Delex+Compress-Preorder/dev.en \
       /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/lex/-Delex+Compress-Preorder/model/aligned.grow-diag-final \
       --compression \
       --crf_compressor /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/lex/compressor/dev.out

python prepare_parallel.py \
       /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/data/alignments/split/test \
       /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/lex/-Delex+Compress-Preorder/test.de \
       /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/lex/-Delex+Compress-Preorder/test.en \
       /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/lex/-Delex+Compress-Preorder/model/aligned.grow-diag-final \
       --compression \
       --crf_compressor /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/lex/compressor/test.out

# +Delex+Compress-Preorder
mkdir /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/+Delex+Compress-Preorder/
mkdir /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/+Delex+Compress-Preorder/model
mkdir /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/+Delex+Compress-Preorder/realization
python prepare_parallel.py \
       /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/data/alignments/split/training \
       /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/+Delex+Compress-Preorder/train.de \
       /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/+Delex+Compress-Preorder/train.en \
       /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/+Delex+Compress-Preorder/model/aligned.grow-diag-final \
       --delex \
       --lex /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/+Delex+Compress-Preorder/train.lex \
       --references /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/+Delex+Compress-Preorder/realization/train.cPickle \
       --compression \
       --crf_compressor /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/compressor/train.out \
       --save_alignments

python prepare_parallel.py \
       /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/data/alignments/split/dev \
       /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/+Delex+Compress-Preorder/dev.de \
       /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/+Delex+Compress-Preorder/dev.en \
       /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/+Delex+Compress-Preorder/model/aligned.grow-diag-final \
       --delex \
       --lex /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/+Delex+Compress-Preorder/dev.lex \
       --references /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/+Delex+Compress-Preorder/realization/dev.cPickle \
       --compression \
       --crf_compressor /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/compressor/dev.out

python prepare_parallel.py \
       /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/data/alignments/split/test \
       /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/+Delex+Compress-Preorder/test.de \
       /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/+Delex+Compress-Preorder/test.en \
       /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/+Delex+Compress-Preorder/model/aligned.grow-diag-final \
       --delex \
       --lex /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/+Delex+Compress-Preorder/test.lex \
       --references /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/+Delex+Compress-Preorder/realization/test.cPickle \
       --compression \
       --crf_compressor /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/compressor/test.out

# -Delex-Compress+Preorder
mkdir /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/lex/-Delex-Compress+Preorder/
mkdir /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/lex/-Delex-Compress+Preorder/model
python prepare_parallel.py \
       /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/data/alignments/split/training \
       /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/lex/-Delex-Compress+Preorder/train.de \
       /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/lex/-Delex-Compress+Preorder/train.en \
       /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/lex/-Delex-Compress+Preorder/model/aligned.grow-diag-final \
       --linearization \
       --one_step /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/lex/preorder/clf_one_step.cPickle \
       --two_step /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/lex/preorder/clf_two_step.cPickle \
       --save_alignments

python prepare_parallel.py \
       /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/data/alignments/split/dev \
       /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/lex/-Delex-Compress+Preorder/dev.de \
       /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/lex/-Delex-Compress+Preorder/dev.en \
       /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/lex/-Delex-Compress+Preorder/model/aligned.grow-diag-final \
       --linearization \
       --one_step /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/lex/preorder/clf_one_step.cPickle \
       --two_step /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/lex/preorder/clf_two_step.cPickle

python prepare_parallel.py \
       /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/data/alignments/split/test \
       /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/lex/-Delex-Compress+Preorder/test.de \
       /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/lex/-Delex-Compress+Preorder/test.en \
       /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/lex/-Delex-Compress+Preorder/model/aligned.grow-diag-final \
       --linearization \
       --one_step /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/lex/preorder/clf_one_step.cPickle \
       --two_step /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/lex/preorder/clf_two_step.cPickle

# +Delex-Compress+Preorder
mkdir /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/+Delex-Compress+Preorder/
mkdir /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/+Delex-Compress+Preorder/model
mkdir /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/+Delex-Compress+Preorder/realization
python prepare_parallel.py \
       /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/data/alignments/split/training \
       /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/+Delex-Compress+Preorder/train.de \
       /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/+Delex-Compress+Preorder/train.en \
       /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/+Delex-Compress+Preorder/model/aligned.grow-diag-final \
       --delex \
       --lex /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/+Delex-Compress+Preorder/train.lex \
       --references /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/+Delex-Compress+Preorder/realization/train.cPickle \
       --linearization \
       --one_step /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/preorder/clf_one_step.cPickle \
       --two_step /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/preorder/clf_two_step.cPickle \
       --save_alignments

python prepare_parallel.py \
       /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/data/alignments/split/dev \
       /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/+Delex-Compress+Preorder/dev.de \
       /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/+Delex-Compress+Preorder/dev.en \
       /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/+Delex-Compress+Preorder/model/aligned.grow-diag-final \
       --delex \
       --lex /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/+Delex-Compress+Preorder/dev.lex \
       --references /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/+Delex-Compress+Preorder/realization/dev.cPickle \
       --linearization \
       --one_step /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/preorder/clf_one_step.cPickle \
       --two_step /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/preorder/clf_two_step.cPickle

python prepare_parallel.py \
       /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/data/alignments/split/test \
       /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/+Delex-Compress+Preorder/test.de \
       /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/+Delex-Compress+Preorder/test.en \
       /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/+Delex-Compress+Preorder/model/aligned.grow-diag-final \
       --delex \
       --lex /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/+Delex-Compress+Preorder/test.lex \
       --references /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/+Delex-Compress+Preorder/realization/test.cPickle \
       --linearization \
       --one_step /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/preorder/clf_one_step.cPickle \
       --two_step /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/preorder/clf_two_step.cPickle

# -Delex+Compress+Preorder
mkdir /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/lex/-Delex+Compress+Preorder/
mkdir /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/lex/-Delex+Compress+Preorder/model
python prepare_parallel.py \
       /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/data/alignments/split/training \
       /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/lex/-Delex+Compress+Preorder/train.de \
       /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/lex/-Delex+Compress+Preorder/train.en \
       /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/lex/-Delex+Compress+Preorder/model/aligned.grow-diag-final \
       --compression \
       --crf_compressor /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/lex/compressor/train.out \
       --linearization \
       --one_step /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/lex/preorder/clf_one_step.cPickle \
       --two_step /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/lex/preorder/clf_two_step.cPickle \
       --save_alignments

python prepare_parallel.py \
       /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/data/alignments/split/dev \
       /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/lex/-Delex+Compress+Preorder/dev.de \
       /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/lex/-Delex+Compress+Preorder/dev.en \
       /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/lex/-Delex+Compress+Preorder/model/aligned.grow-diag-final \
       --compression \
       --crf_compressor /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/lex/compressor/dev.out \
       --linearization \
       --one_step /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/lex/preorder/clf_one_step.cPickle \
       --two_step /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/lex/preorder/clf_two_step.cPickle

python prepare_parallel.py \
       /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/data/alignments/split/test \
       /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/lex/-Delex+Compress+Preorder/test.de \
       /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/lex/-Delex+Compress+Preorder/test.en \
       /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/lex/-Delex+Compress+Preorder/model/aligned.grow-diag-final \
       --compression \
       --crf_compressor /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/lex/compressor/test.out \
       --linearization \
       --one_step /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/lex/preorder/clf_one_step.cPickle \
       --two_step /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/lex/preorder/clf_two_step.cPickle

# +Delex+Compress+Preorder
mkdir /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/+Delex+Compress+Preorder/
mkdir /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/+Delex+Compress+Preorder/model
mkdir /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/+Delex+Compress+Preorder/realization
python prepare_parallel.py \
       /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/data/alignments/split/training \
       /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/+Delex+Compress+Preorder/train.de \
       /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/+Delex+Compress+Preorder/train.en \
       /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/+Delex+Compress+Preorder/model/aligned.grow-diag-final \
       --delex \
       --lex /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/+Delex+Compress+Preorder/train.lex \
       --references /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/+Delex+Compress+Preorder/realization/train.cPickle \
       --compression \
       --crf_compressor /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/compressor/train.out \
       --linearization \
       --one_step /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/preorder/clf_one_step.cPickle \
       --two_step /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/preorder/clf_two_step.cPickle \
       --save_alignments

python prepare_parallel.py \
       /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/data/alignments/split/dev \
       /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/+Delex+Compress+Preorder/dev.de \
       /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/+Delex+Compress+Preorder/dev.en \
       /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/+Delex+Compress+Preorder/model/aligned.grow-diag-final \
       --delex \
       --lex /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/+Delex+Compress+Preorder/dev.lex \
       --references /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/+Delex+Compress+Preorder/realization/dev.cPickle \
       --compression \
       --crf_compressor /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/lex/compressor/dev.out \
       --linearization \
       --one_step /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/preorder/clf_one_step.cPickle \
       --two_step /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/preorder/clf_two_step.cPickle

python prepare_parallel.py \
       /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/data/alignments/split/test \
       /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/+Delex+Compress+Preorder/test.de \
       /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/+Delex+Compress+Preorder/test.en \
       /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/+Delex+Compress+Preorder/model/aligned.grow-diag-final \
       --delex \
       --lex /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/+Delex+Compress+Preorder/test.lex \
       --references /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/+Delex+Compress+Preorder/realization/test.cPickle \
       --compression \
       --crf_compressor /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/compressor/test.out \
       --linearization \
       --one_step /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/preorder/clf_one_step.cPickle \
       --two_step /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/preorder/clf_two_step.cPickle
