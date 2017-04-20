
from ERG import AMR

class CRFCompressor(object):
    def __init__(self, fresults, stopwords = []):
        self.results = self.parse_results(fresults)
        self.stopwords = stopwords

    def parse_results(self, path):
        f = open(path)
        doc = f.read()
        f.close()

        results = []
        amrs = doc.split('\n\n')
        for amr in amrs:
            _amr = amr.split('\n')
            results.append(_amr)

        return results

    def include_all(self, amr):
        if type(amr) == str:
            _amr = AMR(nodes={}, edges={}, root='')
            _amr.parse_aligned(amr)
            amr = _amr

        for node in amr.nodes:
            amr.nodes[node].status = '+'

            for edge in amr.edges[node]:
                edge.status = '+'
        return amr

    def process(self, amr, index):
        self.amr = amr
        self.result = self.results[index]
        self.compress(self.amr.root, 0)
        return self.amr

    def compress(self, root, order_id):
        if self.amr.nodes[root].name in self.stopwords:
            self.amr.nodes[root].status = '-'
        else:
            self.amr.nodes[root].status = self.result[order_id]
        order_id = order_id + 1

        for edge in self.amr.edges[root]:
            if edge.name in self.stopwords:
                edge.status = '-'
            else:
                edge.status = self.result[order_id]
            order_id = order_id + 1

            order_id = self.compress(edge.node_id, order_id)
        return order_id