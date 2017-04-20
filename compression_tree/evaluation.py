import cPickle as p
import json

from sklearn import tree
from sklearn.metrics import f1_score, accuracy_score

class Evaluation(object):
    def __init__(self, train_node, train_edge, dev_node, dev_edge, test_node, test_edge):
        train_node = json.load(open(train_node))
        self.train_node_X = train_node['X']
        self.train_node_y = train_node['y']

        dev_node = json.load(open(dev_node))
        self.dev_node_X = dev_node['X']
        self.dev_node_y = dev_node['y']

        test_node = json.load(open(test_node))
        self.test_node_X = test_node['X']
        self.test_node_y = test_node['y']
        #############################################
        train_edge = json.load(open(train_edge))
        self.train_edge_X = train_edge['X']
        self.train_edge_y = train_edge['y']

        dev_edge = json.load(open(dev_edge))
        self.dev_edge_X = dev_edge['X']
        self.dev_edge_y = dev_edge['y']

        test_edge = json.load(open(test_edge))
        self.test_edge_X = test_edge['X']
        self.test_edge_y = test_edge['y']

        print 'Initializing classifiers...'
        self.init_classifiers()
        print 'Training...'
        self.train()
        print 'Predicting...'
        self.predict()
        print 'Evaluating...'
        self.evaluate()
        print 'Saving...'
        self.save()

    def init_classifiers(self):
        self.clf_node = tree.DecisionTreeClassifier()
        self.clf_edge = tree.DecisionTreeClassifier()

    def train(self):
        self.clf_node.fit(self.train_node_X, self.train_node_y)
        self.clf_edge.fit(self.train_edge_X, self.train_edge_y)

    def predict(self):
        # classifier - node/edge - set - y (class)
        self.clf_node_dev_y = self.clf_node.predict(self.dev_node_X)
        self.clf_node_test_y = self.clf_node.predict(self.test_node_X)

        self.clf_edge_dev_y = self.clf_edge.predict(self.dev_edge_X)
        self.clf_edge_test_y = self.clf_edge.predict(self.test_edge_X)

    def evaluate(self):
        # Classifier - node/edge - set - measure
        self.node_dev_f1 = f1_score(self.dev_node_y, self.clf_node_dev_y)
        self.node_test_f1 = f1_score(self.test_node_y, self.clf_node_test_y)

        self.node_dev_accuracy = accuracy_score(self.dev_node_y, self.clf_node_dev_y)
        self.node_test_accuracy = accuracy_score(self.test_node_y, self.clf_node_test_y)

        self.edge_dev_f1 = f1_score(self.dev_edge_y, self.clf_edge_dev_y)
        self.edge_test_f1 = f1_score(self.test_edge_y, self.clf_edge_test_y)

        self.edge_dev_accuracy = accuracy_score(self.dev_edge_y, self.clf_edge_dev_y)
        self.edge_test_accuracy = accuracy_score(self.test_edge_y, self.clf_edge_test_y)

    def save(self):
        results = {
            'pattern': 'classifier - node/edge - set',
            'y':{
                'node_dev':self.clf_node_dev_y,
                'node_test':self.clf_node_test_y,
                'edge_dev':self.clf_edge_dev_y,
                'edge_test':self.clf_edge_test_y
            },
            'f1':{
                'node_dev':self.node_dev_f1,
                'node_test':self.node_test_f1,
                'edge_dev':self.edge_dev_f1,
                'edge_test':self.edge_test_f1
            },
            'accuracy':{
                'node_dev':self.node_dev_accuracy,
                'node_test':self.node_test_accuracy,
                'edge_dev':self.edge_dev_accuracy,
                'edge_test':self.edge_test_accuracy
            }
        }
        p.dump(results, open('training/results/eval.cPickle', 'w'))

        p.dump(self.clf_node, open('training/results/clf_node.cPickle', 'w'))
        p.dump(self.clf_edge, open('training/results/clf_edge.cPickle', 'w'))

if __name__ == '__main__':
    TRAIN_NODE_PATH = 'training/validation/node_train.json'
    DEV_NODE_PATH = 'training/validation/node_dev.json'
    TEST_NODE_PATH = 'training/validation/node_test.json'

    TRAIN_EDGE_PATH = 'training/validation/edge_train.json'
    DEV_EDGE_PATH = 'training/validation/edge_dev.json'
    TEST_EDGE_PATH = 'training/validation/edge_test.json'

    Evaluation(train_node=TRAIN_NODE_PATH,
               train_edge=TRAIN_EDGE_PATH,
               dev_node=DEV_NODE_PATH,
               dev_edge=DEV_EDGE_PATH,
               test_node=TEST_NODE_PATH,
               test_edge=TEST_EDGE_PATH)