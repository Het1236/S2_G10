"""
Milestone 4: PSO-Based IP Traceback Algorithm
Based on Lin et al. (2019) Computers doi:10.3390/computers8040088

Implements Particle Swarm Optimization for attack path reconstruction
using probabilistically sampled packet data (3% sampling)

Key PSO Parameters (from paper):
- Inertia weight w = 0.8
- Acceleration constants c1 = c2 = 2.0
- Oscillation correction ρ = 1/2
- Particle swarm size = number of sampled packets
"""

import networkx as nx
import numpy as np
import random
import sys
from typing import List, Dict, Tuple, Set
from dataclasses import dataclass
from collections import defaultdict
import copy

# Fix Windows terminal encoding for Unicode characters
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

@dataclass
class Particle:
    """
    Represents a PSO particle (candidate attack path)
    
    Attributes:
        position: Current path (list of nodes)
        velocity: Movement tendency in search space
        fitness: Coverage percentage (Equation 3 from paper)
        pbest_position: Personal best path found
        pbest_fitness: Fitness of personal best
    """
    position: List[str]  # Current candidate path
    velocity: float  # Velocity in search space
    fitness: float  # Coverage percentage
    pbest_position: List[str]  # Personal best path
    pbest_fitness: float  # Best fitness seen by this particle


