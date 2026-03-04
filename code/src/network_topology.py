"""
network_topology.py
===================
Creates the 24-node network topology from the base paper.

This module defines:
- Network structure (4 LANs)
- Node types (hosts, routers, switches)
- Connections between nodes
- IP address assignments
"""

import networkx as nx
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple
import json

class NetworkTopology:
    """
    Represents the network topology for DDoS attack simulation.
    
    Based on Figure 5 from the paper:
    - 24 nodes total
    - 4 Local Area Networks (LANs)
    - Each LAN has 3 hosts, 1 switch, 1 router
    - Routers interconnected through the Internet backbone
    """
    
    def __init__(self):
        """Initialize the network graph and node properties."""
        self.graph = nx.DiGraph()  # Directed graph for routing
        self.nodes = {}  # Node properties
        self.attack_sources = []  # List of attack source nodes
        self.victim = None  # Victim node
        
    def create_topology(self) -> nx.DiGraph:
        """
        Create the 24-node network topology.
        
        Returns:
            nx.DiGraph: The complete network graph
        """
        print("Creating network topology...")
        
        # Create LANs
        self._create_lan1()
        self._create_lan2()  # Contains victim
        self._create_lan3()
        self._create_lan4()
        
        # Interconnect routers (Internet backbone)
        self._connect_routers()
        
        # Set attack sources and victim
        self._configure_attack_scenario()
        
        print(f"Network created: {self.graph.number_of_nodes()} nodes, "
              f"{self.graph.number_of_edges()} edges")
        
        return self.graph
    
    def _create_lan1(self):
        """Create LAN 1 (contains attack sources)."""
        # Hosts
        self._add_node('host1', 'host', '192.170.1.1', lan=1)
        self._add_node('host2', 'host', '192.170.1.2', lan=1)
        self._add_node('host3', 'host', '192.170.1.3', lan=1)
        
        # Switch
        self._add_node('switch1', 'switch', '192.170.1.254', lan=1)
        
        # Router
        self._add_node('router1', 'router', '192.170.1.1', lan=1)
        
        # Connect hosts to switch (bidirectional)
        self._add_edge('host1', 'switch1', capacity=100)
        self._add_edge('switch1', 'host1', capacity=100)
        self._add_edge('host2', 'switch1', capacity=100)
        self._add_edge('switch1', 'host2', capacity=100)
        self._add_edge('host3', 'switch1', capacity=100)
        self._add_edge('switch1', 'host3', capacity=100)
        
        # Connect switch to router (bidirectional)
        self._add_edge('switch1', 'router1', capacity=1000)
        self._add_edge('router1', 'switch1', capacity=1000)
        
    def _create_lan2(self):
        """Create LAN 2 (contains victim)."""
        # Hosts (host4 is the victim)
        self._add_node('host4', 'host', '192.171.1.1', lan=2)  # VICTIM
        self._add_node('host5', 'host', '192.171.1.2', lan=2)
        self._add_node('host6', 'host', '192.171.1.3', lan=2)
        
        # Switch
        self._add_node('switch2', 'switch', '192.171.1.254', lan=2)
        
        # Router
        self._add_node('router2', 'router', '192.171.1.1', lan=2)
        
        # Connections (bidirectional)
        self._add_edge('host4', 'switch2', capacity=100)
        self._add_edge('switch2', 'host4', capacity=100)
        self._add_edge('host5', 'switch2', capacity=100)
        self._add_edge('switch2', 'host5', capacity=100)
        self._add_edge('host6', 'switch2', capacity=100)
        self._add_edge('switch2', 'host6', capacity=100)
        self._add_edge('switch2', 'router2', capacity=1000)
        self._add_edge('router2', 'switch2', capacity=1000)
        
    def _create_lan3(self):
        """Create LAN 3 (contains attack sources)."""
        # Hosts
        self._add_node('host7', 'host', '192.172.1.1', lan=3)
        self._add_node('host8', 'host', '192.172.1.2', lan=3)
        self._add_node('host9', 'host', '192.172.1.3', lan=3)
        
        # Switch
        self._add_node('switch3', 'switch', '192.172.1.254', lan=3)
        
        # Router
        self._add_node('router3', 'router', '192.172.1.1', lan=3)
        
        # Connections (bidirectional)
        self._add_edge('host7', 'switch3', capacity=100)
        self._add_edge('switch3', 'host7', capacity=100)
        self._add_edge('host8', 'switch3', capacity=100)
        self._add_edge('switch3', 'host8', capacity=100)
        self._add_edge('host9', 'switch3', capacity=100)
        self._add_edge('switch3', 'host9', capacity=100)
        self._add_edge('switch3', 'router3', capacity=1000)
        self._add_edge('router3', 'switch3', capacity=1000)
        
    def _create_lan4(self):
        """Create LAN 4 (contains attack sources)."""
        # Hosts
        self._add_node('host10', 'host', '192.173.1.1', lan=4)
        self._add_node('host11', 'host', '192.173.1.2', lan=4)
        self._add_node('host12', 'host', '192.173.1.3', lan=4)
        
        # Switch
        self._add_node('switch4', 'switch', '192.173.1.254', lan=4)
        
        # Router
        self._add_node('router4', 'router', '192.173.1.1', lan=4)
        
        # Connections (bidirectional)
        self._add_edge('host10', 'switch4', capacity=100)
        self._add_edge('switch4', 'host10', capacity=100)
        self._add_edge('host11', 'switch4', capacity=100)
        self._add_edge('switch4', 'host11', capacity=100)
        self._add_edge('host12', 'switch4', capacity=100)
        self._add_edge('switch4', 'host12', capacity=100)
        self._add_edge('switch4', 'router4', capacity=1000)
        self._add_edge('router4', 'switch4', capacity=1000)
        
    def _connect_routers(self):
        """
        Connect routers to form the Internet backbone.
        Based on Figure 5 topology from the paper.
        """
        # Add core routers
        self._add_node('router5', 'router', '10.0.5.1', lan=0)
        self._add_node('router6', 'router', '10.0.6.1', lan=0)
        self._add_node('router7', 'router', '10.0.7.1', lan=0)
        self._add_node('router8', 'router', '10.0.8.1', lan=0)
        
        # Connect routers (backbone connections)
        # From paper's Figure 5 topology
        backbone_connections = [
            ('router1', 'router5'),
            ('router5', 'router8'),
            ('router8', 'router2'),
            ('router3', 'router6'),
            ('router6', 'router8'),
            ('router4', 'router7'),
            ('router7', 'router8'),
        ]
        
        for src, dst in backbone_connections:
            self._add_edge(src, dst, capacity=10000)  # High capacity backbone
            self._add_edge(dst, src, capacity=10000)  # Bidirectional
            
    def _configure_attack_scenario(self):
        """Set up the attack scenario from the paper."""
        # Attack sources (from paper)
        self.attack_sources = ['host1', 'host2', 'host3', 
                               'host7', 'host8', 'host9',
                               'host10', 'host11', 'host12']
        
        # Victim
        self.victim = 'host4'
        
        # Mark nodes
        for node in self.attack_sources:
            self.nodes[node]['is_attacker'] = True
            
        self.nodes[self.victim]['is_victim'] = True
        
    def _add_node(self, name: str, node_type: str, ip: str, lan: int):
        """Add a node to the network."""
        self.graph.add_node(name)
        self.nodes[name] = {
            'type': node_type,
            'ip': ip,
            'lan': lan,
            'is_attacker': False,
            'is_victim': False
        }
        
    def _add_edge(self, src: str, dst: str, capacity: int):
        """Add a directed edge between two nodes."""
        self.graph.add_edge(src, dst, capacity=capacity, packets=0)
        
    def get_node_info(self, node: str) -> Dict:
        """Get information about a specific node."""
        return self.nodes.get(node, {})
    
    def get_neighbors(self, node: str) -> List[str]:
        """Get all neighbors of a node."""
        return list(self.graph.neighbors(node))
    
    def get_predecessors(self, node: str) -> List[str]:
        """Get all nodes that can send packets TO this node."""
        return list(self.graph.predecessors(node))
    
    def visualize(self, save_path: str = None):
        """
        Visualize the network topology.
        
        Args:
            save_path: Path to save the figure (optional)
        """
        plt.figure(figsize=(16, 12))
        
        # Position nodes by LAN
        pos = self._calculate_layout()
        
        # Color nodes by type
        node_colors = []
        for node in self.graph.nodes():
            info = self.nodes[node]
            if info['is_attacker']:
                node_colors.append('red')
            elif info['is_victim']:
                node_colors.append('gold')
            elif info['type'] == 'router':
                node_colors.append('lightblue')
            elif info['type'] == 'switch':
                node_colors.append('lightgreen')
            else:
                node_colors.append('lightgray')
        
        # Draw
        nx.draw(self.graph, pos, 
                node_color=node_colors,
                node_size=1500,
                font_size=10,
                font_weight='bold',
                with_labels=True,
                arrows=True,
                arrowsize=15,
                edge_color='gray',
                alpha=0.8)
        
        plt.title("Network Topology (24 nodes)\nRed=Attackers, Gold=Victim, Blue=Routers, Green=Switches",
                  fontsize=14, fontweight='bold')
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Topology saved to {save_path}")
        
        plt.show()
        
    def _calculate_layout(self) -> Dict[str, Tuple[float, float]]:
        """Calculate positions for visualization."""
        pos = {}
        
        # LAN 1 (top left)
        pos['host1'] = (0, 3)
        pos['host2'] = (0, 2)
        pos['host3'] = (0, 1)
        pos['switch1'] = (1, 2)
        pos['router1'] = (2, 2)
        
        # LAN 2 (top right) - Contains victim
        pos['host4'] = (8, 3)
        pos['host5'] = (8, 2)
        pos['host6'] = (8, 1)
        pos['switch2'] = (7, 2)
        pos['router2'] = (6, 2)
        
        # LAN 3 (bottom left)
        pos['host7'] = (0, -1)
        pos['host8'] = (0, -2)
        pos['host9'] = (0, -3)
        pos['switch3'] = (1, -2)
        pos['router3'] = (2, -2)
        
        # LAN 4 (bottom right)
        pos['host10'] = (8, -1)
        pos['host11'] = (8, -2)
        pos['host12'] = (8, -3)
        pos['switch4'] = (7, -2)
        pos['router4'] = (6, -2)
        
        # Core routers (center)
        pos['router5'] = (3, 1)
        pos['router6'] = (3, -1)
        pos['router7'] = (5, -1)
        pos['router8'] = (5, 1)
        
        return pos
    
    def save_topology(self, filepath: str):
        """Save topology configuration to JSON."""
        config = {
            'nodes': self.nodes,
            'edges': [
                {
                    'src': u,
                    'dst': v,
                    'capacity': self.graph[u][v]['capacity']
                }
                for u, v in self.graph.edges()
            ],
            'attack_sources': self.attack_sources,
            'victim': self.victim
        }
        
        with open(filepath, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"Topology saved to {filepath}")


# Example usage
if __name__ == "__main__":
    import os
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Create output directories
    os.makedirs(os.path.join(PROJECT_ROOT, 'results', 'figures'), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_ROOT, 'data'), exist_ok=True)
    
    # Create network
    network = NetworkTopology()
    network.create_topology()
    
    # Visualize
    network.visualize(save_path=os.path.join(PROJECT_ROOT, 'results', 'figures', 'network_topology.png'))
    
    # Save configuration
    network.save_topology(os.path.join(PROJECT_ROOT, 'data', 'network_config.json'))
    
    # Print statistics
    print(f"\nNetwork Statistics:")
    print(f"  Total nodes: {network.graph.number_of_nodes()}")
    print(f"  Total edges: {network.graph.number_of_edges()}")
    print(f"  Attack sources: {len(network.attack_sources)}")
    print(f"  Victim: {network.victim}")