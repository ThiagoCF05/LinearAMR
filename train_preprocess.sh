# cd compression_crf
# python preprocessing.py \
#         /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/data/alignments/split/training \
#         /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/data/alignments/split/dev \
#         /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/data/alignments/split/test \
#         /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/lex/compressor/train.feat \
#         /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/lex/compressor/dev.feat \
#         /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/lex/compressor/test.feat


# python chunking.py < /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/lex/compressor/train.feat > /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/lex/compressor/train.crfsuite.txt
# python chunking.py < /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/lex/compressor/dev.feat > /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/lex/compressor/dev.crfsuite.txt
# python chunking.py < /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/lex/compressor/test.feat > /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/lex/compressor/test.crfsuite.txt

# crfsuite learn -m /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/lex/compressor/compressor.model -e2 /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/lex/compressor/train.crfsuite.txt /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/lex/compressor/dev.crfsuite.txt

# crfsuite tag -m /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/lex/compressor/compressor.model /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/lex/compressor/train.crfsuite.txt > /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/lex/compressor/train.out
# crfsuite tag -m /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/lex/compressor/compressor.model /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/lex/compressor/dev.crfsuite.txt > /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/lex/compressor/dev.out
# crfsuite tag -m /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/lex/compressor/compressor.model /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/lex/compressor/test.crfsuite.txt > /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/lex/compressor/test.out

# cd ../linearizer
# python classifier.py \
# 		/Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/data/alignments/split/training \
# 		/Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/data/alignments/split/dev \
# 		/Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/data/alignments/split/test \
# 		/Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/lex/preorder

# DELEX
cd ../compression_crf
cd compression_crf
python preprocessing.py \
        /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/data/alignments/split/training \
        /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/data/alignments/split/dev \
        /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/data/alignments/split/test \
        /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/compressor/train.feat \
        /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/compressor/dev.feat \
        /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/compressor/test.feat \
        --delex

python chunking.py < /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/compressor/train.feat > /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/compressor/train.crfsuite.txt
python chunking.py < /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/compressor/dev.feat > /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/compressor/dev.crfsuite.txt
python chunking.py < /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/compressor/test.feat > /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/compressor/test.crfsuite.txt

crfsuite learn -m /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/compressor/compressor.model -e2 /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/compressor/train.crfsuite.txt /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/compressor/dev.crfsuite.txt

crfsuite tag -m /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/compressor/compressor.model /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/compressor/train.crfsuite.txt > /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/compressor/train.out
crfsuite tag -m /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/compressor/compressor.model /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/compressor/dev.crfsuite.txt > /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/compressor/dev.out
crfsuite tag -m /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/compressor/compressor.model /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/compressor/test.crfsuite.txt > /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/compressor/test.out

cd ../linearizer
python classifier.py \
                /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/data/alignments/split/training \
                /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/data/alignments/split/dev \
                /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/data/alignments/split/test \
                /Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/delex/preorder \
                --delex