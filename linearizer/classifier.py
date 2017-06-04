
import argparse
import cPickle as p
import operator
import os
import utils

from ERG import AMR

import nltk
from nltk.classify import MaxentClassifier, accuracy
nltk.config_megam("/usr/local/bin/megam.opt")
from scipy.stats import rankdata

class ClassifierTraining(object):
    def __init__(self, ftrain, fdev, ftest, delexicalized=True):
        self.train_amrs, self.dev_amrs, self.test_amrs = [], [], []
        self.delexicalized = delexicalized

        print 'PARSING...'
        for f in os.listdir(ftrain):
            self.train_amrs.extend(self.parse(os.path.join(ftrain, f)))

        for f in os.listdir(fdev):
            self.dev_amrs.extend(self.parse(os.path.join(fdev, f)))

        for f in os.listdir(ftest):
            self.test_amrs.extend(self.parse(os.path.join(ftest, f)))

        print 'EXTRACTING...'
        self.train_one_step, self.train_two_step = self.extract_features(self.train_amrs)
        self.dev_one_step, self.dev_two_step = self.extract_features(self.dev_amrs)
        # test_one_step, test_two_step = self.extract_features(self.test_amrs)

        print 'SAVING...'
        p.dump(self.train_one_step, open('steps_delex/train_one_step.cPickle', 'w'))
        p.dump(self.train_two_step, open('steps_delex/train_two_step.cPickle', 'w'))
        p.dump(self.dev_one_step, open('steps_delex/dev_one_step.cPickle', 'w'))
        p.dump(self.dev_two_step, open('steps_delex/dev_two_step.cPickle', 'w'))

        print 'TRAINING...'
        self.train()

        p.dump(self.clf_one_step, open('steps_delex/clf_one_step.cPickle', 'w'))
        p.dump(self.clfs_two_step, open('steps_delex/clf_two_step.cPickle', 'w'))

        print 'EVALUATING...'
        self.evaluate()

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
                if self.delexicalized:
                    amr.delexicalize(amr.root, [])
                amr.order(amr.root, 1)

                amrs.append(amr)
            except:
                print 'Parsing error'

        return amrs

    def process(self, amr, root, tokens):
        head = amr.nodes[root].name
        head_tokens = amr.nodes[root].tokens
        tokens.extend(head_tokens)

        before, after = [], []

        for edge in amr.edges[root]:
            child_tokens = self.process(amr, edge.node_id, [])
            child = amr.nodes[edge.node_id].name
            order_id = amr.nodes[edge.node_id].order_id
            child_tokens.extend(edge.tokens)

            tokens.extend(child_tokens)

            feature = {'head':head, 'edge':edge.name, 'child':child, 'order_id':order_id}
            if len(child_tokens) > 0:
                feature['token'] = min(child_tokens)

                if len(head_tokens) > 0:
                    if min(child_tokens) < min(head_tokens):
                        before.append(feature)
                    else:
                        after.append(feature)
                else:
                    before.append(feature)

        # treat group before the head
        before.sort(key=operator.itemgetter('order_id'))
        features_two_step = {'head':head}
        for i, elem in enumerate(before):
            simple_feature = {'head':elem['head'], 'edge':elem['edge'], 'child':elem['child']}
            self.one_step.append((simple_feature, 'before'))

            key = 'edge_' + str(i+1)
            features_two_step[key] = elem['edge']
            key = 'child_' + str(i+1)
            features_two_step[key] = elem['child']

        if 1 < len(before) < 5:
            before.sort(key=operator.itemgetter('token', 'order_id'))
            label = map(lambda x: x['order_id'], before)
            label = map(lambda x: str(int(x)), rankdata(label, method='ordinal'))
            label = '-'.join(label)

            features_two_step['position'] = 'before'

            if len(before) not in self.two_step:
                self.two_step[len(before)] = []
            self.two_step[len(before)].append((features_two_step, label))

        # treat group after the head
        after.sort(key=operator.itemgetter('order_id'))
        features_two_step = {'head':head}
        for i, elem in enumerate(after):
            simple_feature = {'head':elem['head'], 'edge':elem['edge'], 'child':elem['child']}
            self.one_step.append((simple_feature, 'after'))

            key = 'edge_' + str(i+1)
            features_two_step[key] = elem['edge']
            key = 'child_' + str(i+1)
            features_two_step[key] = elem['child']

        if 1 < len(after) < 5:
            after.sort(key=operator.itemgetter('token', 'order_id'))
            label = map(lambda x: x['order_id'], after)
            label = map(lambda x: str(int(x)), rankdata(label, method='ordinal'))
            label = '-'.join(label)

            features_two_step['position'] = 'after'

            if len(after) not in self.two_step:
                self.two_step[len(after)] = []
            self.two_step[len(after)].append((features_two_step, label))
        return tokens

    def extract_features(self, amrs):
        self.one_step = []
        self.two_step = {}

        for amr in amrs:
            self.process(amr, amr.root, [])
        return self.one_step, self.two_step

    def train(self):
        self.clf_one_step = MaxentClassifier.train(self.train_one_step, 'megam', trace=0, max_iter=1000)

        self.clfs_two_step = {
            2: MaxentClassifier.train(self.train_two_step[2], 'megam', trace=0, max_iter=1000),
            3: MaxentClassifier.train(self.train_two_step[3], 'megam', trace=0, max_iter=1000),
            4: MaxentClassifier.train(self.train_two_step[4], 'megam', trace=0, max_iter=1000),
        }

    def evaluate(self):
        print 'One-step: ', accuracy(self.clf_one_step, self.dev_one_step)

        print 'Two-step: '
        print '2', accuracy(self.clfs_two_step[2], self.dev_two_step[2])
        print '3', accuracy(self.clfs_two_step[3], self.dev_two_step[3])
        print '4', accuracy(self.clfs_two_step[4], self.dev_two_step[4])

