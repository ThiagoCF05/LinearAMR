__author__ = 'thiagocastroferreira'

"""
Author: Thiago Castro Ferreira
Date: 23/03/2017
Description:
    This script aims to prepare data to be trained by CRFSuite to perform a compression of an AMR.
"""

import os
import sys
sys.path.append('../')

import utils

from ERG import AMR

READ_TRAIN_FILE = '../data/LDC2016E25/data/alignments/split/training'
READ_DEV_FILE = '../data/LDC2016E25/data/alignments/split/dev'
READ_TEST_FILE = '../data/LDC2016E25/data/alignments/split/test'

WRITE_TRAIN_FILE = 'data_lex/train.feat'
WRITE_DEV_FILE = 'data_lex/dev.feat'
WRITE_TEST_FILE = 'data_lex/test.feat'

class CRFPrepare(object):
    def run(self, ftrain, fdev, ftest, wtrain, wdev, wtest, delexicalized):
        self.train_amrs, self.dev_amrs, self.test_amrs = [], [], []
        self.delexicalized = delexicalized

        print 'READING...'
        print 'TRAINING...'
        for f in os.listdir(ftrain):
            self.train_amrs.extend(self.parse(os.path.join(ftrain, f)))

        print 'DEV...'
        for f in os.listdir(fdev):
            self.dev_amrs.extend(self.parse(os.path.join(fdev, f)))

        print 'TEST...'
        for f in os.listdir(ftest):
            self.test_amrs.extend(self.parse(os.path.join(ftest, f)))

        print 'PROCESSING...'
        self.train_set = self.process(self.train_amrs)
        self.dev_set = self.process(self.dev_amrs)
        self.test_set = self.process(self.test_amrs)

        print 'WRITING...'
        self.save(self.train_set, wtrain)
        self.save(self.dev_set, wdev)
        self.save(self.test_set, wtest)

    def parse(self, corpus):
        if 'prince' in corpus:
            corpus = utils.parse_corpus(corpus, True)
        else:
            corpus = utils.parse_corpus(corpus, False)

        amrs = []
        for l in corpus:
            try:
                amr = AMR(nodes={}, edges={}, root=1)
                amr.parse_aligned(l['amr'].lower())
                amr.remove_senses()
                if self.delexicalized:
                    amr.delexicalize(amr.root, [])
                amr.order(amr.root, 1)

                amrs.append(amr)
            except:
                print 'Parsing error'
                amr = AMR(nodes={}, edges={}, root=1)
                amrs.append(amr)

        return amrs

    def extract(self, root, amr, features):
        parent_edge = amr.nodes[root].parent['edge']
        node_name = amr.nodes[root].name
        status = amr.nodes[root].status

        features.append((node_name, parent_edge, status))

        for edge in amr.edges[root]:
            edge_name = edge.name
            # child_node = amr.nodes[edge.node_id].name
            status = edge.status

            features.append((edge_name, node_name, status))

            features = self.extract(edge.node_id, amr, features)
        return features

    def process(self, amrs):
        factorized_amrs = []
        for amr in amrs:
            if len(amr.nodes) == 0:
                factorized_amrs.append([])
            else:
                factorized_amrs.append(self.extract(amr.root, amr, []))

        return factorized_amrs

    def save(self, factorized, fname):
        f = open(fname, 'w')
        for amr in factorized:
            if len(amr) == 0:
                f.write('- :root +')
                f.write('\n')
            else:
                for feature in amr:
                    f.write(' '.join(feature))
                    f.write('\n')
            f.write('\n')
        f.close()

if __name__ == '__main__':
    prep = CRFPrepare()
    prep.run(READ_TRAIN_FILE, READ_DEV_FILE, READ_TEST_FILE,
             WRITE_TRAIN_FILE, WRITE_DEV_FILE, WRITE_TEST_FILE, delexicalized=False)