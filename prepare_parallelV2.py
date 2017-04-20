import cPickle as p
import utils
import operator
import os

import numpy as np

from ERG import AMR
from compression_tree.compressor import Compressor
from compression_crf.crfcompressor import CRFCompressor
from linearizer.majority import Majority
from linearizer.classifier import Classifier

TRAINING_DIR = 'data/LDC2016E25/data/alignments/split/test'
DE_FILE = 'data/final_evaluation/test/test.de'
EN_FILE = 'data/final_evaluation/test/test.en'
DE_EN_FILE = 'data/final_evaluation/test/model/aligned.grow-diag-final'
LEX_FILE = 'data/final_evaluation/test/test.lex'
VALUES_FILE = 'data/final_evaluation/test/realization/test.cPickle'

# CRF COMPRESSOR
CRF_COMPRESSOR_FILE = 'compression_crf/data_delex/test.out'

# COMPRESSOR DATA
CLF_NODE_PATH = 'compression_tree/training/results/clf_node.cPickle'
CLF_EDGE_PATH = 'compression_tree/training/results/clf_edge.cPickle'
EDGE_PATH = 'compression_tree/training/validation/edge_feat.cPickle'
EDGE_PARENT_PATH = 'compression_tree/training/validation/edge_parent_feat.cPickle'
EDGE_CHILD_PATH = 'compression_tree/training/validation/edge_child_feat.cPickle'
NODE_PATH = 'compression_tree/training/validation/node_feat.cPickle'
NODE_PARENT_PATH = 'compression_tree/training/validation/node_parent_feat.cPickle'

# STOP WORDS
STOP_WORDS_PATH = 'data/AMR_stopwords.txt'

# LINEARIZATION: gold - dfs - maj - clf / COMPRESSION: gold - classifier - all - crf - crfstop
DATA_TYPE = 'clf_crf'

# MAJORITY LINEARIZATION
MAJORITY_MODEL_PATH = 'linearizer/lm/majority.json'
MAJORITY_DELEX_MODEL_PATH = 'linearizer/lm/majority_delex.json'

# CLASSIFIER LINEARIZATION
ONE_STEP_MODEL = 'linearizer/steps_delex/clf_one_step.cPickle'
TWO_STEP_MODEL = 'linearizer/steps_delex/clf_two_step.cPickle'

# Save alignments or not
SAVE_ALIGNMENTS = False

# Delexicalized sentences or not
IS_DELEXICALIZED = True

class Parser(object):
    def __init__(self, amr, snt, data_type, compressor, linearizer, is_delexicalized):
        self.en = snt.split()
        self.lex = snt.split()
        self.de_en = []
        self.de = ''
        self.matrix = []
        self.real_values = []
        self.is_delexicalized = is_delexicalized

        self.amr = amr

        # DELEXICALIZATION
        self.amr.remove_senses()
        if self.is_delexicalized:
            self.delexicalize(self.amr.root)
            self.remove_delexicalized_repetitions()

        # COMPRESSION
        self.order_type, self.compress_type  = data_type.split('_')
        if self.compress_type == 'tree':
            self.amr = compressor.compress(self.amr)
        elif self.compress_type == 'all':
            self.amr.include_all()
        elif self.compress_type == 'crf':
            compressor, index = compressor
            self.amr = compressor.process(self.amr, index)

        # LINEARIZATION
        if self.order_type == 'maj' and linearizer != None:
            self.amr.order_by_majority(linearizer)
        if self.order_type == 'clf' and linearizer != None:
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
            new_name = str(i)
            while new_name in self.en:
                i = i + 1
                new_name = str(i)

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
        wiki_info = filter(lambda x: x['wiki'].lower() == wiki.lower(), utils.wiki_info)


        if wiki != '-' and len(wiki_info) > 0:
            wiki_info = wiki_info[0]

            tags = []
            if wiki_info['type'] == 'other':
                return
            elif wiki_info['type'] == 'location':
                tags = utils.location
            else:
                tags = utils.people

            i = 0
            new_name = tags[0].lower()
            while new_name in self.en:
                i = i + 1
                new_name = tags[i].lower()
            new_name = new_name.encode('utf-8')

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
        if self.order_type == 'gold':
            linear = []
            for elem in self.de_en:
                name, tokens, order_id = elem
                for token in tokens:
                    if (name, token, order_id) not in linear:
                        linear.append((name, token, order_id))
                        break

            linear.sort(key=operator.itemgetter(1, 2))
            de_en = []
            for l in linear:
                tokens = filter(lambda x: x[0] == l[0] and l[1] in x[1] and l[2] == x[2], self.de_en)[0][1]
                de_en.append((l[0], tokens, l[2]))

            self.de_en = de_en
        else:
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

    def format_giza(self):
        # de
        # self.giza_de = 'NULL ({ }) '
        self.giza_de = ''
        for i in range(self.matrix.shape[0]):
            self.giza_de += self.de[i] + ' ({ '
            for j in range(self.matrix.shape[1]):
                if self.matrix[i,j] > 0:
                    self.giza_de += str(j+1) + ' '
            self.giza_de += '}) '
        self.giza_de = self.giza_de.strip()

        # en
        self.giza_en = 'NULL ({ }) '
        # self.giza_en = ''
        nulls = []
        for j in range(self.matrix.shape[1]):
            self.giza_en += self.en[j] + ' ({ '
            isNull = True
            for i in range(self.matrix.shape[0]):
                if self.matrix[i,j] > 0:
                    self.giza_en += str(i+1) + ' '
                    isNull = False
            if isNull:
                nulls.append(j)
            self.giza_en += '}) '
        self.giza_en = self.giza_en.strip()

        # null
        null = 'NULL ({ '
        for n in nulls:
            null += str(n+1) + ' '
        null += '}) '
        self.giza_de = null + self.giza_de

if __name__ == '__main__':
    dir = TRAINING_DIR
    dirs = os.listdir(dir)

    if 'crfstop' in DATA_TYPE:
        stopwords = utils.get_stopwords(STOP_WORDS_PATH)
        crfcompressor = CRFCompressor(fresults=CRF_COMPRESSOR_FILE, stopwords=stopwords)
    else:
        crfcompressor = CRFCompressor(fresults=CRF_COMPRESSOR_FILE, stopwords=[])

    compressor = Compressor(clf_node_path=CLF_NODE_PATH,
                            clf_edge_path=CLF_EDGE_PATH,
                            edge_path=EDGE_PATH,
                            edge_parent_path=EDGE_PARENT_PATH,
                            edge_child_path=EDGE_CHILD_PATH,
                            node_path=NODE_PATH,
                            node_parent_path=NODE_PARENT_PATH)

    maj = Majority(model_path=MAJORITY_MODEL_PATH, delex_model_path=MAJORITY_DELEX_MODEL_PATH)

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
            linearizer = maj
            if 'clf' in DATA_TYPE:
                linearizer = clf

            _amr = AMR(nodes={}, edges={}, root='')
            _amr.parse_aligned(amr['amr'].lower())

            parser = Parser(amr=_amr,
                            snt=amr['sentence'].lower(),
                            data_type=DATA_TYPE,
                            compressor=(crfcompressor, i),
                            linearizer=linearizer,
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