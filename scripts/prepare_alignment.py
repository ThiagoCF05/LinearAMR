__author__ = 'thiagocastroferreira'

"""
Author: Thiago Castro Ferreira
Date: 22/02/2017
Description:
    This script aims to prepare (prepare) a script to be aligned by Giza, as well as
    formatted to the original format after the alignment (write)
"""

from ERG import AMR

import os
import utils
import cPickle as p

def clean(amr):
    amr = amr.replace('\t', '').replace('\n', '').replace('\r', '')

    _amr, isWiki = [], []
    for token in amr.split():
        if token[0] == ':' and len(token) > 0:
            token = token.lower()

        if token == ':wiki':
            isWiki = True
        else:
            if isWiki:
                if token != '-' and (token[0] != '\"' or token[-1] != '\"'):
                    parenthesis = ''
                    for c in token:
                        if c == ')':
                            parenthesis += ')'
                    _amr.append(parenthesis)
                isWiki = False
            else:
                _amr.append(token)
    return ' '.join(_amr)

def prepare(famr, feng):
    dirs = ['data/LDC2016E25/data/amrs/split/test']

    amrs = []
    for dir in dirs:
        for file in os.listdir(dir):
            if 'prince' in dir:
                amrs.extend(utils.parse_corpus(os.path.join(dir, file), True))
            else:
                amrs.extend(utils.parse_corpus(os.path.join(dir, file), False))

    feng = open(feng, 'w')
    famr = open(famr, 'w')

    for i, amr in enumerate(amrs):
        try:
            snt = ' '.join(amr['sentence'].lower().split())
        except:
            print 'Error'
            snt = ''

        try:
            # _amr = AMR(nodes={}, edges={}, root=1)
            # _amr.parse_aligned(amr['amr'].lower())
            # _amr.remove_senses()
            # _amr.delexicalize(_amr.root, [])
            # _amr = clean(_amr.prettify(print_constants=True))
            _amr = clean(amr['amr'])
        except:
            print 'Error'
            print amr['sentence']
            print '\n'
            _amr = ''

        if snt != '' and _amr != '':
            famr.write(_amr)
            famr.write('\n')

            feng.write(snt)
            feng.write('\n')
    feng.close()
    famr.close()

def write(fnread, fnwrite):
    f = open(fnread)
    doc = f.read()
    doc = doc.split('\n\n')[:-1]
    f.close()

    fwrite = open(fnwrite, 'w')
    fwrite.write('# AMR release; corpus: lpp; section: training; number of AMRs: 1274 \n\n')
    for row in doc:
        try:
            snt, amr = row.split('\n')
            snt = map(lambda w: w.split('_')[0], snt.split())
            snt.insert(1, '::snt')
            snt = ' '.join(snt)

            print amr, '\n'
            graph = AMR(nodes={}, edges={}, root=1)
            graph.parse_aligned(amr)
            amr = graph.prettify(print_constants=True)

            fwrite.write('#')
            fwrite.write('\n')
            fwrite.write(snt)
            fwrite.write('\n')
            # fwrite.write('#')
            # fwrite.write('\n')
            fwrite.write('#')
            fwrite.write('\n')
            fwrite.write(amr)
            fwrite.write('\n')
            fwrite.write('\n')
        except:
            print 'Error'
    fwrite.close()

if __name__ == '__main__':
    fnread = 'data/LDC2016E25/evaluation/model_nima1/alignments/test_aligned.txt'
    fwrite = 'data/LDC2016E25/evaluation/model_nima1/alignments/test.txt'
    # write(fnread=fnread, fnwrite=fwrite)

    famr = 'test.txt'
    feng = 'ENG.txt'
    prepare(famr, feng)