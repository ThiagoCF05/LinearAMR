__author__ = 'thiagocastroferreira'

"""
Author: Thiago Castro Ferreira
Date: 03/2017
Description:
    Extract all transliterations to insert in the training data for the PBMT model
"""
import utils
import os

from ERG import AMR

AMR_DIR = 'data/LDC2016E25/data/alignments/unsplit'
DE_FILE = 'trans.de'
EN_FILE = 'trans.en'
DE_EN_FILE = 'trans.de_en'

class Transliteration(object):
    def __init__(self):
        pass

    def extract(self, root):
        de = ''
        en = ''
        de_en = ''

        nodes = []
        for edge in self.amr.edges[root]:
            isConstant = self.amr.nodes[edge.node_id].constant

            if isConstant:
                if len(edge.tokens) > 0:
                    nodes.append((edge.name, min(edge.tokens), edge.order_id, edge.tokens))

                node_name = self.amr.nodes[edge.node_id].name
                node_tokens = self.amr.nodes[edge.node_id].tokens
                order_id = self.amr.nodes[edge.node_id].order_id
                if len(node_tokens) > 0:
                    nodes.append((node_name, min(node_tokens), order_id, node_tokens))

        if len(nodes) > 0:
            de_en = []
            nodes.sort(key=lambda x: (x[1], x[2]))
            de = ' '.join(map(lambda x: x[0], nodes))
            pos = 0
            token2pos = {}
            for i, node in enumerate(nodes):
                tokens = node[3]
                for token in tokens:
                    if token in token2pos:
                        de_en.append((i, token2pos[token]))
                    elif self.snt[token] not in en.split():
                        en += self.snt[token]
                        en += ' '
                        token2pos[token] = pos
                        de_en.append((i, pos))
                        pos += 1

            de_en = sorted(de_en, key=lambda x:x[1])
            de_en = ' '.join(map(lambda x: str(x[0]) + '-' + str(x[1]), de_en))
        return de.strip(), en.strip(), de_en.strip()

    def run(self, amr, snt):
        self.snt = snt.split()
        self.amr = amr

        self.result = []

        for node in self.amr.nodes:
            parent = self.amr.nodes[node].parent

            name = self.amr.nodes[node].name
            if (name == 'name' and parent['edge'] == ':name') or name == 'date-entity':
                de, en, de_en = self.extract(node)
                if de != '':
                    self.result.append({'de':de, 'en':en, 'de_en':de_en})
            elif parent['edge'] in [':quant', ':value']:
                de, en, de_en = self.extract(parent['node'])
                if de != '':
                    self.result.append({'de':de, 'en':en, 'de_en':de_en})

        return self.result

if __name__ == '__main__':
    dir = AMR_DIR
    dirs = os.listdir(dir)

    amrs = []
    for fname in dirs:
        fread = os.path.join(dir, fname)
        if 'prince' in dir:
            amrs.extend(utils.parse_corpus(fread, True))
        else:
            amrs.extend(utils.parse_corpus(fread, False))

    de = open(DE_FILE, 'w')
    en = open(EN_FILE, 'w')
    de_en = open(DE_EN_FILE, 'w')

    parser = Transliteration()

    for i, amr in enumerate(amrs):
        try:
            _amr = AMR(nodes={}, edges={}, root='')
            _amr.parse_aligned(amr['amr'].lower())

            for args in parser.run(_amr, amr['sentence'].lower()):
                de.write(args['de'])
                de.write('\n')

                en.write(args['en'])
                en.write('\n')

                de_en.write(args['de_en'])
                de_en.write('\n')
        except:
            print i, amr['sentence'].lower()
            print 'error'
            print '\n'
            linear = ''

    de.close()
    en.close()
    de_en.close()