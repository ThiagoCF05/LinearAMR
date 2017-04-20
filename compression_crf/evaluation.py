import json
import os
import utils

from ERG import AMR
from sklearn.metrics import f1_score, accuracy_score

class CRFEvaluation(object):
    def __init__(self, famrs, fresults):
        self.amrs = []
        for f in os.listdir(famrs):
            self.amrs.extend(self.parse_amrs(os.path.join(famrs, f)))

        self.results = self.parse_results(fresults)

        self.node_real, self.node_pred = [], []
        self.edge_real, self.edge_pred = [], []

        self.process()
        self.evaluate()

    def parse_amrs(self, corpus):
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

    def parse_results(self, path):
        f = open(path)
        doc = f.read()
        f.close()

        results = []
        amrs = doc.split('\n\n')
        for amr in amrs:
            _amr = amr.split('\n')
            results.append(_amr)

        return results

    def process(self):
        for i, amr in enumerate(self.amrs):
            self.extract(amr.root, amr, self.results[i], 0)

    def extract(self, root, amr, result, order_id):
        status = amr.nodes[root].status
        if status == '+':
            self.node_real.append(1)
        else:
            self.node_real.append(0)

        if result[order_id] == '+':
            self.node_pred.append(1)
        else:
            self.node_pred.append(0)
        order_id = order_id + 1

        for edge in amr.edges[root]:
            status = edge.status
            if status == '+':
                self.edge_real.append(1)
            else:
                self.edge_real.append(0)

            if result[order_id] == '+':
                self.edge_pred.append(1)
            else:
                self.edge_pred.append(0)
            order_id = order_id + 1
            order_id = self.extract(edge.node_id, amr, result, order_id)
        return order_id

    def evaluate(self):
        # Classifier - node/edge - set - measure
        print set(self.node_real), len(self.node_real)
        print set(self.node_pred), len(self.node_pred)
        self.node_f1 = f1_score(self.node_real, self.node_pred)
        self.node_accuracy = accuracy_score(self.node_real, self.node_pred)

        print set(self.edge_real), len(self.edge_real)
        print set(self.edge_pred), len(self.edge_pred)
        self.edge_f1 = f1_score(self.edge_real, self.edge_pred)
        self.edge_accuracy = accuracy_score(self.edge_real, self.edge_pred)

    def save(self, fwrite):
        results = {
            'f1':{
                'node':self.node_f1,
                'edge':self.edge_f1,
            },
            'accuracy':{
                'node':self.node_accuracy,
                'edge':self.edge_accuracy,
            }
        }
        json.dump(results, open(fwrite, 'w'), indent=4, separators=(',', ': '))

if __name__ == '__main__':
    print 'DEVELOPMENT SET'
    READ_AMRS = '../data/LDC2016E25/data/alignments/split/dev'
    READ_RESULTS = 'data/dev.out'
    WRITE_EVAL = 'data/results/dev.eval'
    evaluation = CRFEvaluation(famrs=READ_AMRS, fresults=READ_RESULTS)
    evaluation.save(WRITE_EVAL)

    print 'TEST SET'
    READ_AMRS = '../data/LDC2016E25/data/alignments/split/test'
    READ_RESULTS = 'data/test.out'
    WRITE_EVAL = 'data/results/test.eval'
    evaluation = CRFEvaluation(famrs=READ_AMRS, fresults=READ_RESULTS)
    evaluation.save(WRITE_EVAL)

