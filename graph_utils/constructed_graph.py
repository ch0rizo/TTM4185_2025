from .graph import Graph, nx, plt, copy

class ConstructedGraph(Graph):
    def __init__(self, expanded=False, **attr):
        super().__init__(**attr)
        grid_size = 3 
        G = nx.grid_2d_graph(grid_size, grid_size)
        F = nx.cycle_graph(6)#endret fra 5

        def create_mapping(grid_size):
            mapping = {(0, 0): "a0", (0, 2): "b0", (2, 0): "c0", (1, 2): "d0"}#endret fra (1,2) på c0
            for i in range(grid_size):
                for j in range(grid_size):
                    if not (i, j) in mapping:
                        mapping[(i, j)] = "core" + str(i * 3 + j)
            return mapping

        mapping = create_mapping(grid_size)
        G = nx.relabel_nodes(G, mapping)

        def make_mapping(graph, prefix):
            mapping = {}
            for i, elem in enumerate(graph.nodes):
                mapping[elem] = prefix + str(elem)
            return mapping

        stars = "abcd"
        star_form_list = []
        for letter in stars:
            F_ = nx.relabel_nodes(F, make_mapping(F, letter))
            star_form_list.append(F_)

        access_net_size = 5
        A = nx.star_graph(access_net_size)
        access_net_list = []
        cnt = 0
        for i, letter in enumerate(stars):
            A_ = nx.relabel_nodes(A, make_mapping(A, stars[0] + letter))
            access_net_list.append(A_)

        for i, letter in enumerate(stars):
            A_ = nx.relabel_nodes(A, make_mapping(A, stars[1] + letter))
            access_net_list.append(A_)

        for i, net in enumerate(access_net_list):
            if (i < len(access_net_list) // 2):
                access_net_list[i] = nx.relabel_nodes(net, {list(net.nodes)[1]: list(net.nodes)[2][1:]})
            else:
                access_net_list[i] = nx.relabel_nodes(net, {list(net.nodes)[1]: list(net.nodes)[3][1:]})

        for graph in star_form_list:
            G = nx.compose(G, graph)

        for graph in access_net_list:
            G = nx.compose(G, graph)

        if expanded:
            # adding last part of access nett
            access_sub_net_size = 2
            A_sub = nx.star_graph(access_sub_net_size)
            access_sub_net_list = []
            cnt = 0
            for i, graph in enumerate(access_net_list):
                for j, node in enumerate(list(graph.nodes)[2:]):
                    mapping = make_mapping(A_sub, node)
                    mapping[0] = node
                    A_sub_ = nx.relabel_nodes(A_sub, mapping=mapping)
                    access_sub_net_list.append(A_sub_)

            for graph in access_sub_net_list:
                G = nx.compose(G, graph)

        self.add_nodes_from(G.nodes)
        self.add_edges_from(G.edges)
        
        
        self.add_edge("bb0", "b4")
        self.add_edge("core1", "d0")
        self.add_edge("core3", "b0")
        self.add_edge("d1", "core8")
        self.add_edge("b1", "ab0")#
        self.remove_edge("b0", "d0")
        self.remove_edge("b0", "core1")

    def draw(self, node_color="#1f78b4", edge_color="k", node_size=200, method=None):
        G = copy.deepcopy(self)
        components = list(nx.connected_components(G))

        single_node_components = [c for c in components if len(c) == 1]
        multi_node_components = [c for c in components if len(c) > 1]

        # Plot multi-node components separately
        for i, component in enumerate(multi_node_components):
            subgraph = G.subgraph(component)
            
            if method:
                size = adjust_node_sizes(subgraph, method, node_size)
                size = [s / len(components) for s in size]
            else:
                size = node_size

            plt.figure(figsize=(10, 10))  # Create a new figure for each large component
            nx.draw_kamada_kawai(subgraph, with_labels=True, edge_color=edge_color, 
                                node_color=node_color, node_size=size)
            
            node_count = len(subgraph)
            plt.title(f"Component {i + 1} \n Nodes: {node_count}")
            plt.show()  # Display each plot separately

        # Combine all single-node components into one plot if they exist
        if single_node_components:
            plt.figure(figsize=(10, 10))  # Create a new figure for single-node components
            G_single = nx.Graph()
            
            # Add all single nodes into a new graph
            for component in single_node_components:
                G_single.add_node(next(iter(component)))  # Add the single node
            
            nx.draw_kamada_kawai(G_single, with_labels=True, node_color=node_color, node_size=node_size)
            plt.title(f"Single-Node Components: {len(single_node_components)}")
            plt.show()  # Display all single-node components together
        return G


    
