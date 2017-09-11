####################################################################################################
# Author: Thiago Castro Ferreira
# Date: 23/03/2017
# Description:
#    This script aims to realise the references of the delexicalised outputs
####################################################################################################

data=/Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/AMR/Corpora/LDC2015E86/evaluation/lex/+Delex+Compress+Preorder/

references=$data/realization/test.cPickle
text_delex=$data/test.out
text=$data/test.lex_out

python realization.py $references $text_delex $text