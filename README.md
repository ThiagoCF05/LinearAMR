# LinearAMR
This project provides the implementation of the models described on the paper *[Linguistic realisation as machine translation:
Comparing different MT models for AMR-to-text generation](https://eventos.citius.usc.es/inlg2017/resources/final/21/21_Paper.pdf)*.

To obtain the results described at the paper, the following scripts need to be executed: *build.sh*, *parallel.sh*, *pbmt.sh*/*nmt.sh*, *realisation.sh* and *evaluation.sh*.

## build.sh
This script aims to train the models for compression and preordering both for lexicalised as delexicalised data. Before run the script, update the following variables:

1. *corpus*: path for the aligned parallel corpus splitted in training, dev and test sets
2. *path_lex*:  path where the lexicalised compressor and preordering model should be saved
3. *path_delex*: path where the delexicalised compressor and preordering model should be saved

## parallel.sh
This script aims to create a parallel corpus among preprocessed AMRs and their respective English texts. Several instances of the corpus are created following the different combinations of AMR preprocessing techniques applied. For more information about these combinations, check Table 1 of the paper, where they are all depicted. Before run the script, update the following variables:

1. *corpus*: path for the aligned parallel corpus splitted in training, dev and test sets
2. *path_lex*:  path where the lexicalised compressor and preordering model should be saved
3. *path_delex*: path where the delexicalised compressor and preordering model should be saved

## pbmt.sh
Run this script to train, tune and translate using the Phrase-Based Machine Translation paper described. Before run the script, update the following variables:

1. *mosesdecoder*: path for moses
2. *mgiza*:  path for mgiza
3. *lm*: path for a 5-gram language model trained with KenLM
4. *data*: path where parallel corpora resulted from *parallel.sh* are

Look that [Moses](http://www.statmt.org/moses/), [MGiza](https://github.com/moses-smt/mgiza) and a [5-gram KenLM language model](https://github.com/kpu/kenlm) are required to execute this step.

## realisation.sh
