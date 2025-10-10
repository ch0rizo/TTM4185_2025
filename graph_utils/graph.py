import networkx as nx
import random as rd
import copy
import matplotlib.pyplot as plt
import math
import statistics


class Graph(nx.Graph):
    def __init__(self, **attr):
        super().__init__(**attr)
        self.seed = rd.randint(0, 1000) if "seed" not in attr.keys() else attr["seed"]
        self.attackdict = {
            "degree": nx.degree_centrality,
            "closeness": nx.closeness_centrality,
            "betweenness": nx.betweenness_centrality
        }

    def histogram(self) -> list:
        dist = nx.degree_histogram(self)
        y_values = []
        for i, elem in enumerate(dist):
            y_values += [i] * elem + [i - 0.25] * elem
        max_value = len(dist) - 1
        bins = (max_value + 1) * 4
        plt.hist(y_values, range=(0, max_value + 1), bins=bins)
        max_xticks = 15
        tick_size = math.ceil((max_value + 2) / max_xticks)
        plt.xticks(range(0, max_value + tick_size + 1, tick_size))
        plt.xlabel("Node degree")
        plt.ylabel("Antall")
        plt.show()
        return dist

    def degree_centrality(self):
        return nx.degree_centrality(self)

    def closeness_centrality(self):
        return nx.closeness_centrality(self)

    def betweenness_centrality(self):
        return nx.betweenness_centrality(self)

    def draw_degree_centrality(self, avg_size=300):
        sizes = list(self.degree_centrality().values())
        sizes = [i ** 1.5 for i in sizes]
        mean = statistics.mean(sizes)
        sizes = [i * avg_size / mean for i in sizes]
        self.draw(node_size=sizes)

    def draw_closeness_centrality(self, avg_size=300):
        sizes = list(self.closeness_centrality().values())
        sizes = [i ** 2 for i in sizes]
        mean = statistics.mean(sizes)
        sizes = [i * avg_size / mean for i in sizes]
        self.draw(node_size=sizes)

    def draw_betweenness_centrality(self, avg_size=300):
        sizes = list(self.betweenness_centrality().values())
        mean = statistics.mean(sizes)
        sizes = [i * avg_size / mean for i in sizes]
        self.draw(node_size=sizes)

    def get_largest_components_size(self):
        return len(max(nx.connected_components(self), key=len))

    def delete_random_nodes(self, n: int = 1, print_result=True):
        G = copy.deepcopy(self)
        rd.seed(self.seed)
        for i in range(n):
            node = rd.choice([i for i in nx.nodes(G)])
            if print_result:
                print("Removed node", node, "using", "random_fault")
            G.remove_node(node)
        return G

    def delete_nodes_attack(self, n: int = 1, centrality_index: str = "degree", print_result=True):
        #:TODO mekke pause og highlighte grafen så den lyser
        G = copy.deepcopy(self)
        rd.seed(self.seed)
        for i in range(n):
            analysis = self.attackdict[centrality_index](G)
            node = max(analysis, key=lambda key: analysis[key])
            if print_result:
                print("Removed node", node, "using", str(self.attackdict[centrality_index].__name__))
            G.remove_node(node)
        return G

    def get_shortest_path(self, node1, node2):
        path = None
        try:
            path = nx.shortest_path(self, node1, node2)
        except nx.NetworkXNoPath:
            pass
        return path

    def mark_nodes(self, mark_nodes):
        nodes = self.nodes()
        node_color = ["#1f78b4" if node not in mark_nodes else "#b82d2d" for node in nodes]
        self.draw(node_color=node_color)

    def mark_shortest_path(self, node1, node2):
        path = nx.shortest_path(self, node1, node2)
        edges = self.edges()
        marked_edges = [(element, path[i + 1]) for i, element in enumerate(path) if i < len(path) - 1]
        edge_color = [("k" if (u, v) not in marked_edges and (v, u) not in marked_edges else "#b82d2d") for u, v in
                      edges]
        nodes = self.nodes()
        node_color = ["#1f78b4" if node not in path else "#b82d2d" for node in nodes]
        self.draw(edge_color=edge_color, node_color=node_color)

    def draw(self, node_color="#1f78b4", edge_color="k", node_size=300):
        plt.figure(num=None, figsize=(10, 10))
        nx.draw_kamada_kawai(self, with_labels=True, edge_color=edge_color, node_color=node_color, node_size=node_size)

