from .graph import Graph, nx


class GridGraph(Graph):
    def __init__(self, height, width, **attr):
        super().__init__(**attr)
        g = nx.grid_2d_graph(height, width)
        self.add_nodes_from(g.nodes)
        self.add_edges_from(g.edges)
