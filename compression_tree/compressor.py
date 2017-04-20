import sys
sys.path.append('../')

import cPickle as p
import numpy as np

from ERG import AMR

class Compressor(object):
    def __init__(self, clf_node_path, clf_edge_path, edge_path, edge_parent_path, edge_child_path, node_path, node_parent_path):
        self.clf_node = p.load(open(clf_node_path))
        self.clf_edge = p.load(open(clf_edge_path))

        edge = p.load(open(edge_path))
        self.edge_pos = edge['pos']
        self.edge_neg = edge['neg']

        edge_parent = p.load(open(edge_parent_path))
        self.edge_parent_pos = edge_parent['pos']
        self.edge_parent_neg = edge_parent['neg']

        edge_child = p.load(open(edge_child_path))
        self.edge_child_pos = edge_child['pos']
        self.edge_child_neg = edge_child['neg']

        node = p.load(open(node_path))
        self.node_pos = node['pos']
        self.node_neg = node['neg']

        node_parent = p.load(open(node_parent_path))
        self.node_parent_pos = node_parent['pos']
        self.node_parent_neg = node_parent['neg']

    def set_node_features(self, node, name, parent):
        features = []
        # Is a coreference?
        if 'coref' in node:
            name = '-'.join(name.split('-')[:-1])
            features.append(1)
        else:
            features.append(0)

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

        return features

    def compress(self, amr):
        for node in amr.nodes:
            parent = amr.nodes[node].parent
            name = amr.nodes[node].name

            features = self.set_node_features(node, name, parent)
            features = np.array(features).reshape(1, -1)

            # classify
            y = self.clf_node.predict(features)[0]
            if y == 1:
                amr.nodes[node].status = '-'
            else:
                amr.nodes[node].status = '+'

            if parent['node'] == 'root':
                parent_name = 'root'
            else:
                parent_name = amr.nodes[parent['node']].name

            for i, edge in enumerate(amr.edges[node]):
                child_name = amr.nodes[edge.node_id].name

                edge_feature = self.set_edge_features(edge, edge.node_id, parent_name, child_name)
                edge_feature = np.array(edge_feature).reshape(1, -1)

                # classify
                y = self.clf_edge.predict(edge_feature)[0]
                if y == 1:
                    amr.edges[node][i].status = '-'
                else:
                    amr.edges[node][i].status = '+'
        return amr