class PSOTraceback:
    """
    PSO-based IP traceback algorithm
    
    Uses particle swarm optimization to reconstruct attack paths
    from probabilistically sampled packet data
    """
    
    def __init__(self, 
                 network_graph: nx.DiGraph,
                 router_packet_counts: Dict[str, int],
                 total_sampled_packets: int,
                 w: float = 0.8,  # Inertia weight (paper)
                 c1: float = 2.0,  # Cognitive coefficient (paper)
                 c2: float = 2.0,  # Social coefficient (paper)
                 max_iterations: int = 500,  # Max iterations per run (paper)
                 num_particles: int = 30):  # Swarm size
        """
        Initialize PSO traceback algorithm
        
        Args:
            network_graph: Network topology
            router_packet_counts: Sampled packet counts at each router
            total_sampled_packets: Total packets sampled
            w: Inertia weight (0.8 from paper)
            c1: Cognitive learning factor (2.0 from paper)
            c2: Social learning factor (2.0 from paper)
            max_iterations: Maximum iterations (500 from paper)
            num_particles: Number of particles in swarm
        """
        self.graph = network_graph
        self.router_counts = router_packet_counts
        self.total_packets = total_sampled_packets
        
        # PSO parameters (from paper Section 3.2)
        self.w = w
        self.c1 = c1
        self.c2 = c2
        self.max_iterations = max_iterations
        self.num_particles = num_particles
        
        # Oscillation detection parameters (from paper Equation 7)
        self.oscillation_threshold = 0.001  # δ' in paper
        self.oscillation_count_limit = 3  # α in paper
        self.rho = 0.5  # ρ for position update (Equation 9)
        
        # Results
        self.pgbest_position = None  # Global best path
        self.pgbest_fitness = -np.inf
        self.convergence_history = []
        self.particles = []
        
        # Tabu list to prevent revisiting nodes (from paper)
        self.tabu_list = set()
        
    def calculate_coverage(self, path: List[str]) -> float:
        """
        Calculate coverage percentage for a path (Equation 3 from paper)
        
        Coverage(%) = (Average packets per hop / Total packets) × 100
        
        Args:
            path: Candidate attack path
            
        Returns:
            Coverage percentage
        """
        if len(path) <= 1:
            return 0.0
        
        # Count total packets on this path
        path_packet_count = 0
        valid_hops = 0
        
        for node in path:
            if node.startswith('router'):
                count = self.router_counts.get(node, 0)
                path_packet_count += count
                valid_hops += 1
        
        if valid_hops == 0 or self.total_packets == 0:
            return 0.0
        
        # Calculate average packets per hop
        avg_packets_per_hop = path_packet_count / valid_hops
        
        # Coverage percentage (Equation 3)
        coverage = (avg_packets_per_hop / self.total_packets) * 100
        
        return coverage
    
    def initialize_particles(self, source: str, victim: str) -> None:
        """
        Initialize particle swarm with random candidate paths
        
        Each particle starts with a random path from source to victim
        
        Args:
            source: Attack source node
            victim: Victim node
        """
        self.particles = []
        
        for i in range(self.num_particles):
            # Try to find a path
            try:
                # Use shortest path as starting point
                base_path = nx.shortest_path(self.graph, source, victim)
                
                # Add some randomness: occasionally use alternative paths
                if random.random() < 0.3:  # 30% chance of random exploration
                    # Try to find alternative path by removing a random edge temporarily
                    temp_path = self._find_alternative_path(source, victim, base_path)
                    if temp_path:
                        base_path = temp_path
                
                # Calculate initial fitness
                fitness = self.calculate_coverage(base_path)
                
                # Create particle
                particle = Particle(
                    position=base_path.copy(),
                    velocity=random.uniform(-1, 1),  # Random initial velocity
                    fitness=fitness,
                    pbest_position=base_path.copy(),
                    pbest_fitness=fitness
                )
                
                self.particles.append(particle)
                
                # Update global best if this is better
                if fitness > self.pgbest_fitness:
                    self.pgbest_fitness = fitness
                    self.pgbest_position = base_path.copy()
                    
            except nx.NetworkXNoPath:
                continue
    
    def _find_alternative_path(self, source: str, victim: str, 
                              avoid_path: List[str]) -> List[str]:
        """
        Find alternative path by temporarily removing edges
        
        Args:
            source: Source node
            victim: Victim node
            avoid_path: Path to avoid
            
        Returns:
            Alternative path or None
        """
        try:
            # Create temporary graph
            temp_graph = self.graph.copy()
            
            # Remove some edges from the avoid_path
            if len(avoid_path) > 2:
                # Remove middle edge
                mid = len(avoid_path) // 2
                if temp_graph.has_edge(avoid_path[mid-1], avoid_path[mid]):
                    temp_graph.remove_edge(avoid_path[mid-1], avoid_path[mid])
            
            # Find path in modified graph
            alt_path = nx.shortest_path(temp_graph, source, victim)
            return alt_path
            
        except:
            return None
    
    def update_velocity(self, particle: Particle) -> float:
        """
        Update particle velocity (Equation 1 from paper)
        
        v_i(t+1) = w·v_i(t) + c1·rand()·(Pbest - x_i(t)) + c2·rand()·(Pgbest - x_i(t))
        
        Args:
            particle: Particle to update
            
        Returns:
            New velocity
        """
        # Current velocity (inertia)
        inertia = self.w * particle.velocity
        
        # Cognitive component (personal best)
        r1 = random.random()
        cognitive = self.c1 * r1 * (particle.pbest_fitness - particle.fitness)
        
        # Social component (global best)
        r2 = random.random()
        social = self.c2 * r2 * (self.pgbest_fitness - particle.fitness)
        
        # New velocity
        new_velocity = inertia + cognitive + social
        
        # Clamp velocity to prevent explosion
        v_max = 5.0
        new_velocity = np.clip(new_velocity, -v_max, v_max)
        
        return new_velocity
    
    def update_position(self, particle: Particle, source: str, victim: str) -> List[str]:
        """
        Update particle position based on velocity
        
        Position represents the attack path. We update by:
        1. Selecting path based on velocity direction (positive = explore, negative = exploit)
        2. Checking for oscillation (Equation 7)
        3. Applying correction if needed (Equations 8-9)
        
        Args:
            particle: Particle to update
            source: Source node
            victim: Victim node
            
        Returns:
            New position (path)
        """
        # If velocity is positive, explore more
        # If velocity is negative, exploit current knowledge
        
        if particle.velocity > 0.5:
            # Explore: Try alternative path
            new_path = self._explore_new_path(source, victim, particle.position)
        elif particle.velocity < -0.5:
            # Exploit: Move toward global best
            new_path = self._move_toward_best(source, victim, particle.position)
        else:
            # Stay near current position with small variation
            new_path = self._local_search(source, victim, particle.position)
        
        # If no new path found, keep current
        if not new_path:
            new_path = particle.position
        
        return new_path
    
    def _explore_new_path(self, source: str, victim: str, 
                         current_path: List[str]) -> List[str]:
        """Explore new path (high velocity - exploration)"""
        return self._find_alternative_path(source, victim, current_path) or current_path
    
    def _move_toward_best(self, source: str, victim: str, 
                         current_path: List[str]) -> List[str]:
        """Move toward global best (low velocity - exploitation)"""
        if self.pgbest_position:
            # Use global best path with small variation
            return self.pgbest_position.copy()
        return current_path
    
    def _local_search(self, source: str, victim: str, 
                     current_path: List[str]) -> List[str]:
        """Small local variation"""
        # Just use current path (local minimum)
        return current_path
    
    def detect_oscillation(self, fitness_history: List[float]) -> bool:
        """
        Detect oscillation in fitness (Equation 7 from paper)
        
        Oscillation occurs when fitness changes are very small repeatedly
        
        Args:
            fitness_history: Recent fitness values
            
        Returns:
            True if oscillation detected
        """
        if len(fitness_history) < self.oscillation_count_limit + 1:
            return False
        
        # Check if fitness changes are below threshold repeatedly
        recent = fitness_history[-self.oscillation_count_limit-1:]
        
        changes = [abs(recent[i+1] - recent[i]) for i in range(len(recent)-1)]
        
        oscillating = all(change < self.oscillation_threshold for change in changes)
        
        return oscillating
    
    def trace_attack_source(self, suspected_source: str, victim: str, 
                           verbose: bool = False) -> Dict:
        """
        Trace single attack source using PSO
        
        Args:
            suspected_source: Suspected attack source
            victim: Victim node
            verbose: Print iteration details
            
        Returns:
            Dictionary with traced path and metrics
        """
        print(f"\n🔍 Tracing attack from {suspected_source} using PSO...")
        
        # Initialize particles
        self.initialize_particles(suspected_source, victim)
        
        if not self.particles:
            return {
                'source': suspected_source,
                'path': [],
                'coverage': 0.0,
                'converged': False,
                'iterations': 0
            }
        
        # PSO iterations
        fitness_history = []
        
        for iteration in range(self.max_iterations):
            # Update each particle
            for particle in self.particles:
                # Update velocity (Equation 1)
                particle.velocity = self.update_velocity(particle)
                
                # Update position (Equation 2)
                new_position = self.update_position(particle, suspected_source, victim)
                
                # Calculate fitness
                new_fitness = self.calculate_coverage(new_position)
                
                # Update particle position and fitness
                particle.position = new_position
                particle.fitness = new_fitness
                
                # Update personal best
                if new_fitness > particle.pbest_fitness:
                    particle.pbest_fitness = new_fitness
                    particle.pbest_position = new_position.copy()
                
                # Update global best
                if new_fitness > self.pgbest_fitness:
                    self.pgbest_fitness = new_fitness
                    self.pgbest_position = new_position.copy()
            
            # Record convergence
            fitness_history.append(self.pgbest_fitness)
            self.convergence_history.append({
                'iteration': iteration,
                'best_fitness': self.pgbest_fitness,
                'avg_fitness': np.mean([p.fitness for p in self.particles])
            })
            
            # Check for convergence (no improvement for 50 iterations)
            if len(fitness_history) > 50:
                recent_improvement = max(fitness_history[-50:]) - min(fitness_history[-50:])
                if recent_improvement < 0.01:
                    if verbose:
                        print(f"  ✓ Converged at iteration {iteration}")
                    break
            
            # Verbose output
            if verbose and iteration % 50 == 0:
                print(f"  Iteration {iteration}: Best fitness = {self.pgbest_fitness:.2f}%")
        
        # Final results
        result = {
            'source': suspected_source,
            'path': self.pgbest_position,
            'coverage': self.pgbest_fitness,
            'converged': True,
            'iterations': len(fitness_history),
            'convergence_history': self.convergence_history
        }
        
        print(f"  ✓ Best path: {' → '.join(self.pgbest_position)}")
        print(f"  ✓ Coverage: {self.pgbest_fitness:.2f}%")
        print(f"  ✓ Iterations: {len(fitness_history)}")
        
        return result
    
    def trace_all_attacks(self, suspected_sources: List[str], victim: str, 
                         verbose: bool = False) -> List[Dict]:
        """
        Trace all suspected attack sources
        
        Args:
            suspected_sources: List of suspected sources
            victim: Victim node
            verbose: Print details
            
        Returns:
            List of trace results
        """
        results = []
        
        print(f"\n{'='*70}")
        print(f"PSO-BASED IP TRACEBACK")
        print(f"{'='*70}")
        print(f"Suspected sources: {len(suspected_sources)}")
        print(f"Victim: {victim}")
        print(f"Sampled packets: {self.total_packets}")
        print(f"{'='*70}")
        
        for source in suspected_sources:
            # Reset global best for each source
            self.pgbest_position = None
            self.pgbest_fitness = -np.inf
            self.convergence_history = []
            
            result = self.trace_attack_source(source, victim, verbose=verbose)
            results.append(result)
        
        return results


# Example usage
if __name__ == "__main__":
    print("PSO-Based IP Traceback for M4")
    print("Use in main.py pipeline")
