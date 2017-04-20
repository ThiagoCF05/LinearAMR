from sys import path
path.append('../')

from ERG import AMR

import itertools
import json
import nltk
import utils
import operator
import os

class MajorityTraining(object):
    def __init__(self, train_path, delexicalized):
        self.train_path = train_path
        self.delexicalized = delexicalized

        self.load()
        self.extract()
        self.save()

    def load(self):
        self.amrs = []
        for fname in os.listdir(self.train_path):
            if 'prince' in self.train_path:
                amrs = utils.parse_corpus(os.path.join(self.train_path, fname), True)
            else:
                amrs = utils.parse_corpus(os.path.join(self.train_path, fname), False)
            self.amrs.extend(amrs)

    def process(self, amr, root, all_tokens):
        name, tokens = amr.nodes[root].name, amr.nodes[root].tokens
        all_tokens.extend(tokens)

        linear, linear_delex = [], []
        if len(tokens) > 0:
            linear = [(name, min(tokens), amr.nodes[root].order_id)]
            linear_delex = [('root', min(tokens), amr.nodes[root].order_id)]

        for edge in amr.edges[root]:
            tokens = self.process(amr, edge.node_id, [])
            all_tokens.extend(tokens)

            if len(tokens) > 0:
                linear.append((edge.name, min(tokens), edge.order_id))
                linear_delex.append((edge.name, min(tokens), edge.order_id))

        if len(linear) > 1:
            linear = sorted(linear, key=operator.itemgetter(1, 2))
            linear = ' '.join(map(lambda l: l[0], linear))
            self.train.append(linear)

            linear_delex = sorted(linear_delex, key=operator.itemgetter(1, 2))
            linear_delex = ' '.join(map(lambda l: l[0], linear_delex))
            self.train_delex.append(linear_delex)

        return all_tokens

    def extract(self):
        self.train, self.train_delex = [], []
        for elem in self.amrs:
            try:
                amr = AMR(nodes={}, edges={}, root='')
                amr.parse_aligned(elem['amr'].lower())
                amr.remove_senses()
                amr.delexicalize(amr.root, [])
                amr.order(amr.root, 1)

                self.process(amr, amr.root, [])
            except:
                print 'parsing error'
        self.train = nltk.FreqDist(self.train)
        self.train_delex = nltk.FreqDist(self.train_delex)

    def save(self):
        json.dump(self.train, open('lm/majority.json', 'w'), sort_keys=True, indent=4, separators=(',', ': '))
        json.dump(self.train_delex, open('lm/majority_delex.json', 'w'), sort_keys=True, indent=4, separators=(',', ': '))

class Majority(object):
    def __init__(self, model_path, delex_model_path):
        self.model = json.load(open(model_path))
        self.delex_model = json.load(open(delex_model_path))

    def process(self, amr):
        if type(amr) == str:
            _amr = AMR(nodes={}, edges={}, root='')
            _amr.parse_aligned(amr)
            _amr.delexicalize(_amr.root, {})
            amr = _amr
        self.amr = amr

        return self.linearize(self.amr.root)

    def ranking(self, base, isDelex):
        candidates = []
        for candidate in itertools.permutations(base):
            snt = []
            for e in candidate:
                if e[0] == 'node' and isDelex:
                    snt.append('root')
                else:
                    snt.append(e[1].name)

            snt = ' '.join(snt)

            if isDelex:
                model = self.delex_model
            else:
                model = self.model

            try:
                score = model[snt]
            except:
                score = 0
            candidates.append((candidate, score))

        return sorted(candidates, key=lambda x: x[1], reverse=True)

    def set_amr(self, amr):
        self.amr = amr

    def linearize(self, root, order_id):
        base = [('node', self.amr.nodes[root])]

        for edge in self.amr.edges[root]:
            base.append(('edge', edge))

        # DFS if length bigger than 10
        if len(base) > 10:
            base.sort(key=lambda x: x[1].order_id)
        else:
            candidates = self.ranking(base, False)
            if candidates[0][1] == 0:
                candidates = self.ranking(base, True)
            base = candidates[0][0]

        for e in base:
            e[1].order_id = order_id
            order_id = order_id + 1

            if e[0] == 'edge':
                order_id = self.linearize(e[1].node_id, order_id)

        return order_id

if __name__ == '__main__':
    train = '../data/LDC2016E25/data/alignments/split/training'
    major = MajorityTraining(train_path=train)