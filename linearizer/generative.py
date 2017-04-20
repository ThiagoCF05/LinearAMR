__author__ = 'thiagocastroferreira'

from sys import path
path.append('/home/tcastrof/amr/scp_repo')
path.append('/home/tcastrof/amr/Grammar')
path.append('../')

from compression_tree.compressor import Compressor
from ERG import AMR

import kenlm
import os
import utils
import itertools

class Generative(object):
    def __init__(self, lm_path):
        self.model = kenlm.Model(lm_path)
        self.compressor = compressor

    def process(self, amr):
        self.amr = amr

        return self.linearize(self.amr.root)

    def ranking(self, base):
        candidates = []
        for candidate in itertools.permutations(base):
            snt = []
            for e in candidate:
                for span in e.split():
                    snt.extend(span.split('~'))

            snt = ' '.join(snt)
            score = self.model.score(snt)
            candidates.append((' '.join(candidate), score))

        return sorted(candidates, key=lambda x: x[1], reverse=True)

    def linearize(self, root):
        linear = []

        for edge in self.amr.edges[root]:
            linear_child = self.linearize(edge.node_id)

            if linear_child.strip() != '':
                if edge.status == '+':
                    linear_child = edge.name + '~' + linear_child
                linear.append(linear_child)

        status = self.amr.nodes[root].status
        name = self.amr.nodes[root].name

        if 0 < len(linear) <= 9:
            if status == '+':
                linear.append(name)
            rank = self.ranking(linear)
            return rank[0][0]
        elif len(linear) > 9:
            if status == '+':
                linear.insert(len(linear)-1, name)
            return ' '.join(linear)
        else:
            if status == '+':
                return name
            else:
                return ''

if __name__ == '__main__':
    CLF_NODE_PATH = '../compression/results/clf_node.cPickle'
    CLF_EDGE_PATH = '../compression/results/clf_edge.cPickle'
    EDGE_PATH = '../compression/validation/edge_feat.cPickle'
    EDGE_PARENT_PATH = '../compression/validation/edge_parent_feat.cPickle'
    EDGE_CHILD_PATH = '../compression/validation/edge_child_feat.cPickle'
    NODE_PATH = '../compression/validation/node_feat.cPickle'
    NODE_PARENT_PATH = '../compression/validation/node_parent_feat.cPickle'

    LM_PATH = 'lm/6gram.arpa'

    compressor = Compressor(clf_node_path=CLF_NODE_PATH,
                            clf_edge_path=CLF_EDGE_PATH,
                            edge_path=EDGE_PATH,
                            edge_parent_path=EDGE_PARENT_PATH,
                            edge_child_path=EDGE_CHILD_PATH,
                            node_path=NODE_PATH,
                            node_parent_path=NODE_PARENT_PATH)

    linearizer = Generative(lm_path=LM_PATH)

    amrs_path = '../data/LDC2016E25/data/amrs/split/test'
    amrs = []
    for fname in os.listdir(amrs_path):
        f = os.path.join(amrs_path, fname)
        amrs.extend(utils.parse_corpus(f, False))

    linears = []
    for amr in amrs:
        print amr['sentence']
        linear = linearizer.process(amr['amr'].lower())
        final = []
        for l in linear.split():
            final.extend(l.split('~'))
        linears.append(' '.join(final))

    de = open('../data/LDC2016E25/corpus/test.gen', 'w')
    # en = open('../data/LDC2016E25/corpus/dev.lex', 'w')

    for i, linear in enumerate(linears):
        de.write(linear)
        de.write('\n')

        # en.write(amrs[i]['sentence'].lower())
        # en.write('\n')

    de.close()
    # en.close()