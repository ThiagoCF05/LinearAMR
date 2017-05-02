
import sys
sys.path.append('home/tcastrof/workspace/stanford_corenlp_pywrapper')
from stanford_corenlp_pywrapper import CoreNLP

class Delexicalizer(object):
    def __init__(self, gigaword, delex_gigaword):
        print 'Initializing Stanford CoreNLP'
        self.proc = CoreNLP("ner")

        print 'Loading corpus...'
        f = open(gigaword)
        doc = f.read()
        f.close()

        print 'Processing paragraphs...'
        f = open(delex_gigaword, 'w')
        for paragraph in doc.split('\n'):
            parsed = self.proc_paragraph(paragraph)
            f.write(parsed.encode('utf-8').lower())
            f.write('\n')
        f.close()

    def proc_paragraph(self, paragraph):
        out = self.proc.parse_doc(paragraph)

        parsed_paragraph = {'entitymentions':[], 'tokens':[]}
        for snt in out['sentences']:
            parsed_paragraph['entitymentions'].extend(snt['entitymentions'])
            parsed_paragraph['tokens'].extend(snt['tokens'])

        delex = self.proc_snt(parsed_paragraph)
        return delex

    def proc_snt(self, snt):
        quant, value, name = 1, 1, 1

        # Delexicalizing
        for entitymention in snt['entitymentions']:
            tag = ''
            if entitymention['type'] in ['PERSON', 'LOCATION', 'ORGANIZATION', 'MISC']:
                tag = '__name' + str(name) + '__'
                name += 1
            elif entitymention['type'] in ['PERCENT', 'ORDINAL']:
                tag = '__value' + str(value) + '__'
                value += 1
            elif entitymention['type'] in ['NUMBER', 'MONEY']:
                tag = '__quant' + str(quant) + '__'
                quant += 1

            if tag != '':
                begin, end = entitymention['tokspan']
                for tokspan in range(begin, end):
                    snt['tokens'][tokspan] = tag

        # Removing repetitions
        tokens = snt['tokens']
        new_snt = []
        for i, token in enumerate(tokens):
            if i == 0:
                new_snt.append(token)
            elif (token == tokens[i-1] and ((token[:2] == '__' and token[-2:] == '__'))):
                pass
            else:
                new_snt.append(token)
        return (' '.join(new_snt)).replace('-LRB-', '(').replace('-RRB-', ')')

if __name__ == '__main__':
    gigaword = '/roaming/tcastrof/gigaword/gigaword.delex'
    delex_gigaword = '/roaming/tcastrof/gigaword/gigaword.tok.delex'

    delex = Delexicalizer(gigaword=gigaword, delex_gigaword=delex_gigaword)