__author__ = 'thiagocastroferreira'

import pyter
import operator
import numpy as np

from sklearn import linear_model

ORIGINAL_DIR = '../data/final_evaluation/results/pbmt/-Delex+Compress+Preorder/test.en'
mDelex_compress_preorder = '../data/final_evaluation/results/pbmt/-Delex+Compress+Preorder/test.out'

def read(fname):
    with open(fname) as f:
        doc = f.read().split('\n')
        doc = map(lambda x: x.split(), doc)
        return doc

if __name__ == '__main__':
    hyps = read(ORIGINAL_DIR)
    refs = read(mDelex_compress_preorder)

    result = []
    for i, e in enumerate(hyps):
        if len(hyps[i]) <= 100:
            print i
            try:
                ter = pyter.ter(hyps[i], refs[i])
                if ter <1:
                    result.append((len(hyps[i]), ter))
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