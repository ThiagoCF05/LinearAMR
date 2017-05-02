import json
import os
import operator
import utils

import urllib

from ERG import AMR
from rdflib import Graph, URIRef

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

def get_type(uri):
    try:
        uri = URIRef(uri)
        person = URIRef('http://dbpedia.org/ontology/Person')
        g = Graph()
        g.parse(uri)
        # person
        resp = g.query(
            "ASK {?uri a ?person}",
            initBindings={'uri': uri, 'person': person}
        )
        if resp.askAnswer:
            return 'person'

        # location
        loc = URIRef('http://dbpedia.org/ontology/Location')
        resp = g.query(
            "ASK {?uri a ?loc}",
            initBindings={'uri': uri, 'loc': loc}
        )
        if resp.askAnswer:
            return 'location'

        # organization
        org = URIRef('http://dbpedia.org/ontology/Organization')
        resp = g.query(
            "ASK {?uri a ?org}",
            initBindings={'uri': uri, 'org': org}
        )
        if resp.askAnswer:
            return 'organization'
    except:
        print 'ERROR: ', uri
    return 'other'

def get_training_freq():
    training = 'data/LDC2016E25/data/amrs/split/training'

    amrs = []
    for fname in os.listdir(training):
        amrs.extend(utils.parse_corpus(os.path.join(training, fname)))

    wiki_dict = {}

    for _amr in amrs:
        amr = AMR(nodes={}, edges={}, root=1)
        amr.parse_aligned(_amr['amr'])

        for node in amr.nodes:
            wiki = amr.nodes[node].wiki
            if wiki != '-':
                if wiki not in wiki_dict:
                    wiki_dict[wiki] = 0

                wiki_dict[wiki] += 1

    json.dump(wiki_dict, open('wiki.json', 'w'), sort_keys=True, indent=4, separators=(',', ': '))

def get_entity_info():
    dirs = ['data/LDC2016E25/data/amrs/split/training',
            'data/LDC2016E25/data/amrs/split/dev',
            'data/LDC2016E25/data/amrs/split/test']

    amrs = []
    for dir in dirs:
        for fname in os.listdir(dir):
            amrs.extend(utils.parse_corpus(os.path.join(dir, fname)))

    wiki_dict = []
    wiki_info = []
    for _amr in amrs:
        try:
            amr = AMR(nodes={}, edges={}, root=1)
            amr.parse_aligned(_amr['amr'])

            for node in amr.nodes:
                wiki = amr.nodes[node].wiki
                if wiki != '-':
                    if wiki not in wiki_dict:
                        print wiki
                        wiki_dict.append(wiki)

                        uri = 'http://dbpedia.org/resource/' + urllib.quote_plus(wiki)
                        _type = get_type(uri)
                        wiki_info.append({'wiki':wiki, 'type':_type})
        except:
            'ERROR'

    json.dump(wiki_info, open('wiki_info.json', 'w'), sort_keys=True, indent=4, separators=(',', ': '))

def filter_by_type():
    wiki = json.load(open('wiki.json'))
    info = json.load(open('wiki_info.json'))

    wiki_p, wiki_loc, wiki_other = {}, {}, {}

    for entity in wiki:
        type = filter(lambda x: x['wiki'] == entity, info)[0]['type']

        if type == 'person':
            wiki_p[entity] = wiki[entity]
        elif type == 'location':
            wiki_loc[entity] = wiki[entity]
        else:
            wiki_other[entity] = wiki[entity]

    json.dump(wiki_p, open('wiki_p.json', 'w'), sort_keys=True, indent=4, separators=(',', ': '))
    json.dump(wiki_loc, open('wiki_loc.json', 'w'), sort_keys=True, indent=4, separators=(',', ': '))
    json.dump(wiki_other, open('wiki_other.json', 'w'), sort_keys=True, indent=4, separators=(',', ': '))

if __name__ == '__main__':
    dirs = ['data/LDC2016E25/data/amrs/split/training',
            'data/LDC2016E25/data/amrs/split/dev',
            'data/LDC2016E25/data/amrs/split/test']
    amrs = []
    for dir in dirs:
        for fname in os.listdir(dir):
            amrs.extend(utils.parse_corpus(os.path.join(dir, fname)))

    wiki_dict = []
    wiki_info = []
    concepts = [0, 0]
    for _amr in amrs:
        amr = AMR(nodes={}, edges={}, root=1)
        amr.parse_aligned(_amr['amr'])
        for node in amr.nodes:
            if amr.nodes[node].constant:
                concepts[0] += 1
        concepts[1] += len(amr.nodes)
    print concepts

    # Step 1
    # get_training_freq()
    # get_entity_info()

    # Step 2
    # filter_by_type()

    # Step 3
    # location = json.load(open('data/wiki/wiki_other.json'))
    #
    # location = sorted(location.items(), key=operator.itemgetter(1), reverse=True)
    #
    # i = 0
    # l = []
    # for loc in location[:30]:
    #     if len(loc[0].split('_')) == 1:
    #         name = loc[0].split('_')[-1].split('-')[-1]
    #         if name not in l:
    #             l.append(name)
    #             i += 1
    #     if i == 40:
    #         break
    # print l

