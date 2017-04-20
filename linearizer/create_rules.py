import cPickle as p
import os
import operator
import utils

from ERG import AMR
from scipy.stats import rankdata

class RuleCreator(object):
    def __init__(self, ftrain, wtrain, delexicalized=True):
        self.train_amrs = []
        self.wtrain = wtrain
        self.delexicalized = delexicalized

        print 'PARSING...'
        for f in os.listdir(ftrain):
            self.train_amrs.extend(self.parse(os.path.join(ftrain, f)))

        print 'EXTRACTING...'
        self.extract_features(self.train_amrs)

        print 'SAVING...'
        self.save()

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

    def process(self, amr, root, tokens):
        head = amr.nodes[root].name
        head_tokens = amr.nodes[root].tokens
        tokens.extend(head_tokens)

        edges = []

        for edge in amr.edges[root]:
            child_tokens = self.process(amr, edge.node_id, [])
            order_id = amr.nodes[edge.node_id].order_id
            child_tokens.extend(edge.tokens)

            tokens.extend(child_tokens)

            feature = {'edge':edge.name, 'order_id':order_id}
            if len(child_tokens) > 0:
                feature['token'] = min(child_tokens)

                edges.append(feature)

        _input = [head]
        for edge in edges:
            _input.append(edge['edge'])

        if len(_input) > 1:
            _input = ' '.join(_input)
            if len(head_tokens) > 0:
                feature = {'node':head, 'order_id':amr.nodes[root].order_id, 'token':min(head_tokens)}
                edges.append(feature)

                edges.sort(key=operator.itemgetter('token', 'order_id'))
                label = map(lambda x: x['order_id'], edges)
                label = map(lambda x: str(int(x-1)), rankdata(label, method='ordinal'))
                label = ' '.join(label)
            else:
                edges.sort(key=operator.itemgetter('token', 'order_id'))
                label = map(lambda x: x['order_id'], edges)
                label = map(lambda x: str(int(x)), rankdata(label, method='ordinal'))
                label = ' '.join(label)
                label = '-1 ' + label

            if (_input, label) not in self.freq:
                self.freq[(_input, label)] = 0
            self.freq[(_input, label)] += 1
        return tokens

    def extract_features(self, amrs):
        self.freq = {}

        for amr in amrs:
            self.process(amr, amr.root, [])

    def save(self):
        freq = sorted(self.freq.items(), key=operator.itemgetter(1), reverse=True)

        f = open(self.wtrain, 'w')
        for item in freq:
            _input, label = item[0]
            freq = item[1]

            f.write(str(freq))
            f.write('\n')
            f.write(_input)
            f.write('\n')
            f.write(label)
            f.write('\n')
        f.close()

if __name__ == '__main__':
    ftrain = '../data/LDC2016E25/evaluation/model_nima1/alignments/training'
    creator = RuleCreator(ftrain=ftrain, wtrain='rules.txt')