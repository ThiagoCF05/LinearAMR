####################################################################################################
# Author: Thiago Castro Ferreira
# Date: 23/03/2017
# Description:
#    This script aims to train, tunne and run a PBMT model based on a preprocessed parallel data
####################################################################################################

mosesdecoder=/home/tcastrof/workspace/mosesdecoder
mgiza=/home/tcastrof/workspace/mgiza
lm=/roaming/tcastrof/gigaword/gigaword.bin

data=/Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/lex/-Delex+Compress+Preorder/

cd $data
perl $mosesdecoder/scripts/tokenizer/escape-special-chars.perl <train.en >train_esc.en

perl $mosesdecoder/scripts/training/train-model.perl \
    -root-dir . \
    --corpus train_esc \
    -mgiza \
    --max-phrase-length 9 \
    -external-bin-dir $mgiza \
    --f de --e en \
    --first-step 4 \
    --parallel \
    --distortion-limit 6 \
    --lm 0:5:$lm \
    -reordering phrase-msd-bidirectional-fe,hier-mslr-bidirectional-fe

perl $mosesdecoder/scripts/training/mert-moses.pl \
	dev.de \
	dev.en \
    $mosesdecoder/bin/moses \
    model/moses.ini \
    --mertdir $mosesdecoder/mert \
    --rootdir $mosesdecoder/scripts \
    --nbest 1000 \
    --decoder-flags '-threads 25 -v 0' \
    --batch-mira --return-best-dev \
    --batch-mira-args '-J 60'

$mosesdecoder/bin/moses -f mert-work/moses.ini -s 1000 < test.de > test.out