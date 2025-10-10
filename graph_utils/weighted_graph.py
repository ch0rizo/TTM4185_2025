from .graph import Graph, nx, plt

class WeightedGraph(Graph):
    def __init__(self):
        super().__init__()
        self.make_exam_graph()

    # Hinder the user from adding edges without weight
    def add_edge(self, node1, node2):
        raise NotImplementedError("This method is not implemented in this graph, use add_edges_with_weigth instead")

    # Hinder the user from adding edges without weight
    def add_edges_from(self, ebunch_to_add, **attr):
        raise NotImplementedError("This method is not implemented in this graph, use add_edges_with_weigth_from instead")

    # Methods for adding nodes 
    def add_nodes(self, nodes):
        self.graph.add_nodes_from(nodes)

    # Method for adding a single edge with weight
    def add_edge_with_weigth(self, node1, node2, weight):
        self.graph.add_edge(node1, node2, weight=weight)
    
    # Method for adding multiple edges with weight
    def add_edges_with_weight_from(self, edges):
        for edge in edges:
            self.graph.add_edge(edge[0], edge[1], weight=edge[2])

    # Method for drawing the graph with edges and weights and then present it like a map
    def draw(self):
        plt.figure(figsize=(12, 8))  # Increase figure size for better spacing

        # Fixed positions for each city to make it readable and consistent
        pos = {
            "Szczecin": (0, 4),
            "Kolobrzeg": (1, 6),
            "Gdansk": (3, 6),
            "Bialystok": (5, 5),
            "Warszawa": (4, 4),
            "Bygdgoszcz": (2, 5),
            "Poznan": (2, 3)
        }

        # Draw the graph
        nx.draw(self.graph, pos, with_labels=False, node_size=700, node_color="lightblue", edge_color="gray")

        # Adjust node labels to be slightly above nodes
        label_pos = {k: (v[0], v[1] + 0.2) for k, v in pos.items()}
        nx.draw_networkx_labels(self.graph, label_pos, font_size=12, font_weight="bold")

        # Extract weights and draw edge labels
        edge_labels = {(u, v): self.graph[u][v]['weight'] for u, v in self.graph.edges()}
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels, font_size=10, font_color='red')

        # Add title and show the plot
        plt.title("Excerpt of Poland's Network Topology", fontsize=20)
        plt.show()

    # Method making the graph topology
    def make_exam_graph(self): 
        self.graph = nx.Graph()
        nodes = ["Szczecin", "Kolobrzeg", "Gdansk", "Bygdgoszcz", "Poznan", "Warszawa", "Bialystok"]
        edges = [
            ("Szczecin", "Kolobrzeg", 140),
            ("Kolobrzeg", "Gdansk", 230),
            ("Gdansk", "Bialystok", 360),
            ("Szczecin", "Poznan", 200),
            ("Poznan", "Bygdgoszcz", 110),
            ("Kolobrzeg", "Bygdgoszcz", 240),
            ("Gdansk", "Warszawa", 300),
            ("Bialystok", "Warszawa", 180), 
            ("Bygdgoszcz", "Warszawa", 230)
        ]
        self.graph.add_nodes_from(nodes)
        self.graph.add_weighted_edges_from(edges)

    # Method for calculating the betweenness centrality with weights
    def betweenness_centrality(self):
        return nx.betweenness_centrality(self.graph, weight='weight')

    # Method for calculating the closeness centrality with weights
    def closeness_centrality(self):
        return nx.closeness_centrality(self.graph, distance='weight')

    def degree_centrality(self):
        return nx.degree_centrality(self.graph)



