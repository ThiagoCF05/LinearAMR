__author__ = 'thiagocastroferreira'

"""
Author: Thiago Castro Ferreira
Date: 19/04/2017
Description:
    This script aims to prepare data to be trained by an LSTM to perform a compression of an AMR.
"""

import cPickle as p
import os
import sys
sys.path.append('../')

import utils

from ERG import AMR

READ_TRAIN_FILE = '../data/LDC2016E25/data/alignments/split/training'
READ_DEV_FILE = '../data/LDC2016E25/data/alignments/split/dev'
READ_TEST_FILE = '../data/LDC2016E25/data/alignments/split/test'

WRITE_TRAIN_X_FILE, WRITE_TRAIN_Y_FILE = 'data_lex/train_X.feat', 'data_lex/train_y.feat'
WRITE_DEV_X_FILE, WRITE_DEV_Y_FILE = 'data_lex/dev_X.feat', 'data_lex/dev_y.feat'
WRITE_TEST_X_FILE, WRITE_TEST_Y_FILE = 'data_lex/test_X.feat', 'data_lex/test_y.feat'

WVOC = 'data_lex/voc.cPickle'

class LSTMPrepare(object):
    def run(self, ftrain, fdev, ftest, wtrain_X, wtrain_y, wdev_X, wdev_y, wtest_X, wtest_y, wvoc, delexicalized):
        self.train_amrs, self.dev_amrs, self.test_amrs = [], [], []
        self.delexicalized = delexicalized

        self.wvoc = wvoc

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

        print 'PROCESSING VOCABULARY...'
        self.id2word, self.word2id = self.get_vocabulary()

        print 'PROCESSING...'
        self.train_X, self.train_y = self.process(self.train_amrs)
        self.dev_X, self.dev_y = self.process(self.dev_amrs)
        self.test_X, self.test_y = self.process(self.test_amrs)

        print 'WRITING...'
        self.save_voc()
        self.save(self.train_X, self.train_y, wtrain_X, wtrain_y)
        self.save(self.dev_X, self.dev_y, wdev_X, wdev_y)
        self.save(self.test_X, self.test_y, wtest_X, wtest_y)

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

    def get_vocabulary(self):
        voc = []
        for amr in self.train_amrs:
            for node in amr.nodes:
                voc.append(amr.nodes[node].name)

                for edge in amr.edges[node]:
                    voc.append(edge.name)

        voc.append('node_unk')
        voc.append('edge_unk')
        voc.append('pad')
        voc = list(set(voc))
        print 'VOCABULARY SIZE:', len(voc)
        id2word = dict([(i, w) for i, w in enumerate(voc)])
        word2id = dict([(w, i) for i, w in id2word.iteritems()])
        return id2word, word2id

    def extract(self, root, amr, X, y):
        node_name = amr.nodes[root].name
        status = amr.nodes[root].status

        try:
            index = self.word2id[node_name]
        except:
            index = self.word2id['node_unk']
        X.append(index)

        if status == '+':
            y.append(1)
        else:
            y.append(0)

        for edge in amr.edges[root]:
            edge_name = edge.name
            status = edge.status

            try:
                index = self.word2id[edge_name]
            except:
                index = self.word2id['edge_unk']
            X.append(index)

            if status == '+':
                y.append(1)
            else:
                y.append(0)

            X, y = self.extract(edge.node_id, amr, X, y)
        return X, y

    def process(self, amrs):
        X, y = [], []
        for amr in amrs:
            if len(amr.nodes) == 0:
                X.append([])
                y.append([])
            else:
                _X, _y = self.extract(amr.root, amr, [], [])
                X.append(_X)
                y.append(_y)

        return X, y

    def save_voc(self):
        p.dump(self.id2word, open(self.wvoc, 'w'))

    def save(self, X, y, Xname, yname):
        Xf = open(Xname, 'w')
        yf = open(yname, 'w')

        for i, amr in enumerate(X):
            if len(amr) == 0:
                Xf.write('0')
                yf.write('0')
            else:
                Xf.write(' '.join(map(lambda x: str(x), amr)))
                yf.write(' '.join(map(lambda x: str(x), y[i])))
            Xf.write('\n')
            yf.write('\n')
        Xf.close()
        yf.close()

if __name__ == '__main__':
    prep = LSTMPrepare()
    prep.run(READ_TRAIN_FILE, READ_DEV_FILE, READ_TEST_FILE,
             WRITE_TRAIN_X_FILE, WRITE_TRAIN_Y_FILE,
             WRITE_DEV_X_FILE, WRITE_DEV_Y_FILE,
             WRITE_TEST_X_FILE, WRITE_TEST_Y_FILE, WVOC, delexicalized=False)