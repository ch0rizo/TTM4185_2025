from .graph import Graph, nx, plt

class TrafficSystem(Graph):
    """
    A class representing a traffic communication network with vehicles, emergency services,
    cellular nodes, and a Traffic Management Center (TMC).
    
    The network is structured to simulate real-world traffic systems, allowing users to analyze and
    improve redundancy.
    """
    def __init__(self, vehicle_count=8, emergency_count=2, cellular_count=2, tmc_count=1, **attr):
        super().__init__(**attr)
        self.vehicle_count = vehicle_count
        self.emergency_count = emergency_count
        self.cellular_count = cellular_count
        self.tmc_count = tmc_count
        
        vehicle_range = [0, vehicle_count]
        emergency_range = [vehicle_range[1], vehicle_range[1] + emergency_count]
        cellular_range = [emergency_range[1], emergency_range[1] + cellular_count]
        tmc_range = [cellular_range[1], cellular_range[1] + tmc_count]
        
        G = nx.Graph()
        self._initialize_nodes(G, vehicle_range, emergency_range, cellular_range, tmc_range)
        self._initialize_edges(G, vehicle_range, emergency_range, cellular_range, tmc_range)
        
        self._relabel_nodes(G, vehicle_range, emergency_range, cellular_range, tmc_range)
        self.add_nodes_from(G.nodes(data=True))
        self.add_edges_from(G.edges)
    
    def _initialize_nodes(self, G, vehicle_range, emergency_range, cellular_range, tmc_range):
        """Adds nodes to the graph for different types of entities."""
        for i in range(vehicle_range[1]):
            G.add_node(i)
        for i in range(emergency_range[0], emergency_range[1]):
            G.add_node(i)
        for i in range(cellular_range[0], cellular_range[1]):
            G.add_node(i)
        for i in range(tmc_range[0], tmc_range[1]):
            G.add_node(i)
    
    def _initialize_edges(self, G, vehicle_range, emergency_range, cellular_range, tmc_range):
        """Establishes connections between nodes to form the traffic network."""
        # Connect vehicles to cellular
        for i in range(*vehicle_range):
            for j in range(*cellular_range):
                G.add_edge(i, j)
        
        # Connect emergency vehicles to vehicles and cellular
        for i in range(*emergency_range):
            for j in range(*vehicle_range):
                G.add_edge(i, j)
            for j in range(*cellular_range):
                G.add_edge(i, j)
        
        # Connect vehicles in a chain
        for i in range(vehicle_range[1] - 1):
            G.add_edge(i, i + 1)
        
        # Connect TMC to cellular with limited connections
        tmc_max_connections = 2
        for i in range(*tmc_range):
            connections = 0
            for j in range(*cellular_range):
                if connections >= tmc_max_connections:
                    break
                G.add_edge(i, j)
                connections += 1
    
    def _relabel_nodes(self, G, vehicle_range, emergency_range, cellular_range, tmc_range):
        """Assigns readable labels to nodes based on their type."""
        def make_mapping(prefix, range_index):
            return {i: f"{prefix}{i - range_index[0]}" for i in range(range_index[0], range_index[1])}
        
        mapping = {}
        mapping.update(make_mapping("vehicle", vehicle_range))
        mapping.update(make_mapping("emergency", emergency_range))
        mapping.update(make_mapping("cellular", cellular_range))
        mapping.update(make_mapping("tmc", tmc_range))
        
        nx.relabel_nodes(G, mapping, copy=False)
    
    def _color_nodes(self):
        """Assigns colors to different node types for visualization."""
        color_map = []
        for node in self.nodes:
            if "vehicle" in node:
                color_map.append("#4D6AFF")  # Blue for vehicles
            elif "emergency" in node:
                color_map.append("#FFD700")  # Gold for emergency services
            elif "cellular" in node:
                color_map.append("#AF1144")  # Red for cellular network
            elif "tmc" in node:
                color_map.append('#60AE3E')  # Green for Traffic Management Center
            else:
                color_map.append("#808080")  # Gray for unknown nodes
        return color_map
    
    def draw(self, node_color=None, edge_color="k", node_size=300):
        """Visualizes the network using a force-directed layout."""
        node_color = node_color if node_color else self._color_nodes()
        plt.figure(figsize=(10, 10))
        nx.draw_kamada_kawai(self, with_labels=True, edge_color=edge_color, node_color=node_color, node_size=node_size)
        plt.title("Traffic System Network")
        plt.show()
