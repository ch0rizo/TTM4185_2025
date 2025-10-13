from .graph import Graph, nx, plt

class PetersenGraph(Graph):
    def __init__(self,**attr):
        super().__init__(**attr)
        g = nx.petersen_graph()
        self.add_nodes_from(g.nodes)
        self.add_edges_from(g.edges)
        # self.color_nodes()

    def draw_graph(self):
        # Draw with position 
        pos = nx.multipartite_layout(self)
        nx.draw(self, pos, with_labels=True)
        plt.show()
