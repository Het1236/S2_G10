"""
Milestone 4: Probabilistic Attack Simulator with 3% Packet Sampling
Based on Lin et al. (2019) - PSO-Based IP Traceback

Key Changes from M3:
- Implements S ~ Bernoulli(p=0.03) for each packet
- Expected sampled packets: N ~ Binomial(1800, 0.03), E[N] = 54 ± 7.24
- Introduces randomness for realistic simulation
"""

import networkx as nx
import numpy as np
import random
import json
import os
import sys
from dataclasses import dataclass
from typing import List, Dict, Tuple
from collections import defaultdict

# Fix Windows terminal encoding for Unicode characters
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

@dataclass
class Packet:
    """Represents a network packet with sampling probability"""
    packet_id: int
    source: str
    destination: str
    path: List[str]
    timestamp: float
    sampled: bool  # NEW: Whether this packet was sampled

class ProbabilisticAttackSimulator:
    """
    Simulates DDoS attack with probabilistic packet sampling (SPIE mechanism)
    
    Parameters from paper:
    - Sampling probability p = 0.03 (3%)
    - Total packets: 1800
    - Expected sampled: E[N] = 54, σ = 7.24
    """
    
    def __init__(self, network_graph: nx.DiGraph, sampling_probability: float = 0.03):
        """
        Initialize probabilistic attack simulator
        
        Args:
            network_graph: Network topology from M3
            sampling_probability: p value for Bernoulli sampling (default 0.03 from paper)
        """
        self.graph = network_graph
        self.p = sampling_probability  # Sampling probability
        self.packets = []
        self.router_logs = defaultdict(list)  # Only sampled packets
        self.total_packets = 0
        self.sampled_packets = 0
        
        # Random seed for reproducibility (can be changed for different runs)
        np.random.seed(None)  # None = different each run (stochastic)
        random.seed(None)
        
    def simulate_ddos_attack(self, attack_sources: List[str], victim: str, 
                           packets_per_source: int = 200) -> Dict:
        """
        Simulate DDoS attack with probabilistic packet sampling
        
        Args:
            attack_sources: List of attacker node IDs
            victim: Victim node ID
            packets_per_source: Packets each attacker sends (default 200)
            
        Returns:
            Dictionary with attack statistics
        """
        print(f"\n{'='*70}")
        print(f"MILESTONE 4: PROBABILISTIC ATTACK SIMULATION")
        print(f"{'='*70}")
        print(f"Sampling probability (p): {self.p}")
        print(f"Expected sampled packets: E[N] = {len(attack_sources) * packets_per_source * self.p:.1f}")
        print(f"Standard deviation: σ = {np.sqrt(len(attack_sources) * packets_per_source * self.p * (1-self.p)):.2f}")
        print(f"{'='*70}\n")
        
        packet_id = 0
        
        for source in attack_sources:
            print(f"Simulating attack from {source}...")
            
            # Find shortest path (same routing as M3)
            try:
                path = nx.shortest_path(self.graph, source, victim)
            except nx.NetworkXNoPath:
                print(f"  ⚠️  No path from {source} to {victim}")
                continue
            
            # Generate packets from this source
            for i in range(packets_per_source):
                timestamp = i * 0.01  # Stagger packets
                
                # CREATE PACKET
                packet = Packet(
                    packet_id=packet_id,
                    source=source,
                    destination=victim,
                    path=path,
                    timestamp=timestamp,
                    sampled=False  # Will be determined below
                )
                
                # PROBABILISTIC SAMPLING: S ~ Bernoulli(p)
                # Each packet has probability p of being sampled
                if np.random.random() < self.p:
                    packet.sampled = True
                    self.sampled_packets += 1
                    
                    # Log packet at each router on the path
                    for router in path:
                        if router.startswith('router'):
                            self.router_logs[router].append({
                                'packet_id': packet_id,
                                'source': source,
                                'destination': victim,
                                'timestamp': timestamp
                            })
                
                self.packets.append(packet)
                self.total_packets += 1
                packet_id += 1
        
        # Calculate actual sampling statistics
        actual_sampling_rate = self.sampled_packets / self.total_packets if self.total_packets > 0 else 0
        
        print(f"\n{'='*70}")
        print(f"ATTACK SIMULATION COMPLETE")
        print(f"{'='*70}")
        print(f"Total packets generated: {self.total_packets}")
        print(f"Packets sampled: {self.sampled_packets}")
        print(f"Actual sampling rate: {actual_sampling_rate:.4f} (expected {self.p})")
        print(f"{'='*70}\n")
        
        return {
            'total_packets': self.total_packets,
            'sampled_packets': self.sampled_packets,
            'actual_sampling_rate': actual_sampling_rate,
            'expected_samples': self.total_packets * self.p,
            'sampling_variance': self.total_packets * self.p * (1 - self.p)
        }
    
    def get_sampled_packet_count(self, router: str) -> int:
        """Get number of sampled packets at a router"""
        return len(self.router_logs.get(router, []))
    
    def get_all_router_counts(self) -> Dict[str, int]:
        """Get packet counts for all routers (sampled packets only)"""
        return {router: len(packets) for router, packets in self.router_logs.items()}
    
    def save_attack_logs(self, output_dir: str = 'data/attack_logs'):
        """Save attack logs to disk"""
        os.makedirs(output_dir, exist_ok=True)
        
        # Save router logs (sampled packets only)
        for router, packets in self.router_logs.items():
            filepath = os.path.join(output_dir, f'{router}_sampled_log.json')
            with open(filepath, 'w') as f:
                json.dump(packets, f, indent=2)
        
        # Save attack summary
        summary = {
            'total_packets': self.total_packets,
            'sampled_packets': self.sampled_packets,
            'sampling_probability': self.p,
            'router_counts': self.get_all_router_counts()
        }
        
        with open(os.path.join(output_dir, 'attack_summary.json'), 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"✅ Attack logs saved to {output_dir}")
    
    def get_sampling_statistics(self) -> Dict:
        """
        Calculate detailed sampling statistics for validation
        
        Returns:
            Dictionary with sampling metrics
        """
        # Calculate per-source statistics
        source_stats = defaultdict(lambda: {'total': 0, 'sampled': 0})
        
        for packet in self.packets:
            source_stats[packet.source]['total'] += 1
            if packet.sampled:
                source_stats[packet.source]['sampled'] += 1
        
        # Calculate variance
        expected_n = self.total_packets * self.p
        variance = self.total_packets * self.p * (1 - self.p)
        std_dev = np.sqrt(variance)
        
        # 95% Confidence Interval (from M2)
        z_score = 1.96
        ci_lower = expected_n - z_score * std_dev
        ci_upper = expected_n + z_score * std_dev
        
        return {
            'total_packets': self.total_packets,
            'sampled_packets': self.sampled_packets,
            'expected_samples': expected_n,
            'variance': variance,
            'std_dev': std_dev,
            'ci_95': (ci_lower, ci_upper),
            'within_ci': ci_lower <= self.sampled_packets <= ci_upper,
            'per_source': dict(source_stats)
        }


# Example usage
if __name__ == "__main__":
    # This would normally import from M3
    print("Probabilistic Attack Simulator for M4")
    print("Use in main.py pipeline")
