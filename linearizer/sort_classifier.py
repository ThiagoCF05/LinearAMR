
import cPickle as p
import operator
import os
import utils

from ERG import AMR

import nltk
from nltk.classify import MaxentClassifier, accuracy
nltk.config_megam("/usr/local/bin/megam.opt")

class SortClassifierTraining(object):
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
        self.train_one_step, self.train_sort_step = self.extract_features(self.train_amrs)
        self.dev_one_step, self.dev_sort_step = self.extract_features(self.dev_amrs)
        # test_one_step, test_two_step = self.extract_features(self.test_amrs)

        print 'SAVING...'
        p.dump(self.train_one_step, open('sort_lex/train_one_step.cPickle', 'w'))
        p.dump(self.train_sort_step, open('sort_lex/train_sort_step.cPickle', 'w'))
        p.dump(self.dev_one_step, open('sort_lex/dev_one_step.cPickle', 'w'))
        p.dump(self.dev_sort_step, open('sort_lex/dev_sort_step.cPickle', 'w'))

        print 'TRAINING...'
        self.train()

        p.dump(self.clf_one_step, open('sort_lex/clf_one_step.cPickle', 'w'))
        p.dump(self.clf_sort_step, open('sort_lex/clf_sort_step.cPickle', 'w'))

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

    def process(self, amr, root, tokens, height):
        head = amr.nodes[root].name
        head_tokens = amr.nodes[root].tokens
        tokens.extend(head_tokens)

        before, after = [], []
        parsed_edges = []

        for edge in amr.edges[root]:
            child_tokens = self.process(amr, edge.node_id, [], height+1)
            child = amr.nodes[edge.node_id].name
            leaf = len(amr.edges[edge.node_id]) == 0
            child_tokens.extend(edge.tokens)

            parsed_edges.append({'edge': edge, 'tokens':child_tokens})

            tokens.extend(child_tokens)

            feature = {'head':head, 'edge':edge.name, 'child':child, 'leaf':leaf, 'height':height}
            if len(child_tokens) > 0:
                feature['token'] = min(child_tokens)

                if len(head_tokens) > 0:
                    if min(child_tokens) < min(head_tokens):
                        before.append(feature)
                    else:
                        after.append(feature)
                else:
                    before.append(feature)

        edge_before, edge_after = [], []
        for i, edge in enumerate(parsed_edges):
            for j in range(i+1, len(parsed_edges)):
                edge_2 = parsed_edges[j]

                tokens_i = parsed_edges[i]['tokens']
                tokens_j = parsed_edges[j]['tokens']

                if len(tokens_i) > 0 and len(tokens_j) > 0:
                    token_i = min(tokens_i)
                    token_j = min(tokens_j)

                    feature = {
                        'head':head,
                        'edge_1':edge['edge'].name,
                        'child_1':amr.nodes[edge['edge'].node_id].name,
                        'leaf_1':len(amr.edges[edge['edge'].node_id]) == 0,
                        'edge_2':edge_2['edge'].name,
                        'child_2':amr.nodes[edge_2['edge'].node_id].name,
                        'leaf_2':len(amr.edges[edge_2['edge'].node_id]) == 0,
                        'height':height
                    }
                    if token_i < token_j:
                        edge_before.append(feature)
                    elif token_i > token_j:
                        edge_after.append(feature)
                    else:
                        if edge['edge'].order_id < edge_2['edge'].order_id:
                            edge_before.append(feature)
                        else:
                            edge_after.append(feature)

        for feature in before:
            self.one_step.append((feature, 'before'))
        for feature in after:
            self.one_step.append((feature, 'after'))

        for feature in edge_before:
            self.sort_step.append((feature, 'before'))
        for feature in edge_after:
            self.sort_step.append((feature, 'after'))

        return tokens

    def extract_features(self, amrs):
        self.one_step = []
        self.sort_step = []

        for amr in amrs:
            self.process(amr, amr.root, [], 1)
        return self.one_step, self.sort_step

    def train(self):
        self.clf_one_step = MaxentClassifier.train(self.train_one_step, 'megam', trace=0, max_iter=1000)

        self.clf_sort_step = MaxentClassifier.train(self.train_sort_step, 'megam', trace=0, max_iter=1000)

    def evaluate(self):
        print 'One-step: ', accuracy(self.clf_one_step, self.dev_one_step)

        print 'Sort-step: ',  accuracy(self.clf_sort_step, self.dev_sort_step)

class SortClassifier(object):
    def __init__(self, clf_one_step, clf_sort_step):
        self.clf_one_step = p.load(open(clf_one_step))
        self.clf_sort_step = p.load(open(clf_sort_step))

    def process(self, amr):
        self.amr = amr

        self.linearize(self.amr.root, 1)
        return self.amr

    def sort_step(self, group, height):
        if len(group) <= 1:
            return group

        half = len(group) / 2
        group1 = self.sort_step(group[:half])
        group2 = self.sort_step(group[half:])

        result = []
        while len(group1) > 0 or len(group2) > 0:
            if len(group1) == 0:
                result.append(group2[0])
                del group2[0]
            elif len(group2) == 0:
                result.append(group1[0])
                del group1[0]
            else:
                g1, g2 = group1[0], group2[0]

                feature = {
                    'head': g1[1]['head'],
                    'edge_1': g1[1]['edge'],
                    'child_1': g1[1]['child'],
                    'leaf_1':len(self.amr.edges[g1[0]['edge'].node_id]) == 0,
                    'edge_2': g2[1]['edge'],
                    'child_2': g2[1]['child'],
                    'leaf_2':len(self.amr.edges[g2[0]['edge'].node_id]) == 0,
                    'height':height
                }
                label = self.clf_sort_step.classify(feature)
                if label == 'before':
                    result.append(g1)
                    result.append(g2)
                else:
                    result.append(g2)
                    result.append(g1)
                del group1[0]
                del group2[0]
        return result

    def linearize(self, root, order_id, height=1):
        before, after = [], []
        head = self.amr.nodes[root].name

        for edge in self.amr.edges[root]:
            child = self.amr.nodes[edge.node_id].name
            leaf = len(self.amr.edges[edge.node_id]) == 0
            feature = {'head':head, 'edge':edge.name, 'child':child, 'leaf':leaf, 'height':height}

            if self.amr.nodes[root].status == '+':
                label = self.clf_one_step.classify(feature)
                if label == 'before':
                    before.append((edge, feature))
                else:
                    after.append((edge, feature))
            else:
                before.append((edge, feature))

        # treat nodes before
        before = self.sort_step(before, height)
        for elem in before:
            elem[0].order_id = order_id
            order_id += 1
            order_id = self.linearize(elem[0].node_id, order_id, height+1)

        # treat head
        self.amr.nodes[root].order_id = order_id
        order_id += 1

        # treat nodes after
        after = self.sort_step(after, height)
        for elem in after:
            elem[0].order_id = order_id
            order_id += 1
            order_id = self.linearize(elem[0].node_id, order_id, height+1)

        return order_id

if __name__ == '__main__':
    train = '../data/LDC2016E25/data/alignments/split/training'
    dev = '../data/LDC2016E25/data/alignments/split/dev'
    test = '../data/LDC2016E25/data/alignments/split/test'

    prep = SortClassifierTraining(train, dev, test, delexicalized=False)