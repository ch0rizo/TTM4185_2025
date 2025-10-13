from .graph import Graph, nx


class RingGraph(Graph):
    def __init__(self, n, **attr):
        super().__init__(**attr)
        g = nx.cycle_graph(n)
        self.add_nodes_from(g.nodes)
        self.add_edges_from(g.edges)
