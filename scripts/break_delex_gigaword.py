__author__ = 'thiagocastroferreira'

"""
Author: Thiago Castro Ferreira
Date: 02/05/2017
Description:
    This script aims to break (and unite) the Gigaword corpus in subfiles with 2 million sentences to boost the parsing performed
    by delex_gigaword.py
"""

import os

def _break(gigaword):
    f = open(gigaword)
    doc = f.read()
    f.close()

    nfiles = 1
    f = open(gigaword+str(nfiles), 'w')
    for i, line in enumerate(doc.split('\n')):
        f.write(line)
        f.write('\n')

        if (i+1) % 2000000 == 0:
            nfiles += 1
            f.close()

            f = open(gigaword+str(nfiles), 'w')
    f.close()

def _unite(split_gigaword, wgigaword):
    f = open(wgigaword, 'w')
    for fname in os.listdir(split_gigaword):
        if 'gigaword.tok.delex' in fname:
            g = open(os.path.join(split_gigaword, fname), 'w')
            doc = g.read()
            g.close()

            f.write(doc)
    f.close()

if __name__ == '__main__':
    # gigaword = '/roaming/tcastrof/gigaword/delex/gigaword.delex'
    # _break(gigaword)

    split_gigaword = '/roaming/tcastrof/gigaword/delex'
    wgigaword = '/roaming/tcastrof/gigaword/gigaword.tok.delex'
    _unite(split_gigaword, wgigaword)