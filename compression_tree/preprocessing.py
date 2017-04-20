import os
import sys
sys.path.append('../')

import cPickle as p
import json
import nltk
import utils

from ERG import AMR

class Prepare(object):
    def run(self, ftrain, fdev, ftest):
        self.train_amrs, self.dev_amrs, self.test_amrs = [], [], []

        for f in os.listdir(ftrain):
            self.train_amrs.extend(self.parse(os.path.join(ftrain, f)))

        for f in os.listdir(fdev):
            self.dev_amrs.extend(self.parse(os.path.join(fdev, f)))

        for f in os.listdir(ftest):
            self.test_amrs.extend(self.parse(os.path.join(ftest, f)))

        self.set_vocabulary()
        self.save_vocabulary()

        self.train_node_X, self.train_node_y, self.train_edge_X, self.train_edge_y = self.preprocess(self.train_amrs)
        self.dev_node_X, self.dev_node_y, self.dev_edge_X, self.dev_edge_y = self.preprocess(self.dev_amrs)
        self.test_node_X, self.test_node_y, self.test_edge_X, self.test_edge_y = self.preprocess(self.test_amrs)

        self.save_features()

    def parse(self, corpus):
        if 'prince' in corpus:
            corpus = utils.parse_corpus(corpus, True)
        else:
            corpus = utils.parse_corpus(corpus, False)

        amrs = []
        for l in corpus:
            try:
                # print l['sentence']
                amr = AMR(nodes={}, edges={}, root=1)
                amr.parse_aligned(l['amr'].lower())
                amr.remove_senses()
                amr.delexicalize(amr.root, [])
                amr.order(amr.root, 1)

                amrs.append(amr)
            except:
                print 'Parsing error'

        return amrs

    def save_vocabulary(self):
        edge = {'pos': self.edge_pos, 'neg': self.edge_neg}
        p.dump(edge, open('training/validation/edge_feat.cPickle', 'w'))

        edge_parent = {'pos': self.edge_parent_pos, 'neg': self.edge_parent_neg}
        p.dump(edge_parent, open('training/validation/edge_parent_feat.cPickle', 'w'))

        edge_child = {'pos': self.edge_child_pos, 'neg': self.edge_child_neg}
        p.dump(edge_child, open('training/validation/edge_child_feat.cPickle', 'w'))

        node = {'pos': self.node_pos, 'neg':self.node_neg}
        p.dump(node, open('training/validation/node_feat.cPickle', 'w'))

        node_parent = {'pos': self.node_parent_pos, 'neg': self.node_parent_neg}
        p.dump(node_parent, open('training/validation/node_parent_feat.cPickle', 'w'))

    def load_vocabulary(self):
        edge = p.load(open('training/validation/edge_feat.cPickle'))
        self.edge_pos = edge['pos']
        self.edge_neg = edge['neg']

        edge_parent = p.load(open('training/validation/edge_parent_feat.cPickle'))
        self.edge_parent_pos = edge_parent['pos']
        self.edge_parent_neg = edge_parent['neg']

        edge_child = p.load(open('training/validation/edge_child_feat.cPickle'))
        self.edge_child_pos = edge_child['pos']
        self.edge_child_neg = edge_child['neg']

        node = p.load(open('training/validation/node_feat.cPickle'))
        self.node_pos = node['pos']
        self.node_neg = node['neg']

        node_parent = p.load(open('training/validation/node_parent_feat.cPickle'))
        self.node_parent_pos = node_parent['pos']
        self.node_parent_neg = node_parent['neg']

    def set_vocabulary(self):
        # initialize
        self.edge_pos = []
        self.edge_neg = []

        self.edge_parent_pos = []
        self.edge_parent_neg = []

        self.edge_child_pos = []
        self.edge_child_neg = []

        # self.edge_parent_child_pos = []
        # self.edge_parent_child_neg = []

        self.node_pos = []
        self.node_neg = []

        self.node_parent_pos = []
        self.node_parent_neg = []

        # extraction
        for amr in self.train_amrs:
            self.extract_features(amr)

        # counting
        self.edge_pos = nltk.FreqDist(self.edge_pos)
        self.edge_neg = nltk.FreqDist(self.edge_neg)

        self.edge_parent_pos = nltk.FreqDist(self.edge_parent_pos)
        self.edge_parent_neg = nltk.FreqDist(self.edge_parent_neg)

        self.edge_child_pos = nltk.FreqDist(self.edge_child_pos)
        self.edge_child_neg = nltk.FreqDist(self.edge_child_neg)

        # self.edge_parent_child_pos = nltk.FreqDist(self.edge_parent_child_pos)
        # self.edge_parent_child_neg = nltk.FreqDist(self.edge_parent_child_neg)

        self.node_pos = nltk.FreqDist(self.node_pos)
        self.node_neg = nltk.FreqDist(self.node_neg)

        self.node_parent_pos = nltk.FreqDist(self.node_parent_pos)
        self.node_parent_neg = nltk.FreqDist(self.node_parent_neg)

    def extract_features(self, amr):
        for node in amr.nodes:
            parent = amr.nodes[node].parent
            name = amr.nodes[node].name

            name_parent = (name, parent['edge'])
            isDeleted = len(amr.nodes[node].tokens) == 0
            if isDeleted:
                self.node_pos.append(name)
                self.node_parent_pos.append(name_parent)
            else:
                self.node_neg.append(name)
                self.node_parent_neg.append(name_parent)

            if parent['node'] == 'root':
                parent_name = 'root'
            else:
                parent_name = amr.nodes[parent['node']].name

            for edge in amr.edges[node]:
                child_name = amr.nodes[edge.node_id].name

                edge_name = edge.name
                edge_parent = (edge.name, parent_name)
                edge_child = (edge.name, child_name)
                # edge_parent_child = (edge.name, parent_name, child_name)

                isDeleted = len(edge.tokens) == 0
                if isDeleted:
                    self.edge_pos.append(edge_name)
                    self.edge_parent_pos.append(edge_parent)
                    self.edge_child_pos.append(edge_child)
                    # self.edge_parent_child_pos.append(edge_parent_child)
                else:
                    self.edge_neg.append(edge_name)
                    self.edge_parent_neg.append(edge_parent)
                    self.edge_child_neg.append(edge_child)
                    # self.edge_parent_child_neg.append(edge_parent_child)

    def set_node_features(self, node, name, parent):
        features = []
        # Is a coreference?
        if 'coref' in node:
            feat = 1
        else:
            feat = 0
        features.append(feat)

        # node frequency
        try:
            feat_pos = self.node_pos[name]
        except:
            feat_pos = 0

        try:
            feat_neg = self.node_neg[name]
        except:
            feat_neg = 0

        if feat_pos == 0 and feat_neg == 0:
            feat = 0
        else:
            feat = float(feat_pos) / (feat_pos+feat_neg)
        features.append(feat)

        # (node, parent) frequency
        name_parent = (name, parent['edge'])
        try:
            feat_pos = self.node_parent_pos[name_parent]
        except:
            feat_pos = 0

        try:
            feat_neg = self.node_parent_neg[name_parent]
        except:
            feat_neg = 0

        if feat_pos == 0 and feat_neg == 0:
            feat = 0
        else:
            feat = float(feat_pos) / (feat_pos+feat_neg)
        features.append(feat)

        return features

    def set_edge_features(self, edge, node, parent_name, child_name):
        features = []
        # is a coreference?
        if 'coref' in node:
            feat = 1
        else:
            feat = 0
        features.append(feat)

        # edge frequency
        try:
            feat_pos = self.edge_pos[edge.name]
        except:
            feat_pos = 0

        try:
            feat_neg = self.edge_neg[edge.name]
        except:
            feat_neg = 0

        if feat_pos == 0 and feat_neg == 0:
            feat = 0
        else:
            feat = float(feat_pos) / (feat_pos+feat_neg)
        features.append(feat)

        # (edge, parent) frequency
        edge_parent = (edge.name, parent_name)
        try:
            feat_pos = self.edge_parent_pos[edge_parent]
        except:
            feat_pos = 0

        try:
            feat_neg = self.edge_parent_neg[edge_parent]
        except:
            feat_neg = 0

        if feat_pos == 0 and feat_neg == 0:
            feat = 0
        else:
            feat = float(feat_pos) / (feat_pos+feat_neg)
        features.append(feat)

        # (edge, child) frequency
        edge_child = (edge.name, child_name)
        try:
            feat_pos = self.edge_child_pos[edge_child]
        except:
            feat_pos = 0

        try:
            feat_neg = self.edge_child_neg[edge_child]
        except:
            feat_neg = 0

        if feat_pos == 0 and feat_neg == 0:
            feat = 0
        else:
            feat = float(feat_pos) / (feat_pos+feat_neg)
        features.append(feat)

        # (edge, parent, child) frequency
        # edge_parent_child = (edge.name, parent_name, child_name)
        # try:
        #     feat_pos = self.edge_parent_child_pos[edge_parent_child]
        # except:
        #     feat_pos = 0
        #
        # try:
        #     feat_neg = self.edge_parent_child_neg[edge_parent_child]
        # except:
        #     feat_neg = 0
        #
        # if feat_pos == 0 and feat_neg == 0:
        #     feat = 0
        # else:
        #     feat = float(feat_pos) / (feat_pos+feat_neg)
        # features.append(feat)

        return features

    def preprocess(self, amrs):
        node_X, node_y, edge_X, edge_y = [], [], [], []

        for amr in amrs:
            for node in amr.nodes:
                parent = amr.nodes[node].parent
                name = amr.nodes[node].name

                features = self.set_node_features(node, name, parent)
                node_X.append(features)

                isDeleted = len(amr.nodes[node].tokens) == 0
                if isDeleted:
                    node_y.append(1)
                else:
                    node_y.append(0)

                if parent['node'] == 'root':
                    parent_name = 'root'
                else:
                    parent_name = amr.nodes[parent['node']].name
                for edge in amr.edges[node]:
                    child_name = amr.nodes[edge.node_id].name

                    edge_feature = self.set_edge_features(edge, edge.node_id, parent_name, child_name)
                    edge_X.append(edge_feature)

                    # set edge class
                    isDeleted = len(edge.tokens) == 0
                    if isDeleted:
                        edge_y.append(1)
                    else:
                        edge_y.append(0)

        return node_X, node_y, edge_X, edge_y

    def save_features(self):
        node_train = {
            'X': self.train_node_X,
            'y': self.train_node_y
        }
        node_dev = {
            'X': self.dev_node_X,
            'y': self.dev_node_y
        }
        node_test = {
            'X': self.test_node_X,
            'y': self.test_node_y
        }

        json.dump(node_train, open('training/validation/node_train.json', 'w'), sort_keys=True, indent=4, separators=(',', ': '))
        json.dump(node_dev, open('training/validation/node_dev.json', 'w'), sort_keys=True, indent=4, separators=(',', ': '))
        json.dump(node_test, open('training/validation/node_test.json', 'w'), sort_keys=True, indent=4, separators=(',', ': '))

        edge_train = {
            'X': self.train_edge_X,
            'y': self.train_edge_y
        }
        edge_dev = {
            'X': self.dev_edge_X,
            'y': self.dev_edge_y
        }
        edge_test = {
            'X': self.test_edge_X,
            'y': self.test_edge_y
        }

        json.dump(edge_train, open('training/validation/edge_train.json', 'w'), sort_keys=True, indent=4, separators=(',', ': '))
        json.dump(edge_dev, open('training/validation/edge_dev.json', 'w'), sort_keys=True, indent=4, separators=(',', ': '))
        json.dump(edge_test, open('training/validation/edge_test.json', 'w'), sort_keys=True, indent=4, separators=(',', ': '))

if __name__ == '__main__':
    train = '../data/LDC2016E25/data/alignments/split/training'
    dev = '../data/LDC2016E25/data/alignments/split/dev'
    test = '../data/LDC2016E25/data/alignments/split/test'

    prep = Prepare()
    prep.run(train, dev, test)