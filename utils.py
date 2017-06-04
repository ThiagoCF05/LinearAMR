__author__ = 'thiagocastroferreira'

import json
import re

people = [u'Obama', u'Bush', u'Gingrich', u'Romney', u'Clinton',
          u'Paul', u'Hussein', u'Jackson', u'Paterno', u'Zimmerman',
          u'Laden', u'Palin', u'Sandusky', u'ElBaradei', u'Beck',
          u'Sarkozy', u'Reagan', u'Gaddafi', u'Santorum', u'Martin',
          u'Putin', u'Murdoch', u'Perry', u'Blair', u'McCain',
          u'Cheney', u'Jesus', u'Limbaugh', u'Brown', u'Truman',
          u'Christie', u'Cameron', u'McQueary', u'Bachmann', u'Clarke',
          u'Zedong', u'Jiabao']

location = [u'China', u'Iran', u'Russia', u'Japan', u'India', u'Pakistan',
            u'Afghanistan', u'Iraq', u'France', u'Israel', u'Europe',
            u'Australia', u'Vietnam', u'Germany', u'Taiwan', u'Libya',
            u'Thailand', u'Beijing', u'Asia', u'Spain', u'Singapore',
            u'Egypt', u'Estonia', u'Indonesia', u'Laos', u'Canada', u'London',
            u'Jordan', u'Syria', u'Brazil']

wiki_info = json.load(open('/Users/thiagocastroferreira/Documents/Doutorado/Third_Chapter/LinearAMR/data/wiki/wiki_info.json'))

def parse_aligned_corpus(fname):
    with open(fname) as f:
        doc = f.read()

    instances = doc.split('\n\n')[1:]

    amrs = []
    for instance in instances:
        try:
            instance = instance.split('\n')
            sentence_id = instance[0].split()[2]
            sentence = ' '.join(instance[1].split()[2:])
            alignments = instance[2].split()[2:]
            amr = '\n'.join(instance[3:])

            amrs.append({'id':sentence_id, 'file':fname, 'sentence': sentence, 'alignments': alignments, 'amr': amr})
        except:
            pass
    return amrs

def parse_corpus(fname, prince=False):
    with open(fname) as f:
        doc = f.read()

    instances = doc.split('\n\n')[1:]

    amrs = []
    for instance in instances:
        try:
            instance = instance.split('\n')
            # sentence_id = instance[0].split()[2]
            sentence = ' '.join(instance[1].split()[2:])
            if prince:
                amr = '\n'.join(instance[4:])
            else:
                amr = '\n'.join(instance[3:])

            amrs.append({'file':fname, 'sentence': sentence, 'amr': amr})
        except:
            pass
    return amrs

def get_stopwords(fname):
    f = open(fname)
    stopwords = f.read()
    f.close()

    stopwords = map(lambda x: x.strip(), stopwords.split('\n'))
    return stopwords

def noun_verb(fname):
    verb2noun, noun2verb = {}, {}
    verb2actor, actor2verb = {}, {}
    with open(fname) as f:
        doc = f.read()

    for row in doc.split('\n'):
        regex = re.compile("""::DERIV-VERB \"(.+?)\"""")
        verb = regex.match(row).groups()[0]

        regex = re.compile("""::DERIV-NOUN \"(.+?)\"""")
        m = regex.search(row)
        if m != None:
            noun = m.groups()[0]
            verb2noun[verb] = noun
            noun2verb[noun] = verb

        regex = re.compile("""::DERIV-NOUN-ACTOR \"(.+?)\"""")
        m = regex.search(row)
        if m != None:
            actor = m.groups()[0]
            verb2actor[verb] = actor
            actor2verb[actor] = verb

    return verb2noun, noun2verb, verb2actor, actor2verb

def subgraph_word(fname):
    sub2word = {}

    with open(fname) as f:
        doc = f.read()

    regex1 = re.compile("""VERBALIZE (.+) TO (.+)""")
    regex2 = re.compile("""MAYBE-VERBALIZE (.+) TO (.+)""")

    for row in doc.split('\n'):
        m = regex1.match(row)
        if m == None:
            m = regex2.match(row)

        if m != None:
            aux = m.groups()
            word = aux[0]

            _subgraph = aux[1].split()
            root = _subgraph[0]
            subgraph = [root]

            node, edge = '', ''
            for instance in _subgraph[1:]:
                if instance[0] == ':':
                    edge = instance
                else:
                    node = instance
                    subgraph.append((edge, node))
            subgraph = tuple(subgraph)
            if subgraph not in sub2word:
                sub2word[subgraph] = [word]
            else:
                sub2word[subgraph].append(word)

    return sub2word

def isPropbank(name):
    regex = re.compile('(.*)-[0-9]+')
    m = regex.match(name)
    if m != None:
        name = m.groups()[0]
    return name
