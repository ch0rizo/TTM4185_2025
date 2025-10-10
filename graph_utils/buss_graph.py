from .graph import Graph, nx


class BussGraph(Graph):
    def __init__(self, n, **attr):
        super().__init__(**attr)
        g = nx.path_graph(n)
        self.add_nodes_from(g.nodes)
        self.add_edges_from(g.edges)
