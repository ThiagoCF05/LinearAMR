__author__ = 'thiagocastroferreira'

"""
Author: Thiago Castro Ferreira
Date: 02/05/2017
Description:
    This script aims to break the Gigaword corpus in subfiles with 2 million sentences to boost the parsing performed
    by delex_gigaword.py
"""


if __name__ == '__main__':
    gigaword = '/roaming/tcastrof/gigaword/delex/gigaword.delex'

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