class Classifier(object):
    def __init__(self, clf_one_step, clfs_two_step):
        self.clf_one_step = p.load(open(clf_one_step))
        self.clfs_two_step = p.load(open(clfs_two_step))

    def process(self, amr):
        self.amr = amr

        self.linearize(self.amr.root, 1)
        return self.amr

    def prepare_two_step_features(self, l, label):
        features_two_step = {}

        key = 'head'
        features_two_step[key] = l[0][1]['head']
        for i, elem in enumerate(l):
            key = 'edge_' + str(i+1)
            features_two_step[key] = elem[1]['edge']
            key = 'child_' + str(i+1)
            features_two_step[key] = elem[1]['child']

        features_two_step['position'] = label
        return features_two_step

    def linearize(self, root, order_id):
        before, after = [], []
        head = self.amr.nodes[root].name

        for edge in self.amr.edges[root]:
            child = self.amr.nodes[edge.node_id].name
            feature = {'head':head, 'edge':edge.name, 'child':child}

            if self.amr.nodes[root].status == '+':
                label = self.clf_one_step.classify(feature)
                if label == 'before':
                    before.append((edge, feature))
                else:
                    after.append((edge, feature))
            else:
                before.append((edge, feature))

        # treat nodes before
        if 1 < len(before) < 5:
            feature = self.prepare_two_step_features(before, 'before')

            label = self.clfs_two_step[len(before)].classify(feature)
            label = map(lambda x: int(x), label.split('-'))

            for i in label:
                before[i-1][0].order_id = order_id
                order_id += 1
                order_id = self.linearize(before[i-1][0].node_id, order_id)
        else:
            for elem in before:
                elem[0].order_id = order_id
                order_id += 1
                order_id = self.linearize(elem[0].node_id, order_id)

        # treat head
        self.amr.nodes[root].order_id = order_id
        order_id += 1

        # treat nodes after
        if 1 < len(after) < 5:
            feature = self.prepare_two_step_features(after, 'after')

            label = self.clfs_two_step[len(after)].classify(feature)
            label = map(lambda x: int(x), label.split('-'))

            for i in label:
                after[i-1][0].order_id = order_id
                order_id += 1
                order_id = self.linearize(after[i-1][0].node_id, order_id)
        else:
            for elem in after:
                elem[0].order_id = order_id
                order_id += 1
                order_id = self.linearize(elem[0].node_id, order_id)

        return order_id

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('train', type=str, default='../data/LDC2016E25/data/alignments/split/training', help='train file')
    parser.add_argument('dev', type=str, default='../data/LDC2016E25/data/alignments/split/dev', help='dev file')
    parser.add_argument('test', type=str, default='../data/LDC2016E25/data/alignments/split/test', help='test file')
    parser.add_argument("--delex", action="store_true", help="delexicalized")
    args = parser.parse_args()

    train = args.train
    dev = args.dev
    test = args.test
    delex = args.delex

    prep = ClassifierTraining(train, dev, test, delexicalized=delex)