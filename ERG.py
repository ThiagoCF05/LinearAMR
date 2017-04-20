__author__ = 'thiagocastroferreira'

import copy
import re
import utils

class AMREdge(object):
    def __init__(self, name, order_id, node_id, isRule=False, status='', tokens=[]):
        self.order_id = order_id
        self.name = name
        self.node_id = node_id
        self.isRule = isRule
        self.tokens = tokens
        self.status = status

class AMRNode(object):
    def __init__(self, id, order_id, name, parent, status, tokens, constant):
        self.id = id
        self.order_id = order_id
        self.name = name
        self.parent = parent
        self.status = status
        self.tokens = tokens
        self.wiki = '-'
        self.constant = constant

class AMR(object):
    def __init__(self, nodes={}, edges={}, root=''):
        self.nodes = nodes
        self.edges = edges
        self.root = root

    def get_rules(self, root='', rules=[]):
        for edge in self.edges[root]:
            if edge.isRule:
                rules.append(edge.node_id)
            else:
                rules = self.get_rules(edge.node_id, rules)
        return rules

    def isPropbank(self, name):
        regex = re.compile('(.*)-[0-9]+')
        m = regex.match(name)
        if m != None:
            if m.groups()[0].strip() != '':
                name = m.groups()[0]
        return name

    def include_all(self):
        for node in self.nodes:
            self.nodes[node].status = '+'

            for edge in self.edges[node]:
                edge.status = '+'

    def compress(self, root, sub2word):
        # filter subgraphs with the root given as a parameter which the related word is in the sentence
        subgraphs = filter(lambda iter: iter[0][0] == self.nodes[root].name, sub2word.iteritems())

        # subgraphs, lemma = [], ''
        # for candidate in f:
        #     for _lemma in filter(lambda x: x[1] == 'unlabeled', self.lemmas):
        #         if _lemma[0] in candidate[1]:
        #             subgraphs.append(candidate[0])
        #             lemma = _lemma[0]
        #             break

        if len(subgraphs) > 0:
            subgraphs = sorted(subgraphs, key=len)
            subgraphs.reverse()

            matched = True
            filtered_subgraph = [self.nodes[root].name]
            for sub in subgraphs:
                matched = True
                for edge in sub[1:]:
                    f = filter(lambda match_edge: match_edge.name == edge[0] and self.nodes[match_edge.node_id].name == edge[1], self.edges[root])
                    if len(f) > 0:
                        filtered_subgraph.append(f[0])
                    else:
                        matched = False
                        filtered_subgraph = [self.nodes[root].name]
                        break
                if matched:
                    break

            if matched:
                pass

    def remove_senses(self):
        for node in self.nodes:
            self.nodes[node].name = self.isPropbank(self.nodes[node].name)

    def parse_aligned(self, amr):
        self.edges['root'] = []

        node_id, edge, node_tokens, edge_tokens = '', ':root', [], []
        edge_status = '-'
        parent = 'root'
        for instance in amr.replace('/', '').split():
            closing = 0
            for i in range(len(instance)):
                if instance[-(i+1)] == ')':
                    closing = closing + 1
                else:
                    break
            if closing > 0:
                instance = instance[:-closing]

            if instance[0] == ':':
                instance = instance.split('~e.')
                edge = instance[0].strip()

                edge_status = '-'
                if len(instance) > 1:
                    edge_tokens.extend(map(lambda x: int(x), instance[1].split(',')))
                    edge_status = '+'
            elif instance[0] == '(':
                node_id = instance[1:].strip()
            else:
                instance = instance.replace('\'', '').replace('\"', '').split('~e.')
                name = instance[0].strip()

                node_status = '-'
                if len(instance) > 1:
                    node_tokens.extend(map(lambda x: int(x), instance[1].split(',')))
                    node_status = '+'

                if node_id != '':
                    if node_id in self.nodes.keys():
                        i = 1
                        node_id = node_id + '~' + str(i)
                        while node_id in self.nodes.keys():
                            i += 1
                            node_id = node_id + '~' + str(i)

                    node = AMRNode(id=node_id, name=name, order_id=-1, parent={'node':parent, 'edge':edge}, status=node_status, tokens=sorted(list(set(node_tokens))), constant=False)
                    self.nodes[node_id] = node

                    self.edges[node_id] = []
                    _edge = AMREdge(name=edge, node_id=node_id, order_id=-1, status=edge_status, tokens=edge_tokens)
                    self.edges[parent].append(_edge)

                    parent = node_id
                else:
                    if edge not in [':wiki']:
                        _node = copy.copy(name)
                        i, isCoref = 1, False
                        while _node in self.nodes.keys():
                            _node = name + '-coref' + str(i)
                            isCoref = True
                            i = i + 1
                        if isCoref:
                            name = self.nodes[name].name

                        node = AMRNode(id=_node, name=name, order_id=-1, parent={'node':parent, 'edge':edge}, status=node_status, tokens=sorted(list(set(node_tokens))), constant=True)
                        self.nodes[_node] = node

                        self.edges[_node] = []

                        _edge = AMREdge(name=edge, node_id=_node, order_id=-1, status=edge_status, tokens=edge_tokens)
                        self.edges[parent].append(_edge)
                    else:
                        node.wiki = name
                node_id, node_tokens, edge_tokens = '', [], []

            for i in xrange(closing):
                parent = self.nodes[parent].parent['node']
        self.root = self.edges['root'][0].node_id

    def order(self, root, order_id):
        self.nodes[root].order_id = order_id
        order_id += 1

        for i, edge in enumerate(self.edges[root]):
            self.edges[root][i].order_id = order_id
            order_id += 1

            order_id = self.order(edge.node_id, order_id)

        return order_id

    def order_by_majority(self, majority):

        majority.set_amr(self)
        majority.linearize(self.root, 1)

    def delexicalize(self, root, real_values):
        parent = self.nodes[root].parent
        if parent['node'] == 'root':
            parent_node = ''
        else:
            parent_node = self.nodes[parent['node']].name
        parent_edge = parent['edge']

        name = self.nodes[root].name
        if self.nodes[root].constant and (parent_edge in [':quant', ':value'] or parent_node == 'date-entity'):
            i = 1
            new_name = '__' + parent_edge[1:] + str(i) + '__'
            # new_name = str(i)
            while len(filter(lambda x: x['tag'] == new_name, real_values)) > 0:
                i = i + 1
                new_name = '__' + parent_edge[1:] + str(i) + '__'
                # new_name = str(i)

            real_values.append({'tag':new_name, 'edge':parent_edge, 'constant':name, 'wiki':'-'})

            self.nodes[root].name = new_name
        elif parent_edge == ':name':
            real_values = self.delexicalize_name(root, real_values)

        for edge in self.edges[root]:
            real_values = self.delexicalize(edge.node_id, real_values)
        return real_values

    def delexicalize_nameV2(self, root, real_values):
        parent = self.nodes[root].parent
        if parent['node'] == 'root':
            return real_values
        wiki = self.nodes[parent['node']].wiki
        wiki_info = filter(lambda x: x['wiki'].lower() == wiki.lower(), utils.wiki_info)

        if wiki != '-' and len(wiki_info) > 0:
            wiki_info = wiki_info[0]

            tags = []
            if wiki_info['type'] == 'other':
                return real_values
            elif wiki_info['type'] == 'location':
                tags = utils.location
            else:
                tags = utils.people

            i = 0
            new_name = tags[0].lower()
            while len(filter(lambda x: x['tag'] == new_name, real_values)):
                i = i + 1
                new_name = tags[i].lower()
            new_name = new_name.encode('utf-8')

            real_value = []
            for edge in self.edges[root]:
                if ':op' in edge.name:
                    name = self.nodes[edge.node_id].name
                    real_value.append((edge.name, edge.node_id, name))

            real_value.sort(key=lambda x: x[0])
            description = ' '.join(map(lambda x: x[2], real_value))

            # Update name node
            self.nodes[root].name = new_name

            for v in real_value:
                node_id = v[1]
                tokens = self.nodes[node_id].tokens
                self.nodes[root].tokens.extend(tokens)

                # remove :op nodes
                del self.nodes[node_id]
                del self.edges[node_id]

                edge = filter(lambda x: x.node_id == node_id, self.edges[root])[0]
                self.edges[root].remove(edge)

            self.nodes[root].tokens = sorted(list(set(self.nodes[root].tokens)))
            self.nodes[root].status = '+'

            real_values.append({'tag':new_name, 'edge': ':name', 'constant':description, 'wiki':wiki})
        return real_values

    # Old version. Introduced in EMNLP 2017 submission
    def delexicalize_name(self, root, real_values):
        parent = self.nodes[root].parent
        if parent['node'] == 'root':
            return real_values
        wiki = self.nodes[parent['node']].wiki
        i = 1
        if wiki != '-':
            # new_name = 'wiki~' + wiki + '_' + str(i)
            new_name = '__name' + str(i) + '__'
            while len(filter(lambda x: x['tag'] == new_name, real_values)) > 0:
                i = i + 1
                new_name = '__name' + str(i) + '__'

            real_value = []
            for edge in self.edges[root]:
                if ':op' in edge.name:
                    name = self.nodes[edge.node_id].name
                    real_value.append((edge.name, edge.node_id, name))

            real_value.sort(key=lambda x: x[0])
            description = ' '.join(map(lambda x: x[2], real_value))

            # Update name node
            self.nodes[root].name = new_name

            for v in real_value:
                node_id = v[1]
                tokens = self.nodes[node_id].tokens
                self.nodes[root].tokens.extend(tokens)

                # remove :op nodes
                del self.nodes[node_id]
                del self.edges[node_id]

                edge = filter(lambda x: x.node_id == node_id, self.edges[root])[0]
                self.edges[root].remove(edge)

            self.nodes[root].tokens = sorted(list(set(self.nodes[root].tokens)))
            self.nodes[root].status = '+'

            real_values.append({'tag':new_name, 'edge': ':name', 'constant':description, 'wiki':wiki})
        return real_values

    def prettify(self, head='', root='', print_constants=True):
        def print_amr(root, head, amr, level):
            closing = False
            level = level + 1
            if '-coref' in root:
                if '--' in root:
                    amr = amr + ' -'
                else:
                    amr = amr + ' ' + root.split('-')[0]
            elif self.nodes[root].constant:
                if print_constants:
                    amr = amr + ' ' + self.nodes[root].name
                else:
                    amr = amr + ' ' + 'c'
            else:
                if self.nodes[root].name == head:
                    amr = amr + ' (XXX'
                else:
                    amr = amr + ' (' + root.split('~')[0] + ' / ' + self.nodes[root].name
                closing = True

            for edge in self.edges[root]:
                amr = amr + ' \n' + (level * '\t') + ' ' + edge.name
                if not edge.isRule:
                    amr = print_amr(edge.node_id, head, amr, level)
                else:
                    amr = amr + ' -'
            if closing:
                amr = amr + ')'
            return amr.strip()

        if root == '':
            root = self.edges['root'][0].node_id
        return print_amr(root, head, '', 0)