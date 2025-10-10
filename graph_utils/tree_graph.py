from .graph import Graph, nx


class TreeGraph(Graph):
    def __init__(self, splits, height, **attr):
        super().__init__(**attr)
        g = nx.balanced_tree(splits, height)
        self.add_nodes_from(g.nodes)
        self.add_edges_from(g.edges)
