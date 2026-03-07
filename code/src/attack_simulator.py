"""
attack_simulator.py
===================
Simulates DETERMINISTIC DDoS attack traffic.

KEY DIFFERENCE FROM PAPER:
- Paper uses probabilistic sampling (p=0.03, only 3% of packets)
- We use ALL packets (deterministic, no sampling)
- This is our baseline for comparison

Attack Scenario:
- 9 attack sources send packets to victim (host4)
- Total: 1800 packets
- Each router logs EVERY packet (not just 3%)
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple
from dataclasses import dataclass
from datetime import datetime
import networkx as nx

@dataclass
class Packet:
    """Represents a network packet."""
    packet_id: int
    source_ip: str
    dest_ip: str
    source_node: str
    dest_node: str
    timestamp: float
    path: List[str]  # Nodes traversed
    
class DeterministicAttackSimulator:
    """
    Simulates DDoS attack with DETERMINISTIC packet routing.
    
    Key properties:
    - NO randomness
    - ALL packets are logged (not sampled)
    - Fixed routing based on shortest path
    - Same attack always produces same packet logs
    """
    
    def __init__(self, network_topology):
        """
        Initialize the simulator.
        
        Args:
            network_topology: NetworkTopology object
        """
        self.network = network_topology
        self.packets = []  # All packets sent
        self.router_logs = {}  # Packets seen by each router
        self.total_packets = 1800  # From paper
        
        # Initialize router logs
        for node in self.network.graph.nodes():
            if self.network.nodes[node]['type'] == 'router':
                self.router_logs[node] = []
                
    def run_attack(self) -> pd.DataFrame:
        """
        Execute the DDoS attack simulation.
        
        Returns:
            DataFrame with all packet information
        """
        print("\n" + "="*70)
        print("STARTING DETERMINISTIC DDOS ATTACK SIMULATION")
        print("="*70)
        
        # Step 1: Generate attack packets
        print("\n[Step 1/3] Generating attack packets...")
        self._generate_attack_packets()
        
        # Step 2: Route packets through network
        print("[Step 2/3] Routing packets (deterministic shortest paths)...")
        self._route_packets()
        
        # Step 3: Log packets at routers
        print("[Step 3/3] Logging packets at routers (ALL packets, no sampling)...")
        self._log_packets()
        
        print("\n" + "="*70)
        print(f"ATTACK COMPLETE:")
        print(f"  Total packets sent: {len(self.packets)}")
        print(f"  Routers with logs: {len(self.router_logs)}")
        print("="*70 + "\n")
        
        return self._create_packet_dataframe()
    
    def _generate_attack_packets(self):
        """Generate packets from all attack sources."""
        packets_per_source = self.total_packets // len(self.network.attack_sources)
        
        packet_id = 0
        for attacker in self.network.attack_sources:
            attacker_info = self.network.get_node_info(attacker)
            victim_info = self.network.get_node_info(self.network.victim)
            
            for i in range(packets_per_source):
                packet = Packet(
                    packet_id=packet_id,
                    source_ip=attacker_info['ip'],
                    dest_ip=victim_info['ip'],
                    source_node=attacker,
                    dest_node=self.network.victim,
                    timestamp=packet_id * 0.001,  # Simulate time
                    path=[]
                )
                self.packets.append(packet)
                packet_id += 1
                
        print(f"  Generated {len(self.packets)} packets from {len(self.network.attack_sources)} sources")
        
    def _route_packets(self):
        """
        Route packets using DETERMINISTIC shortest path.
        
        Key: This is deterministic - same source/dest always gives same path.
        """
        for packet in self.packets:
            try:
                # Use Dijkstra's algorithm (deterministic shortest path)
                path = nx.shortest_path(
                    self.network.graph,
                    source=packet.source_node,
                    target=packet.dest_node
                )
                packet.path = path
                
            except nx.NetworkXNoPath:
                print(f"Warning: No path from {packet.source_node} to {packet.dest_node}")
                packet.path = []
                
    def _log_packets(self):
        """
        Log packets at each router they traverse.
        
        CRITICAL: We log ALL packets (not 3% sample like in paper).
        This is our deterministic baseline.
        """
        for packet in self.packets:
            for node in packet.path:
                node_info = self.network.get_node_info(node)
                
                # Log at routers only
                if node_info['type'] == 'router':
                    self.router_logs[node].append({
                        'packet_id': packet.packet_id,
                        'source': packet.source_node,
                        'dest': packet.dest_node,
                        'timestamp': packet.timestamp
                    })
                    
                    # Increment packet count on edge (for visualization)
                    if len(packet.path) > packet.path.index(node) + 1:
                        next_node = packet.path[packet.path.index(node) + 1]
                        if self.network.graph.has_edge(node, next_node):
                            self.network.graph[node][next_node]['packets'] += 1
        
        # Print router statistics
        print("\n  Packets logged per router:")
        for router, logs in sorted(self.router_logs.items()):
            print(f"    {router}: {len(logs)} packets")
            
    def _create_packet_dataframe(self) -> pd.DataFrame:
        """Create a DataFrame with all packet information."""
        data = []
        for packet in self.packets:
            data.append({
                'packet_id': packet.packet_id,
                'source': packet.source_node,
                'destination': packet.dest_node,
                'source_ip': packet.source_ip,
                'dest_ip': packet.dest_ip,
                'path': ' -> '.join(packet.path),
                'path_length': len(packet.path),
                'timestamp': packet.timestamp
            })
        
        return pd.DataFrame(data)
    
    def get_router_packet_counts(self) -> Dict[str, int]:
        """Get packet count for each router."""
        return {router: len(logs) for router, logs in self.router_logs.items()}
    
    def save_logs(self, filepath: str):
        """Save packet logs to CSV."""
        df = self._create_packet_dataframe()
        df.to_csv(filepath, index=False)
        print(f"Packet logs saved to {filepath}")
        
    def visualize_attack_traffic(self, save_path: str = None):
        """Visualize packet distribution across routers."""
        import matplotlib.pyplot as plt
        import seaborn as sns
        
        # Get packet counts
        counts = self.get_router_packet_counts()
        
        plt.figure(figsize=(12, 6))
        
        # Bar plot
        routers = list(counts.keys())
        packet_counts = list(counts.values())
        
        sns.barplot(x=routers, y=packet_counts, palette='viridis')
        plt.xlabel('Router', fontsize=12, fontweight='bold')
        plt.ylabel('Number of Packets Logged', fontsize=12, fontweight='bold')
        plt.title('Packet Distribution Across Routers (Deterministic - ALL Packets)',
                  fontsize=14, fontweight='bold')
        plt.xticks(rotation=45)
        plt.grid(axis='y', alpha=0.3)
        
        # Add value labels on bars
        for i, count in enumerate(packet_counts):
            plt.text(i, count + 10, str(count), ha='center', fontweight='bold')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Traffic visualization saved to {save_path}")
            
        plt.show()


# Example usage
if __name__ == "__main__":
    import os
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Create output directories
    os.makedirs(os.path.join(PROJECT_ROOT, 'data', 'attack_logs'), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_ROOT, 'results', 'figures'), exist_ok=True)
    
    from network_topology import NetworkTopology
    
    # Create network
    network = NetworkTopology()
    network.create_topology()
    
    # Run attack simulation
    simulator = DeterministicAttackSimulator(network)
    packet_df = simulator.run_attack()
    
    # Save logs
    simulator.save_logs(os.path.join(PROJECT_ROOT, 'data', 'attack_logs', 'packet_logs.csv'))
    
    # Visualize
    simulator.visualize_attack_traffic(os.path.join(PROJECT_ROOT, 'results', 'figures', 'packet_distribution.png'))
    
    # Print sample packets
    print("\nSample packets:")
    print(packet_df.head(10))