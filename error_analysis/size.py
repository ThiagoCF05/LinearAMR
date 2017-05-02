__author__ = 'thiagocastroferreira'

import pyter
import operator
import os
import numpy as np
import nltk
import utils

from ERG import AMR
from sklearn import linear_model

ANALYSIS_TYPE = 'unseen'
MEASURE = 'ter'

READ_TRAIN_FILE = '../data/LDC2016E25/data/alignments/split/training'
READ_TEST_FILE = '../data/LDC2016E25/data/alignments/split/test'

ORIGINAL_DIR = '../data/final_evaluation/results/pbmt/-Delex+Compress+Preorder/test.en'
mDelex_compress_preorder = '../data/final_evaluation/results/pbmt/-Delex+Compress+Preorder/test.out'

def read(fname):
    with open(fname) as f:
        doc = f.read().split('\n')
        doc = map(lambda x: x.split(), doc)
        return doc

def write(plot, fname):
    f = open(fname, 'w')
    for elem in plot:
        f.write(str(elem[0]))
        f.write(' ')
        f.write(str(elem[1]))
        f.write('\\\\')
    f.close()

def parse(corpus):
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
            amr.order(amr.root, 1)

            amrs.append(amr)
        except:
            print 'Parsing error'
            amr = AMR(nodes={}, edges={}, root=1)
            amrs.append(amr)

    return amrs

def get_depth(root, amr, depth, max_depth):
    if depth > max_depth:
        max_depth = depth

    for edge in amr.edges[root]:
        max_depth = get_depth(edge.node_id, amr, depth+1, max_depth)

    return max_depth

def get_breadth(root, amr, max_breadth):

    breadth = len(amr.edges[root])
    if breadth > max_breadth:
        max_breadth = breadth

    for edge in amr.edges[root]:
        max_breadth = get_breadth(edge.node_id, amr, max_breadth)
    return max_breadth

def get_voc():
    voc = []
    for f in os.listdir(READ_TRAIN_FILE):
        amrs = parse(os.path.join(READ_TRAIN_FILE, f))

        for amr in amrs:
            for node in amr.nodes:
                voc.append(amr.nodes[node].name)

                for edge in amr.edges[node]:
                    voc.append(edge.name)
    return sorted(list(set(voc)))

def count_unseen(amr, voc):
    unseen = 0
    dem = 0
    for node in amr.nodes:
        if amr.nodes[node].name not in voc:
            unseen += 1
        dem += 1

        for edge in amr.edges[node]:
            if edge.name not in voc:
                unseen += 1
            dem += 1

    return unseen

if __name__ == '__main__':
    amrs = []
    for f in os.listdir(READ_TEST_FILE):
        amrs.extend(parse(os.path.join(READ_TEST_FILE, f)))

    refs = read(ORIGINAL_DIR)
    hyps = read(mDelex_compress_preorder)

    if ANALYSIS_TYPE == 'unseen':
        voc = get_voc()
    else:
        voc = []

    result = []
    for i, amr in enumerate(amrs):
        if len(refs[i]) <= 100:
            print i
            try:
                if MEASURE == 'ter':
                    measure = pyter.ter(hyps[i], refs[i])
                else:
                    measure = nltk.translate.bleu([refs[i]], hyps[i])

                if ANALYSIS_TYPE == 'depth':
                    axis = get_depth(amr.root, amr, 0, 0)
                elif ANALYSIS_TYPE == 'breadth':
                    axis = get_breadth(amr.root, amr, 0)
                elif ANALYSIS_TYPE == 'amr_size':
                    axis = len(amr.nodes) + len(amr.edges)
                elif ANALYSIS_TYPE == 'unseen':
                    axis = count_unseen(amr, voc)
                else:
                    axis = len(hyps[i])

                if measure <= 1:
                    result.append((axis, measure))
            except:
                print 'Error'

    result.sort(key=operator.itemgetter(0))

    graph = []
    for ter in result:
        i = len(graph)-1
        if i == -1:
            graph.append((ter[0], [ter[1]]))
        elif graph[i][0] == ter[0]:
            graph[i][1].append(ter[1])
        else:
            graph.append((ter[0], [ter[1]]))

    for i, ter in enumerate(graph):
        graph[i] = (graph[i][0], np.mean(graph[i][1]))

    print graph
    write(graph, 'real.txt')

    # train a regression
    X = map(lambda x: [x[0]], graph)
    y = map(lambda x: x[1], graph)
    reg = linear_model.LinearRegression()
    reg.fit(X, y)

    y_pred = reg.predict(X)

    predictions = []
    for i, pred in enumerate(y_pred):
        predictions.append((X[i][0], pred))

    print 'Predictions'
    print predictions
    write(predictions, 'predictions.txt')