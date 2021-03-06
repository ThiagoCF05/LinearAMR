__author__ = 'thiagocastroferreira'

"""
Author: Thiago Castro Ferreira
Date: 03/2017
Description:
    Main script of the project. It aims to prepare the data for training and decoding of MT models
"""

import argparse
import cPickle as p
import utils
import operator
import os

import numpy as np

from ERG import AMR
from compression_crf.crfcompressor import CRFCompressor
from linearizer.classifier import Classifier

class Parser(object):
    def __init__(self, amr, snt, compressor, linearizer, is_delexicalized, is_compressed, is_linearized):
        self.en = snt.split()
        self.lex = snt.split()
        self.de_en = []
        self.de = ''
        self.matrix = []
        self.real_values = []
        self.is_delexicalized = is_delexicalized
        self.is_compressed = is_compressed
        self.is_linearized = is_linearized

        self.amr = amr

        # DELEXICALIZATION
        self.amr.remove_senses()
        if self.is_delexicalized:
            self.delexicalize(self.amr.root)
            self.remove_delexicalized_repetitions()

        # COMPRESSION
        if is_compressed:
            compressor, index = compressor
            self.amr = compressor.process(self.amr, index)
        else:
            self.amr.include_all()

        # LINEARIZATION
        if self.is_linearized:
            self.amr = linearizer.process(self.amr)
        else:
            self.amr.order(self.amr.root, 0)

        # PREPARE TRANSLATION
        # GET DE-EN ALIGNMENTS
        self.get_de_en()
        self.linearize()

        # GET FR-DE ALIGNMENTS
        self.get_fr_de()

        # MOSES ALIGNMENT FORMAT
        self.format_moses()

        self.en = ' '.join(self.en)
        self.lex = ' '.join(self.lex)

    def get_fr_de(self):
        self.fr = []
        for node in self.amr.nodes:
            name, order_id = self.amr.nodes[node].name, self.amr.nodes[node].order_id
            self.fr.append((name, order_id))

            for edge in self.amr.edges[node]:
                edge_name = edge.name
                edge_order_id = edge.order_id

                self.fr.append((edge_name, edge_order_id))

        self.fr.sort(key=lambda x:x[1])
        xdim, ydim = len(self.fr), len(self.de_en)
        self.fr_de = []

        for i in range(xdim):
            for j in range(ydim):
                if self.fr[i][1] == self.de_en[j][2]:
                    self.fr_de.append((i, j))

        self.fr = map(lambda x: x[0], self.fr)

        self.fr_de = sorted(self.fr_de, key=lambda x:x[1])
        self.fr_de = ' '.join(map(lambda x: str(x[0]) + '-' + str(x[1]), self.fr_de))

    def get_de_en(self):
        self.de_en, self.fr = [], []
        for node in self.amr.nodes:
            status = self.amr.nodes[node].status
            tokens = self.amr.nodes[node].tokens
            if status == '+':
                name = self.amr.nodes[node].name
                node_order_id = self.amr.nodes[node].order_id
                self.de_en.append((name, tokens, node_order_id))

            for edge in self.amr.edges[node]:
                status = edge.status
                tokens = edge.tokens

                if status == '+':
                    edge_name = edge.name
                    edge_order_id = edge.order_id
                    self.de_en.append((edge_name, tokens, edge_order_id))

    def remove_delexicalized_repetitions(self):
        def update_tokens(index):
            for node in self.amr.nodes:
                tokens = self.amr.nodes[node].tokens

                for j, token in enumerate(tokens):
                    if token >= index:
                        self.amr.nodes[node].tokens[j] -= 1

                self.amr.nodes[node].tokens = sorted(list(set(self.amr.nodes[node].tokens)))

                for edge in self.amr.edges[node]:
                    tokens = edge.tokens
                    for j, token in enumerate(tokens):
                        if token >= index:
                            edge.tokens[j] -= 1

                    edge.tokens = sorted(list(set(edge.tokens)))

        new_en, prev_token = [], ''
        for i, word in enumerate(self.en):
            # If the delexicalized token is equal to the previous one, remove it and update the alignments
            if word == prev_token and ((word[:2] == '__' and word[-2:] == '__') or 'wiki~' in word):
                update_tokens(len(new_en))
            else:
                new_en.append(word)
                prev_token = word
        self.en = new_en

    def delexicalize(self, root):
        parent = self.amr.nodes[root].parent
        if parent['node'] == 'root':
            parent_node = ''
        else:
            parent_node = self.amr.nodes[parent['node']].name
        parent_edge = parent['edge']

        name = self.amr.nodes[root].name
        if self.amr.nodes[root].constant and (parent_edge in [':quant', ':value'] or parent_node == 'date-entity'):
            i = 1
            new_name = '__' + parent_edge[1:] + str(i) + '__'
            while new_name in self.en:
                i = i + 1
                new_name = '__' + parent_edge[1:] + str(i) + '__'

            tokens = self.amr.nodes[root].tokens
            text_value = []
            for token in tokens:
                text_value.append((token, self.en[token]))
                self.en[token] = new_name
            self.amr.nodes[root].name = new_name

            text_value.sort(key=lambda x: x[0])
            text_value = ' '.join(map(lambda x: x[1], text_value))
            self.real_values.append({'tag':new_name, 'edge':parent_edge, 'constant':name, 'wiki':'-', 'name': text_value})
        elif name == 'name':
            self.delexicalize_name(root)

        for edge in self.amr.edges[root]:
            self.delexicalize(edge.node_id)

    def delexicalize_name(self, root):
        parent = self.amr.nodes[root].parent
        if parent['node'] == 'root':
            return
        wiki = self.amr.nodes[parent['node']].wiki

        i = 1
        if wiki != '-':
            # new_name = 'wiki~' + wiki + '_' + str(i)
            new_name = '__name' + str(i) + '__'
            while new_name in self.en:
                i = i + 1
                new_name = '__name' + str(i) + '__'

            real_value = []
            for edge in self.amr.edges[root]:
                if ':op' in edge.name:
                    name = self.amr.nodes[edge.node_id].name
                    real_value.append((edge.name, edge.node_id, name))

            real_value.sort(key=lambda x: x[0])
            description = ' '.join(map(lambda x: x[2], real_value))

            # Update name node
            self.amr.nodes[root].name = new_name

            for v in real_value:
                node_id = v[1]
                tokens = self.amr.nodes[node_id].tokens
                for token in tokens:
                    self.en[token] = new_name
                self.amr.nodes[root].tokens.extend(tokens)

                # remove :op nodes
                del self.amr.nodes[node_id]
                del self.amr.edges[node_id]

                edge = filter(lambda x: x.node_id == node_id, self.amr.edges[root])[0]
                self.amr.edges[root].remove(edge)

            self.amr.nodes[root].tokens = sorted(list(set(self.amr.nodes[root].tokens)))
            self.amr.nodes[root].status = '+'

            # Saving the real names to the realization part
            text_name = []
            for token in self.amr.nodes[root].tokens:
                text_name.append((token, self.lex[token]))

            text_name.sort(key=lambda x: x[0])
            text_name = ' '.join(map(lambda x: x[1], text_name))
            self.real_values.append({'tag':new_name, 'edge': ':name', 'constant':description, 'wiki':wiki, 'name': text_name})

    def linearize(self):
        self.de_en.sort(key=operator.itemgetter(2))
        linear = self.de_en

        self.de = map(lambda x: x[0], linear)

    # get the matrix and the alignments map
    def format_moses(self):
        de_en = []

        xdim, ydim = len(self.de_en), len(self.en)
        self.matrix = np.zeros((xdim, ydim))

        for i, w in enumerate(self.de_en):
            for j in w[1]:
                self.matrix[i,j] = 1
                de_en.append((i, j))

        self.de_en = sorted(de_en, key=lambda x:x[1])
        self.de_en = ' '.join(map(lambda x: str(x[0]) + '-' + str(x[1]), self.de_en))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('training_dir', type=str, default='data/LDC2016E25/data/alignments/split/training', help='training path')
    parser.add_argument('de', type=str, default='data/evaluation/-Delex+Compress+Sort/train.de', help='source file')
    parser.add_argument('en', type=str, default='data/evaluation/-Delex+Compress+Sort/train.en', help='target file')
    parser.add_argument('de_en', type=str, default='data/evaluation/-Delex+Compress+Sort/model/aligned.grow-diag-final', help='alignment file')
    parser.add_argument('--lex', type=str, default='data/evaluation/-Delex+Compress+Sort/train.lex', help='lexicalized file')
    parser.add_argument('--references', type=str, default='data/evaluation/-Delex+Compress+Sort/realization/train.cPickle', help='references writing file')
    parser.add_argument('--crf_compressor', type=str, default='compression_crf/data_lex/train.out', help='trained crf compressor path')
    parser.add_argument('--one_step', type=str, default='linearizer/sort_lex/clf_one_step.cPickle', help='trained one step model')
    parser.add_argument('--two_step', type=str, default='linearizer/sort_lex/clf_sort_step.cPickle', help='trained two step model')
    parser.add_argument("--delex", action="store_true", help="delexicalization")
    parser.add_argument("--linearization", action="store_true", help="linearization")
    parser.add_argument("--compression", action="store_true", help="compression")
    parser.add_argument("--save_alignments", action="store_true", help="save alignments")
    args = parser.parse_args()

    TRAINING_DIR = args.training_dir
    DE_FILE = args.de
    EN_FILE = args.en
    DE_EN_FILE = args.de_en
    LEX_FILE = args.lex
    VALUES_FILE = args.references

    # Delexicalized sentences or not
    IS_DELEXICALIZED = args.delex

    IS_COMPRESSED = args.compression

    # CRF COMPRESSOR
    CRF_COMPRESSOR_FILE = args.crf_compressor

    IS_LINEARIZED = args.linearization

    # CLASSIFIER LINEARIZATION
    ONE_STEP_MODEL = args.one_step
    TWO_STEP_MODEL = args.two_step

    # Save alignments or not
    SAVE_ALIGNMENTS = args.save_alignments

    dir = TRAINING_DIR
    dirs = os.listdir(dir)

    crfcompressor = CRFCompressor(fresults=CRF_COMPRESSOR_FILE, stopwords=[])

    clf = Classifier(clf_one_step=ONE_STEP_MODEL, clfs_two_step=TWO_STEP_MODEL)

    amrs = []
    for fname in dirs:
        fread = os.path.join(dir, fname)
        if 'prince' in dir:
            amrs.extend(utils.parse_corpus(fread, True))
        else:
            amrs.extend(utils.parse_corpus(fread, False))

    de = open(DE_FILE, 'w')
    en = open(EN_FILE, 'w')

    if IS_DELEXICALIZED:
        lex = open(LEX_FILE, 'w')
        real_values = {}

    if SAVE_ALIGNMENTS:
        de_en_align = open(DE_EN_FILE, 'w')

    for i, amr in enumerate(amrs):
        try:
            linearizer = clf

            _amr = AMR(nodes={}, edges={}, root='')
            _amr.parse_aligned(amr['amr'].lower())

            parser = Parser(amr=_amr,
                            snt=amr['sentence'].lower(),
                            compressor=(crfcompressor, i),
                            linearizer=linearizer,
                            is_compressed=IS_COMPRESSED,
                            is_linearized=IS_LINEARIZED,
                            is_delexicalized=IS_DELEXICALIZED)

            de.write(' '.join(parser.de).lower())
            de.write('\n')

            en.write(parser.en)
            en.write('\n')

            if SAVE_ALIGNMENTS:
                de_en_align.write(parser.de_en)
                de_en_align.write('\n')

            if IS_DELEXICALIZED:
                lex.write(parser.lex)
                lex.write('\n')

                real_values[i+1] = parser.real_values
        except:
            print i, amr['sentence'].lower()
            print 'error'
            print '\n'
            linear = ''

    de.close()
    en.close()

    # Saving real values for realization
    if IS_DELEXICALIZED:
        p.dump(real_values, open(VALUES_FILE, 'w'))
        lex.close()

    if SAVE_ALIGNMENTS:
        de_en_align.close()