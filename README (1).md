# PSO-Based IP Traceback for DDoS Attack Detection

[![Course](https://img.shields.io/badge/Course-CSE%20400-blue)](https://www.ahduni.edu.in/)
[![University](https://img.shields.io/badge/University-Ahmedabad%20University-orange)](https://www.ahduni.edu.in/)
[![Subject](https://img.shields.io/badge/Subject-Fundamentals%20of%20Probability%20in%20Computing-green)](https://www.ahduni.edu.in/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **Fundamentals of Probability in Computing (CSE 400) - Course Project**  
> **School of Engineering and Applied Science, Ahmedabad University**

---

## 📋 Table of Contents

- [Project Overview](#-project-overview)
- [Problem Statement](#-problem-statement)
- [Solution Architecture](#-solution-architecture)
- [Probabilistic Framework](#-probabilistic-framework)
- [PSO Algorithm](#-pso-algorithm)
- [Implementation](#-implementation)
- [Experimental Results](#-experimental-results)
- [Project Structure](#-project-structure)
- [Installation & Usage](#-installation--usage)
- [Team & Milestones](#-team--milestones)
- [References](#-references)
- [License](#-license)

---

## 🎯 Project Overview

This project implements a **Particle Swarm Optimization (PSO) based IP Traceback mechanism** to identify the source of **Distributed Denial of Service (DDoS) attacks** in computer networks. The solution addresses the fundamental challenge of tracing attack origins when attackers use spoofed IP addresses and only limited routing information is available.

### Key Highlights

| Aspect | Description |
|--------|-------------|
| **Algorithm** | Modified Particle Swarm Optimization (PSO-IPTBK) |
| **Detection Accuracy** | 98.33% (24-node network), 94.64% (40-node network) |
| **Sampling Rate** | 3% packet marking (SPIE mechanism) |
| **Simulation Platform** | OMNeT++ 5.5.1 with INET 4 Framework |
| **Core Innovation** | Oscillation detection to prevent premature convergence |

### Research Foundation

This implementation is based on the research paper:  
> **"Implementation of a PSO-Based Security Defense Mechanism for Tracing the Sources of DDoS Attacks"**  
> by Hsiao-Chung Lin, Ping Wang, and Wen-Hui Lin  
> Published in *Computers* (MDPI), 2019

---

## 🔍 Problem Statement

### The DDoS Challenge

**Distributed Denial of Service (DDoS)** attacks represent one of the most severe cybersecurity threats, where:

- Multiple compromised systems (zombies) flood a target server
- Attackers use **IP spoofing** to hide their true identity
- Legitimate users are denied access to services
- Traditional defense mechanisms (firewalls, NIDS) can only block traffic, not trace sources

### The IP Traceback Problem

**Given:**
- A victim server receiving massive attack traffic
- Limited routing information (only ~3% of packets carry path data)
- A network topology with multiple possible routes
- Computational constraints (time and packet count)

**Find:**
- The most probable attack route from attacker to victim
- The actual source(s) of the DDoS attack

### Why This is a Probabilistic Problem

| Source of Uncertainty | Description |
|----------------------|-------------|
| **Packet Marking** | Only 3% of packets are marked (Bernoulli trial with p=0.03) |
| **Multiple Routes** | Many feasible paths exist in the network topology |
| **Spoofed IPs** | Attackers inject false source addresses |
| **Dynamic Routing** | Network paths may change over time |

---

## 🏗️ Solution Architecture

### System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         PSO-IPTBK SYSTEM ARCHITECTURE                        │
└─────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────┐         ┌──────────────┐         ┌──────────────┐
    │   DDoS       │         │   Network    │         │   NIDS       │
    │   Attackers  │────────▶│   Routers    │────────▶│   Detection  │
    │   (Spoofed)  │         │   (SPIE)     │         │   System     │
    └──────────────┘         └──────────────┘         └──────┬───────┘
                                                              │
                                                              ▼
    ┌──────────────────────────────────────────────────────────────────┐
    │                    DATA COLLECTION PHASE                          │
    │  • 3% packet sampling (Bernoulli p=0.03)                         │
    │  • 32-bit packet digests stored                                  │
    │  • Partial path information extracted                            │
    └──────────────────────────────┬───────────────────────────────────┘
                                   │
                                   ▼
    ┌──────────────────────────────────────────────────────────────────┐
    │                    PSO-IPTBK ALGORITHM                            │
    │                                                                   │
    │  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐         │
    │  │ Initialize  │───▶│   Update    │───▶│  Evaluate   │         │
    │  │ Particles   │    │  Velocity   │    │   Fitness   │         │
    │  └─────────────┘    └─────────────┘    └──────┬──────┘         │
    │         ▲                                       │                │
    │         │            ┌─────────────┐            │                │
    │         └────────────│   Check     │◀───────────┘                │
    │                      │ Convergence │                               │
    │                      └──────┬──────┘                               │
    │                             │                                      │
    │                             ▼                                      │
    │                      ┌─────────────┐                               │
    │                      │   Output    │                               │
    │                      │Attack Route │                               │
    │                      └─────────────┘                               │
    └──────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
    ┌──────────────────────────────────────────────────────────────────┐
    │                      OUTPUT & METRICS                             │
    │  • Identified attack path: R1 → R2 → ... → Attacker              │
    │  • Coverage percentage: 98.33% (24 nodes)                        │
    │  • False rate: 1.67% (24 nodes)                                  │
    └──────────────────────────────────────────────────────────────────┘
```

### Core Components

#### 1. SPIE (Source Path Isolation Engine)
- **Function**: Collects partial routing information
- **Mechanism**: Routers store 32-bit packet digests
- **Sampling**: Only 3% of packets marked (reduces overhead)
- **Output**: Partial path data for reconstruction

#### 2. NIDS (Network Intrusion Detection System)
- **Function**: Detects attack patterns and triggers traceback
- **Process**: Recursive lookup through collected digests
- **Integration**: Feeds data to PSO algorithm

#### 3. PSO-IPTBK Algorithm
- **Function**: Probabilistic search for optimal attack route
- **Approach**: Swarm intelligence with oscillation detection
- **Output**: Most probable attack path

---

## 🎲 Probabilistic Framework

### Sources of Uncertainty

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         UNCERTAINTY PROPAGATION                              │
└─────────────────────────────────────────────────────────────────────────────┘

    Network Topology                    Packet Marking                    Algorithm
         │                                   │                             │
         ▼                                   ▼                             ▼
┌─────────────────┐              ┌─────────────────┐              ┌─────────────────┐
│ • Multiple paths│              │ • Bernoulli     │              │ • rand() in     │
│   between nodes │              │   p = 0.03      │              │   velocity      │
│ • Dynamic       │              │ • Independent   │              │ • Random init   │
│   routing       │              │   events        │              │ • Exploration   │
│ • Unknown       │              │ • Missing info  │              │   vs Exploit    │
│   topology      │              │                 │              │                 │
└────────┬────────┘              └────────┬────────┘              └────────┬────────┘
         │                                │                                │
         └────────────────┬───────────────┴────────────────┬───────────────┘
                          │                                │
                          ▼                                ▼
              ┌─────────────────────┐          ┌─────────────────────┐
              │ Partial Information │          │ Probabilistic Search │
              │ Collected           │          │ Space               │
              └──────────┬──────────┘          └──────────┬──────────┘
                         │                                │
                         └──────────────┬─────────────────┘
                                        │
                                        ▼
                          ┌─────────────────────┐
                          │ Most Probable Route │
                          │ Identified          │
                          └─────────────────────┘
```

### Random Variables

#### Primary Random Variables

| Variable | Symbol | Domain | Description |
|----------|--------|--------|-------------|
| **Particle Position** | $x_i(t)$ | $\mathbb{R}^D$ | Position of particle $i$ at time $t$ in D-dimensional space |
| **Particle Velocity** | $v_i(t)$ | $[-v_{max}, v_{max}]^D$ | Velocity of particle $i$ at time $t$ |
| **Personal Best** | $P_{best}$ | $\mathbb{R}^D$ | Best position found by particle $i$ so far |
| **Global Best** | $P_{gbest}$ | $\mathbb{R}^D$ | Best position found by any particle in swarm |
| **Random Number** | $\text{rand}()$ | $[0, 1]$ | Uniform random number for exploration |

#### Network-Related Random Variables

| Variable | Symbol | Description |
|----------|--------|-------------|
| **Network Nodes** | $X = \{x_{i1}, ..., x_{iD}\}$ | Set of all routers/nodes in topology |
| **Source Nodes** | $x_s$ | Attack source nodes (randomly distributed) |
| **Sink Nodes** | $x_d$ | Victim nodes |
| **Edges** | $e_i$ | Connections between nodes |
| **Marking Probability** | $p$ | Probability a router marks a packet (0.03) |

#### PSO Parameter Random Variables

| Variable | Symbol | Typical Value | Description |
|----------|--------|---------------|-------------|
| **Inertia Weight** | $w_i$ | 0.8 | Controls momentum vs. exploration |
| **Cognitive Coefficient** | $c_1$ | 2.0 | Weight for personal experience |
| **Social Coefficient** | $c_2$ | 2.0 | Weight for swarm experience |
| **Acceleration Ratio** | $\rho$ | 0.5 | Used when oscillation detected |

### Probabilistic Relationships

#### Independence Assumptions

1. **Packet Markings**: Events are independent across routers
   ```
   P(mark at R_i AND mark at R_j) = P(mark at R_i) × P(mark at R_j)
   ```

2. **Random Components**: `rand()` calls are independent
   ```
   rand_i(t) ⟂ rand_j(t') for all i ≠ j or t ≠ t'
   ```

3. **Attack Sources**: Distributed independently in network

#### Dependence Relationships (Markov Chain)

1. **Velocity depends on previous velocity**:
   ```
   v_i(t) depends on v_i(t-1)
   ```

2. **Position depends on previous position**:
   ```
   x_i(t) depends on x_i(t-1)
   ```

3. **Personal best depends on history**:
   ```
   P_best(t) = argmax{F(x_i(τ)) : τ ≤ t}
   ```

#### Conditional Probability

The probability that route $R_j$ is the true attack path given collected data:

```
P(R_j is attack path | collected packets) ∝ F(R_j)
```

Where $F(R_j)$ is the fitness of route $R_j$.

---

## 🧬 PSO Algorithm

### Core Equations

#### 1. Velocity Update Equation

```
v_i(t+1) = w_i · v_i(t) 
         + c_1 · rand() · (P_best - x_i(t)) 
         + c_2 · rand() · (P_gbest - x_i(t))
```

**Components:**

| Term | Name | Purpose |
|------|------|---------|
| $w_i \cdot v_i(t)$ | **Inertia** | Maintains momentum in current direction |
| $c_1 \cdot \text{rand}() \cdot (P_{best} - x_i(t))$ | **Cognitive** | Pulls toward particle's best experience |
| $c_2 \cdot \text{rand}() \cdot (P_{gbest} - x_i(t))$ | **Social** | Pulls toward swarm's best experience |

#### 2. Position Update Equation

```
x_i(t+1) = x_i(t) + v_i(t+1)
```

#### 3. Fitness Function

```
F = ||(x_i ⊆ R_j(x_i))||

If ||D(x_i, P_gbest)_{t+1} < D(x_i, P_gbest)_t|| then F = F + 1
```

Where distance is Euclidean:
```
D(x_i, P_gbest) = √[Σ(x_i(i,j) - P_gbest(i,j))²]
```

#### 4. Coverage Percentage Metric

```
Coverage % = (Average packets on attack path / Total routing packets) × 100%
```

#### 5. Oscillation Detection

```
If (||D(x_i, P_gbest)_{t+1} < D(x_i, P_gbest)_t|| < δ') repeats α times:
    Detect oscillation → Apply revised update
```

#### 6. Revised Position Update (for oscillation)

```
x_i(t+1) = x_i(t) + ρ[(x_max - x_min)]

where: ρ = (x_i(t) - x_min) / (x_max - x_min)
```

### Algorithm Flowchart

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          PSO-IPTBK ALGORITHM                                 │
└─────────────────────────────────────────────────────────────────────────────┘

    ┌─────────────────┐
    │     START       │
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │  Initialize     │
    │  • m particles  │
    │  • Random x_i   │
    │  • Random v_i   │
    │  • P_best = x_i │
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐     ┌─────────────────┐
    │  For each       │────▶│  Update         │
    │  iteration t    │     │  velocity       │
    └────────┬────────┘     │  v_i(t+1)       │
             │              └────────┬────────┘
             │                       │
             │                       ▼
             │              ┌─────────────────┐
             │              │  Update         │
             │              │  position       │
             │              │  x_i(t+1)       │
             │              └────────┬────────┘
             │                       │
             │                       ▼
             │              ┌─────────────────┐
             │              │  Evaluate       │
             │              │  fitness F      │
             │              └────────┬────────┘
             │                       │
             │                       ▼
             │              ┌─────────────────┐
             │              │  Update P_best  │
             │              │  and P_gbest    │
             │              └────────┬────────┘
             │                       │
             │                       ▼
             │              ┌─────────────────┐
             │              │  Check          │
             │              │  oscillation?   │
             │              └────────┬────────┘
             │                       │
             │              ┌────────┴────────┐
             │              │                 │
             │             YES               NO
             │              │                 │
             │              ▼                 │
             │     ┌─────────────────┐        │
             │     │  Apply revised  │        │
             │     │  position update│        │
             │     │  (escape local  │        │
             │     │   optimum)      │        │
             │     └────────┬────────┘        │
             │              │                 │
             │              └────────┬────────┘
             │                       │
             │                       ▼
             │              ┌─────────────────┐
             │              │  Check          │
             │              │  convergence?   │
             │              │  (max iter or   │
             │              │   stable)       │
             │              └────────┬────────┘
             │                       │
             │              ┌────────┴────────┐
             │              │                 │
             │             YES               NO
             │              │                 │
             │              ▼                 │
             │     ┌─────────────────┐        │
             │     │   Output        │        │
             │     │   Attack Route  │        │
             │     └────────┬────────┘        │
             │              │                 │
             │              ▼                 │
             │     ┌─────────────────┐        │
             │     │   Calculate     │        │
             │     │   metrics       │        │
             │     └────────┬────────┘        │
             │              │                 │
             │              ▼                 │
             │     ┌─────────────────┐        │
             └────▶│   Next          │◀───────┘
                   │   iteration     │
                   └─────────────────┘
                          │
                          ▼
                   ┌─────────────────┐
                   │      END        │
                   └─────────────────┘
```

### Parameter Settings

| Parameter | Symbol | Value | Description |
|-----------|--------|-------|-------------|
| Particle count | $m$ | 1800 | Equal to attack packets |
| Generations | $G$ | 10 | Number of generations |
| Iterations | $I$ | 500 | Iterations per generation |
| Inertia weight | $w_i$ | 0.8 | Initial weight |
| Cognitive coefficient | $c_1$ | 2.0 | Personal experience weight |
| Social coefficient | $c_2$ | 2.0 | Swarm experience weight |
| Acceleration ratio | $\rho$ | 0.5 | Oscillation escape factor |

---

## 💻 Implementation

### Project Structure

```
pso-iptbk-ddos/
├── README.md                          # This file
├── LICENSE                            # MIT License
├── .gitignore                         # Git ignore rules
│
├── docs/                              # Documentation
│   ├── concept_map/                   # Concept map files
│   │   ├── PSO_IPTBK_ConceptMap.drawio
│   │   └── concept_map.png
│   ├── scribes/                       # Scribe submissions
│   │   ├── milestone_1.md
│   │   ├── milestone_2.md
│   │   └── ...
│   └── video/                         # Video presentations
│       └── README.md
│
├── src/                               # Source code
│   ├── pso/                           # PSO algorithm
│   │   ├── __init__.py
│   │   ├── particle.py                # Particle class
│   │   ├── swarm.py                   # Swarm management
│   │   ├── fitness.py                 # Fitness functions
│   │   └── oscillation.py             # Oscillation detection
│   │
│   ├── network/                       # Network simulation
│   │   ├── __init__.py
│   │   ├── topology.py                # Network topology
│   │   ├── router.py                  # Router simulation
│   │   └── spie.py                    # SPIE mechanism
│   │
│   ├── simulation/                    # OMNeT++ integration
│   │   ├── __init__.py
│   │   └── omnetpp_integration.py
│   │
│   └── utils/                         # Utilities
│       ├── __init__.py
│       ├── metrics.py                 # Performance metrics
│       └── visualization.py           # Plotting functions
│
├── experiments/                       # Experimental results
│   ├── case_24_nodes/                 # 24-node network results
│   │   ├── config.ini
│   │   ├── results.csv
│   │   └── plots/
│   │
│   └── case_40_nodes/                 # 40-node network results
│       ├── config.ini
│       ├── results.csv
│       └── plots/
│
├── tests/                             # Unit tests
│   ├── test_particle.py
│   ├── test_swarm.py
│   └── test_fitness.py
│
└── data/                              # Sample data
    ├── network_topologies/
    └── packet_samples/
```

### Core Implementation

#### Particle Class

```python
"""
Particle class for PSO-IPTBK algorithm.
Represents a potential solution (attack route) in the search space.
"""

import numpy as np
from typing import Tuple, Optional

class Particle:
    """
    A particle in the PSO swarm.
    
    Attributes:
        position (np.ndarray): Current position x_i(t) in R^D
        velocity (np.ndarray): Current velocity v_i(t)
        pbest (np.ndarray): Personal best position found
        pbest_fitness (float): Fitness of personal best
    """
    
    def __init__(self, dim: int, bounds: Tuple[float, float]):
        """
        Initialize particle with random position and velocity.
        
        Args:
            dim: Dimension of search space (number of network nodes)
            bounds: (min, max) bounds for position values
        """
        self.dim = dim
        self.bounds = bounds
        
        # Random initialization - x_i(0) ~ Uniform(bounds)
        self.position = np.random.uniform(bounds[0], bounds[1], dim)
        
        # Random velocity - v_i(0) ~ Uniform(-v_max, v_max)
        v_max = (bounds[1] - bounds[0]) * 0.5
        self.velocity = np.random.uniform(-v_max, v_max, dim)
        
        # Personal best initially equals current position
        self.pbest = self.position.copy()
        self.pbest_fitness = -np.inf
    
    def update_velocity(
        self, 
        gbest: np.ndarray, 
        w: float = 0.8, 
        c1: float = 2.0, 
        c2: float = 2.0
    ) -> None:
        """
        Update velocity using PSO equation.
        
        v_i(t+1) = w·v_i(t) + c1·rand()·(P_best - x_i) + c2·rand()·(P_gbest - x_i)
        
        Args:
            gbest: Global best position
            w: Inertia weight
            c1: Cognitive coefficient
            c2: Social coefficient
        """
        # Random components - rand() ~ U[0,1]
        r1 = np.random.random(self.dim)
        r2 = np.random.random(self.dim)
        
        # Inertia component
        inertia = w * self.velocity
        
        # Cognitive component (personal experience)
        cognitive = c1 * r1 * (self.pbest - self.position)
        
        # Social component (swarm experience)
        social = c2 * r2 * (gbest - self.position)
        
        # Velocity update
        self.velocity = inertia + cognitive + social
        
        # Clamp velocity to bounds
        v_max = (self.bounds[1] - self.bounds[0]) * 0.5
        self.velocity = np.clip(self.velocity, -v_max, v_max)
    
    def update_position(self) -> None:
        """
        Update position using velocity.
        
        x_i(t+1) = x_i(t) + v_i(t+1)
        """
        self.position = self.position + self.velocity
        
        # Ensure position stays within bounds
        self.position = np.clip(self.position, self.bounds[0], self.bounds[1])
    
    def update_pbest(self, fitness: float) -> bool:
        """
        Update personal best if current fitness is better.
        
        Args:
            fitness: Current position fitness value
            
        Returns:
            True if pbest was updated
        """
        if fitness > self.pbest_fitness:
            self.pbest = self.position.copy()
            self.pbest_fitness = fitness
            return True
        return False
```

#### Swarm Class

```python
"""
Swarm class for managing the particle population.
"""

import numpy as np
from typing import List, Callable, Optional, Tuple
from .particle import Particle

class Swarm:
    """
    Manages the particle swarm for PSO-IPTBK.
    
    Attributes:
        particles (List[Particle]): List of particles
        gbest (np.ndarray): Global best position
        gbest_fitness (float): Fitness of global best
    """
    
    def __init__(
        self, 
        n_particles: int, 
        dim: int, 
        bounds: Tuple[float, float]
    ):
        """
        Initialize swarm with n_particles.
        
        Args:
            n_particles: Number of particles (typically = attack packets)
            dim: Dimension of search space
            bounds: (min, max) bounds for positions
        """
        self.n_particles = n_particles
        self.dim = dim
        self.bounds = bounds
        
        # Initialize particles with random positions
        self.particles: List[Particle] = [
            Particle(dim, bounds) for _ in range(n_particles)
        ]
        
        # Global best
        self.gbest: Optional[np.ndarray] = None
        self.gbest_fitness: float = -np.inf
        
        # Oscillation detection
        self.oscillation_count: int = 0
        self.prev_distance: float = np.inf
    
    def optimize(
        self,
        fitness_func: Callable[[np.ndarray], float],
        max_iter: int = 500,
        w: float = 0.8,
        c1: float = 2.0,
        c2: float = 2.0,
        oscillation_threshold: float = 1e-6,
        oscillation_alpha: int = 10,
        rho: float = 0.5
    ) -> Tuple[np.ndarray, float, List[float]]:
        """
        Run PSO optimization.
        
        Args:
            fitness_func: Function to evaluate particle fitness
            max_iter: Maximum iterations
            w: Inertia weight
            c1: Cognitive coefficient
            c2: Social coefficient
            oscillation_threshold: Threshold for oscillation detection
            oscillation_alpha: Number of consecutive small changes to detect oscillation
            rho: Acceleration ratio for escaping oscillation
            
        Returns:
            (gbest, gbest_fitness, fitness_history)
        """
        fitness_history = []
        
        for iteration in range(max_iter):
            # Evaluate all particles
            for particle in self.particles:
                fitness = fitness_func(particle.position)
                
                # Update personal best
                particle.update_pbest(fitness)
                
                # Update global best
                if fitness > self.gbest_fitness:
                    self.gbest = particle.position.copy()
                    self.gbest_fitness = fitness
            
            fitness_history.append(self.gbest_fitness)
            
            # Check oscillation
            if self.gbest is not None:
                distance = np.linalg.norm(self.gbest - self.particles[0].position)
                
                if abs(distance - self.prev_distance) < oscillation_threshold:
                    self.oscillation_count += 1
                else:
                    self.oscillation_count = 0
                
                self.prev_distance = distance
                
                # Apply oscillation escape if detected
                if self.oscillation_count >= oscillation_alpha:
                    self._escape_oscillation(rho)
                    self.oscillation_count = 0
            
            # Update velocities and positions
            for particle in self.particles:
                particle.update_velocity(self.gbest, w, c1, c2)
                particle.update_position()
        
        return self.gbest, self.gbest_fitness, fitness_history
    
    def _escape_oscillation(self, rho: float) -> None:
        """
        Apply revised position update to escape local optimum.
        
        x_i(t+1) = x_i(t) + rho[(x_max - x_min)]
        
        Args:
            rho: Acceleration ratio
        """
        x_range = self.bounds[1] - self.bounds[0]
        
        for particle in self.particles:
            # Calculate position-based acceleration
            position_rho = (particle.position - self.bounds[0]) / x_range
            
            # Apply revised update
            particle.position = particle.position + rho * position_rho * x_range
            
            # Ensure bounds
            particle.position = np.clip(
                particle.position, 
                self.bounds[0], 
                self.bounds[1]
            )
```

#### Fitness Function

```python
"""
Fitness functions for evaluating attack routes.
"""

import numpy as np
from typing import List, Tuple

def route_fitness(
    position: np.ndarray,
    gbest: np.ndarray,
    packet_counts: np.ndarray,
    route_edges: List[Tuple[int, int]]
) -> float:
    """
    Calculate fitness of a potential attack route.
    
    Fitness is based on:
    1. Distance to global best (closer is better)
    2. Packet count alignment with route
    
    Args:
        position: Particle position representing a route
        gbest: Global best position
        packet_counts: Number of packets at each node
        route_edges: List of (from, to) edges in the route
        
    Returns:
        Fitness value (higher is better)
    """
    # Distance to global best (Euclidean)
    distance = np.linalg.norm(position - gbest)
    
    # Packet alignment score
    packet_score = np.sum(packet_counts * position) / np.sum(packet_counts)
    
    # Combined fitness (inverse distance + packet score)
    fitness = 1.0 / (1.0 + distance) + packet_score
    
    return fitness


def coverage_percentage(
    attack_path_packets: int,
    total_packets: int,
    path_hops: int
) -> float:
    """
    Calculate coverage percentage metric.
    
    Coverage % = (Average packets per hop / Total packets) × 100
    
    Args:
        attack_path_packets: Total packets on identified attack path
        total_packets: Total packets collected
        path_hops: Number of hops in attack path
        
    Returns:
        Coverage percentage
    """
    if total_packets == 0:
        return 0.0
    
    avg_packets_per_hop = attack_path_packets / path_hops
    coverage = (avg_packets_per_hop / total_packets) * 100.0
    
    return coverage


def false_rate(
    particles_off_route: int,
    total_particles: int
) -> float:
    """
    Calculate false rate of position updating.
    
    FR = (Particles not on optimal route / Total particles)
    
    Args:
        particles_off_route: Number of particles not on optimal route
        total_particles: Total number of particles
        
    Returns:
        False rate (lower is better)
    """
    if total_particles == 0:
        return 0.0
    
    return particles_off_route / total_particles
```

---

## 📊 Experimental Results

### Test Case 1: 24-Node Network

#### Network Configuration
- **Nodes**: 24 (4 LANs with 3 hosts each)
- **Attack Packets**: 1800 (m = 1800 particles)
- **Attack Duration**: 120 seconds (6 cycles)
- **Attack Type**: UDP flood

#### Results

| Metric | Value |
|--------|-------|
| **Coverage Percentage** | **98.33%** |
| **False Rate** | **1.67%** |
| **Accuracy** | **98.33%** |

#### Identified Attack Routes

| Attack Route | Packets Collected | Coverage % |
|--------------|-------------------|------------|
| router1(1)→router2(0)→router2(1)→router5(0)→router5(1)→router8(1) | 570 | 31.67% |
| router2(1)→router5(0)→router5(1)→router8(1) | 600 | 33.33% |
| router4(0)→router1(3)→router1(2)→router3(0)→router3(1)→router6(0)→router6(1)→router8(2) | 600 | 33.33% |

### Test Case 2: 40-Node Network

#### Network Configuration
- **Nodes**: 40 (8 LANs)
- **Attack Packets**: 8400 (m = 8400 particles)
- **Attack Duration**: 12 seconds (bursts)
- **Attack Type**: Irregular packet bursts

#### Results

| Metric | Value |
|--------|-------|
| **Coverage Percentage** | **94.64%** |
| **False Rate** | **5.36%** |
| **Accuracy** | **94.64%** |

### Monte Carlo Analysis

**Setup**: 200 random attacks with varying particle colony sizes

| Particle Count (m) | Convergence Speed | Performance |
|-------------------|-------------------|-------------|
| 1000 | Fastest | Most efficient |
| 4000 | Medium | Good |
| 8000 | Slowest | Decreased performance |

**Key Finding**: Smaller particle colonies (m=1000) converge faster and more efficiently than larger ones.

### Performance Summary

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         PERFORMANCE SUMMARY                                  │
└─────────────────────────────────────────────────────────────────────────────┘

    Accuracy (%)
    100 │                                    ┌─────────┐
        │                                    │  98.33% │
     95 │            ┌─────────┐            │ 24 nodes│
        │            │ 94.64%  │            └─────────┘
     90 │            │40 nodes │
        │            └─────────┘
     85 │
        │
     80 └────────────────────────────────────────────────────────────────
              24 Nodes              40 Nodes

    Observations:
    • Larger networks show decreased accuracy (expected due to complexity)
    • Oscillation detection improves convergence
    • 3% sampling rate sufficient for high accuracy
```

---

## 📁 Project Structure

```
pso-iptbk-ddos/
├── README.md                          # Project documentation
├── LICENSE                            # MIT License
├── .gitignore                         # Git ignore rules
│
├── docs/                              # Documentation
│   ├── concept_map/                   # Concept map files
│   │   ├── PSO_IPTBK_ConceptMap.drawio
│   │   └── concept_map.png
│   ├── scribes/                       # Scribe submissions
│   │   ├── milestone_1.md
│   │   ├── milestone_2.md
│   │   ├── milestone_3.md
│   │   ├── milestone_4.md
│   │   ├── milestone_5.md
│   │   └── milestone_6.md
│   ├── video/                         # Video presentations
│   │   └── README.md
│   └── paper/                         # Research paper
│       └── DoSS_PSO.pdf
│
├── src/                               # Source code
│   ├── pso/                           # PSO algorithm
│   │   ├── __init__.py
│   │   ├── particle.py
│   │   ├── swarm.py
│   │   ├── fitness.py
│   │   └── oscillation.py
│   │
│   ├── network/                       # Network simulation
│   │   ├── __init__.py
│   │   ├── topology.py
│   │   ├── router.py
│   │   └── spie.py
│   │
│   ├── simulation/                    # OMNeT++ integration
│   │   ├── __init__.py
│   │   └── omnetpp_integration.py
│   │
│   └── utils/                         # Utilities
│       ├── __init__.py
│       ├── metrics.py
│       └── visualization.py
│
├── experiments/                       # Experimental results
│   ├── case_24_nodes/
│   │   ├── config.ini
│   │   ├── results.csv
│   │   └── plots/
│   └── case_40_nodes/
│       ├── config.ini
│       ├── results.csv
│       └── plots/
│
├── tests/                             # Unit tests
│   ├── test_particle.py
│   ├── test_swarm.py
│   └── test_fitness.py
│
└── data/                              # Sample data
    ├── network_topologies/
    └── packet_samples/
```

---

## 🚀 Installation & Usage

### Prerequisites

- Python 3.8+
- NumPy
- Matplotlib (for visualization)
- OMNeT++ 5.5.1 (for network simulation)
- INET 4 Framework

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/pso-iptbk-ddos.git
cd pso-iptbk-ddos

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Usage

#### 1. Run PSO Algorithm

```python
from src.pso.swarm import Swarm
from src.pso.fitness import route_fitness
import numpy as np

# Initialize swarm
n_particles = 1800  # Number of attack packets
dim = 24  # Network nodes
bounds = (0, 100)  # Position bounds

swarm = Swarm(n_particles, dim, bounds)

# Define fitness function
def fitness_func(position):
    # Your fitness evaluation logic
    return route_fitness(position, gbest, packet_counts, route_edges)

# Run optimization
gbest, gbest_fitness, history = swarm.optimize(
    fitness_func=fitness_func,
    max_iter=500,
    w=0.8,
    c1=2.0,
    c2=2.0
)

print(f"Best route found: {gbest}")
print(f"Fitness: {gbest_fitness}")
```

#### 2. Run Simulation (OMNeT++)

```bash
# Navigate to simulation directory
cd simulation/

# Run simulation
opp_run -r 0 -m -u Cmdenv -c DDoSAttack -n .:../inet4/src:../inet4/examples:../inet4/tutorials:../inet4/showcases --image-path=../inet4/images -l ../inet4/src/INET omnetpp.ini
```

#### 3. Analyze Results

```python
from src.utils.metrics import coverage_percentage, false_rate

# Calculate metrics
coverage = coverage_percentage(
    attack_path_packets=570,
    total_packets=1800,
    path_hops=6
)

fr = false_rate(
    particles_off_route=30,
    total_particles=1800
)

print(f"Coverage: {coverage:.2f}%")
print(f"False Rate: {fr*100:.2f}%")
```

---

## 👥 Team & Milestones

### Team Structure

| Role | Responsibility | Member |
|------|----------------|--------|
| **Project Manager** | GitHub management, coordination, submissions | TBD |
| **Scribes (2)** | Answer scribe questions, documentation | TBD |
| **Video Team (2)** | Create 20-min video presentations | TBD |
| **Reviewer** | Review work, concept map, quality check | TBD |

### Milestone Timeline

| Milestone | Deadline | Focus Area | Deliverables |
|-----------|----------|------------|--------------|
| **M1** | Feb 4, 2026 | Problem definition, random variables | Scribe, Video, Concept Map, GitHub |
| **M2** | TBD | Probabilistic modeling refinement | Scribe, Video, Updated Concept Map |
| **M3** | TBD | Implementation & simulation | Scribe, Video, Code |
| **M4** | TBD | Experimental results & analysis | Scribe, Video, Results |
| **M5** | TBD | Optimization & improvements | Scribe, Video, Enhanced Model |
| **M6** | TBD | Final report & presentation | Complete documentation |

### Current Milestone: M1

**Status**: In Progress  
**Focus**: Define probabilistic problem, identify random variables, establish conceptual framework

**Deliverables**:
- [ ] Scribe answers (6 questions)
- [ ] 20-minute video presentation
- [ ] Concept map
- [ ] GitHub repository setup

---

## 📚 References

1. **Primary Paper**:
   - Lin, H.C., Wang, P., & Lin, W.H. (2019). "Implementation of a PSO-Based Security Defense Mechanism for Tracing the Sources of DDoS Attacks." *Computers*, 8(4), 88. MDPI.

2. **PSO Foundation**:
   - Kennedy, J., & Eberhart, R. (1995). "Particle Swarm Optimization." *Proceedings of IEEE International Conference on Neural Networks*, 1942-1948.

3. **IP Traceback**:
   - Savage, S., Wetherall, D., Karlin, A., & Anderson, T. (2001). "Network Support for IP Traceback." *IEEE/ACM Transactions on Networking*, 9(3), 226-237.

4. **SPIE Mechanism**:
   - Snoeren, A.C., Partridge, C., Sanchez, L.A., Jones, C.E., et al. (2001). "Hash-based IP Traceback." *ACM SIGCOMM*, 3-14.

5. **Course Resources**:
   - CSE 400: Fundamentals of Probability in Computing, Ahmedabad University
   - Concept Map Guidelines, SEAS, Ahmedabad University

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Course Instructor**: CSE 400 Teaching Team, Ahmedabad University
- **Research Paper Authors**: Hsiao-Chung Lin, Ping Wang, Wen-Hui Lin
- **Tools**: OMNeT++, INET Framework, Python, NumPy

---

## 📧 Contact

For questions or suggestions, please contact:

- **Course**: CSE 400 - Fundamentals of Probability in Computing
- **University**: School of Engineering and Applied Science, Ahmedabad University
- **Repository**: https://github.com/yourusername/pso-iptbk-ddos

---

<p align="center">
  <b>Fundamentals of Probability in Computing (CSE 400)</b><br>
  <b>School of Engineering and Applied Science</b><br>
  <b>Ahmedabad University</b>
</p>

---

*This README was generated for the CSE 400 course project. The probabilistic model and implementation will evolve across milestones based on feedback and deeper understanding.*
