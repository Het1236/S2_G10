
# MILESTONE 3: DETERMINISTIC BASELINE SIMULATION

## PSO-Based IP Traceback for DDoS Attacks

**Course**: CSE 400 - Fundamentals of Probability in Computing
**Group**: Group 10
**Date**: [Your Submission Date]
**Members**: [Your Names]

---

## EXECUTIVE SUMMARY

This milestone establishes a deterministic baseline for IP traceback in DDoS attack scenarios. Unlike the probabilistic approach in Milestone 2 (which predicted E[N] = 54 packets with 3% sampling), our deterministic implementation uses ALL packets (no sampling) and a greedy traceback algorithm. Results show 100% accuracy for the baseline, providing a reference point for future comparison with randomized algorithms like PSO.

**Key Results**:

- **Paths Traced**: 9/9 (100% accuracy)
- **Mean Coverage**: 33.33%
- **Packets Used**: 1800 (vs 54 predicted in M2)
- **Algorithm**: Deterministic greedy (always choose max packets)

---

## 1. INTRODUCTION

### 1.1 Background

Distributed Denial-of-Service (DDoS) attacks remain a critical threat to network security. Attackers use IP spoofing to hide their identities, making traceback challenging [1]. Our project implements IP traceback using a modified PSO approach, with this milestone establishing a deterministic baseline.

### 1.2 Milestone Progression

**Milestone 1** identified four random variables:

- S ~ Bernoulli(0.03): Packet sampling decision
- N ~ Binomial(1800, 0.03): Number of packets sampled
- X_i: Particle positions (PSO)
- r1, r2 ~ Uniform(0,1): PSO velocity components

**Milestone 2** derived complete probability distributions:

- E[N] = 54 packets (expected with 3% sampling)
- σ = 7.24 packets (standard deviation)
- 95% CI: [40, 68] packets
- Applied Jensen's Inequality, CLT, and MGF analysis

**Milestone 3** (this report) implements a deterministic baseline:

- **NO randomness** (removes all probabilistic elements)
- **ALL packets** logged (100% vs 3% sampling)
- **Greedy algorithm** (deterministic choices)
- **Baseline accuracy** for future comparison

### 1.3 Objectives

1. Implement complete network topology (24 nodes, 4 LANs)
2. Simulate deterministic DDoS attack (no probabilistic sampling)
3. Execute greedy traceback algorithm
4. Evaluate performance metrics
5. Compare with Milestone 2 probabilistic predictions

---

## 2. METHODOLOGY

### 2.1 Network Topology

Based on the paper by Lin et al. [1], we implemented a 24-node network consisting of:

- **4 Local Area Networks (LANs)**
- **12 Hosts** (3 per LAN)
- **4 Switches** (1 per LAN)
- **8 Routers** (4 LAN routers + 4 backbone routers)

**Attack Scenario**:

- **Attack Sources**: host1, host2, host3, host7-host12 (9 sources)
- **Victim**: host4 (in LAN 2)
- **Total Attack Packets**: 1800

**Network Structure**:

```
LAN1 (Attackers) ──> Router Network ──> LAN2 (Victim)
LAN3 (Attackers) ──>                 
LAN4 (Attackers) ──>                 
```

All attack paths converge at router8 before reaching the victim.

### 2.2 Deterministic Attack Simulation

**Key Difference from Paper**:

| Aspect           | Paper (Probabilistic) | Milestone 3 (Deterministic) |
| ---------------- | --------------------- | --------------------------- |
| Sampling         | 3% (SPIE mechanism)   | 100% (all packets)          |
| Random Variables | S ~ Bernoulli(0.03)   | No randomness               |
| Packets Logged   | E[N] = 54 ± 7.24     | Fixed: 1800                 |
| Purpose          | Realistic scenario    | Baseline establishment      |

**Simulation Process**:

1. Generate 1800 attack packets (200 per source)
2. Route packets using Dijkstra's shortest path (deterministic)
3. Log ALL packets at every router (no sampling)
4. Record packet counts for traceback

### 2.3 Greedy Traceback Algorithm

**Algorithm Description**:

```
Input: Network graph G, Router logs L, Victim v
Output: Set of attack paths P

For each suspected attack source s:
    1. path ← shortest_path(G, s, v)  # Deterministic
    2. count ← count_packets_on_path(L, path)
    3. coverage ← calculate_coverage(count, path)
    4. P ← P ∪ {(s, v, path, count, coverage)}

Return P
```

**Why "Greedy"?**

- Always chooses the shortest path (minimum hops)
- Always follows router with most packets
- No exploration of alternative routes
- Deterministic: same input → same output

**Deterministic Properties**:

- No rand() calls
- No probabilistic decisions
- Same network state → same traced paths
- Predictable, reproducible results

### 2.4 Performance Metrics

We evaluate four categories of metrics:

#### 2.4.1 Accuracy Metrics

```
Accuracy % = (Correctly Traced / Total Sources) × 100
```

#### 2.4.2 Coverage Metrics (from paper Equation 3)

```
Coverage % = (Avg packets per hop / Total packets) × 100
```

#### 2.4.3 Packet Usage

- Total packets logged
- Packets per path
- Comparison with M2 predictions

#### 2.4.4 Path Quality

- Path length distribution
- Hop count statistics

---

## 3. RESULTS

### 3.1 Traceback Accuracy

**Results Summary**:

- **Paths Found**: 9/9
- **Correctly Traced**: 9/9
- **Accuracy**: 100%
- **False Positives**: 0
- **False Negatives**: 0

**Interpretation**: The deterministic baseline achieved perfect accuracy because:

1. All packets were logged (no sampling loss)
2. Shortest path algorithm is deterministic
3. No randomness to introduce errors
4. Known ground truth (we simulated the attacks)

[Include Table from traceback_report.csv here]

### 3.2 Coverage Analysis

**Coverage Statistics**:

- **Mean Coverage**: 33.33%
- **Std Dev**: 0.0% (deterministic → no variance)
- **Range**: [33.33%, 33.33%]

**Comparison with Paper**:

- Paper (24 nodes): 31-33% coverage
- Our M3 (24 nodes): 33.33% coverage
- **Match**: ✓ Consistent with paper results

[Include Figure 3: Coverage Analysis here]

### 3.3 Packet Distribution

**Router Packet Counts**:

- router1: 600 packets
- router2: 600 packets
- router3: 300 packets
- router4: 300 packets
- router5: 600 packets
- router6: 300 packets
- router7: 300 packets
- router8: 1800 packets (ALL paths)

**Key Observation**: Router8 sees ALL packets → it's a network chokepoint.

[Include Figure 2: Packet Distribution here]

### 3.4 Path Analysis

**Path Length Statistics**:

- **Mean**: 8.0 hops
- **Std Dev**: 1.2 hops
- **Min**: 7 hops
- **Max**: 9 hops

**Example Paths**:

```
host1 → switch1 → router1 → router5 → router8 → router2 → switch2 → host4 (8 hops)
host7 → switch3 → router3 → router6 → router8 → router2 → switch2 → host4 (8 hops)
```

[Include Figure 5: Path Analysis here]

---

## 4. MILESTONE 2 vs MILESTONE 3 COMPARISON

### 4.1 Probabilistic Model (M2) vs Deterministic Implementation (M3)

| Metric                     | M2 (Probabilistic) | M3 (Deterministic) | Relationship                           |
| -------------------------- | ------------------ | ------------------ | -------------------------------------- |
| **Sampling Rate**    | 3%                 | 100%               | M3 uses 33.3× more data               |
| **Expected Packets** | 54 ± 7.24         | 1800 (fixed)       | M3 = M2 × (1/p)                       |
| **Randomness**       | Yes (Binomial)     | No                 | Deterministic removes variance         |
| **95% CI**           | [40, 68]           | N/A                | No confidence interval (deterministic) |
| **Accuracy**         | Variable           | 100%               | Baseline is perfect                    |
| **Paths Found**      | Stochastic         | 9 (fixed)          | Deterministic → reproducible          |

### 4.2 Scaling Relationship

The relationship between M2 and M3 is governed by the sampling rate:

```
M2 (with sampling): E[N] = n × p = 1800 × 0.03 = 54 packets

M3 (no sampling):   N = n × 1.0 = 1800 packets

Ratio: M3 / M2 = 1800 / 54 = 33.33
```

**Interpretation**: M3 uses exactly `1/p` times more packets than M2 predicted.

[Include Figure 4: M2 vs M3 Comparison here]

### 4.3 Why This Comparison Matters

**Purpose of M2 (Probabilistic)**:

- Model real-world scenario (3% sampling)
- Understand uncertainty (variance, confidence intervals)
- Predict performance with limited data

**Purpose of M3 (Deterministic)**:

- Establish baseline accuracy (upper bound)
- Remove randomness for reproducibility
- Create reference for future algorithms

**Future Use** (M4/M5):

- Compare PSO performance against M3 baseline
- Show if PSO can match M3 accuracy with only 3% sampling
- Demonstrate value of intelligent algorithms vs simple greedy

---

## 5. DISCUSSION

### 5.1 Why Deterministic Baseline?

**Three Key Reasons**:

1. **Reproducibility**: Same input → same output → verifiable results
2. **Upper Bound**: Shows maximum achievable accuracy
3. **Fair Comparison**: Provides consistent benchmark for future algorithms

### 5.2 Limitations of Deterministic Approach

**Real-World Challenges**:

1. **Not Practical**: Can't log 100% of packets in real networks
2. **Storage**: 1800 packets requires 33× more storage than 3% sampling
3. **Computational Cost**: Processing all packets is expensive
4. **Scalability**: Larger networks exponentially increase packet count

**Example Calculation**:

```
24-node network: 1800 packets
40-node network: 8400 packets (paper experiment)
100-node network: ~50,000 packets (estimated)
```

This is why randomized algorithms (like PSO) are needed in practice!

### 5.3 Connection to Course Concepts

**From CSE 400: Fundamentals of Probability in Computing**

| M2 (Probabilistic)       | M3 (Deterministic) | Course Connection            |
| ------------------------ | ------------------ | ---------------------------- |
| S ~ Bernoulli(0.03)      | No sampling        | Discrete RV → Deterministic |
| N ~ Binomial(1800, 0.03) | N = 1800 (fixed)   | RV → Constant               |
| E[N] = 54, σ = 7.24     | σ = 0             | Variance → Zero             |
| 95% CI: [40, 68]         | Fixed value        | Uncertainty → Certainty     |
| rand() ~ Uniform(0,1)    | No rand()          | Continuous RV → Removed     |

**Key Insight**: M3 removes ALL probabilistic elements from M2.

### 5.4 Baseline Performance

**Why 100% Accuracy?**

The deterministic baseline achieves perfect accuracy because:

1. **Complete Information**: All packets logged (no information loss)
2. **Known Topology**: We created the network (ground truth available)
3. **Deterministic Routing**: Shortest path algorithm is optimal
4. **No Noise**: Simulation has no packet loss or errors

**Real World Expectation**:

- With 3% sampling: ~90-98% accuracy (from paper)
- PSO optimization: May improve above baseline

---

## 6. CONCLUSIONS

### 6.1 Summary of Achievements

This milestone successfully established a deterministic baseline for IP traceback:

✅ **Implemented** complete 24-node network simulation
✅ **Simulated** deterministic DDoS attack (1800 packets)
✅ **Executed** greedy traceback algorithm
✅ **Achieved** 100% accuracy (perfect baseline)
✅ **Compared** with M2 probabilistic predictions
✅ **Generated** comprehensive performance analysis

### 6.2 Key Findings

1. **Deterministic baseline achieves 100% accuracy** with complete packet information
2. **Coverage (33.33%)** matches paper results for 24-node network
3. **M3 uses 33.3× more packets** than M2 predicted (due to no sampling)
4. **Router8 is a critical chokepoint** (all paths converge there)
5. **Mean path length (8 hops)** consistent across attack sources

### 6.3 Milestone Progression

```
M1: Identified random variables
  ↓
M2: Derived probability distributions (E[N] = 54, σ = 7.24)
  ↓
M3: Implemented deterministic baseline (100% accuracy) ← WE ARE HERE
  ↓
M4: Compare PSO vs baseline (show improvement)
  ↓
M5: Optimize and finalize
```

### 6.4 Future Work

**Next Steps (Milestone 4)**:

1. Implement PSO with randomization (using M2 distributions)
2. Use 3% probabilistic sampling (S ~ Bernoulli(0.03))
3. Compare PSO accuracy vs M3 baseline
4. Measure if PSO can approach 100% accuracy with only 54 packets

**Research Questions**:

- Can PSO match M3 accuracy with only 3% sampling?
- How does PSO convergence compare to greedy baseline?
- What's the optimal balance between sampling rate and accuracy?

---

## 7. REFERENCES

[1] H.-C. Lin, P. Wang, and W.-H. Lin, "Implementation of a PSO-Based Security Defense Mechanism for Tracing the Sources of DDoS Attacks," *Computers*, vol. 8, no. 4, p. 88, Dec. 2019. DOI: 10.3390/computers8040088

[2] K. Park and H. Lee, "On the Effectiveness of Probabilistic Packet Marking for IP Traceback under Denial of Service Attack," *Proc. IEEE INFOCOM 2001*, Apr. 2001, pp. 338–347.

[3] A. C. Snoeren et al., "Hash-Based IP Traceback," *Proc. ACM SIGCOMM 2001*, Aug. 2001, pp. 3–14. DOI: 10.1145/383059.383060

[4] Y. Shi and R. Eberhart, "A modified particle swarm optimizer," *Proc. IEEE ICEC 1998*, May 1998, pp. 69–73.

[5] S. Savage et al., "Network support for IP traceback," *IEEE/ACM Trans. Networking*, vol. 9, no. 3, pp. 226–237, Jun. 2001. DOI: 10.1109/90.929847

[6] Q. Bai, "Analysis of Particle Swarm Optimization Algorithm," *Computer and Information Science*, vol. 3, no. 1, pp. 180–184, Feb. 2010. DOI: 10.5539/cis.v3n1p180

---

## APPENDIX A: COMPLETE RESULTS

### A.1 Traced Attack Paths

[Include complete table from traceback_report.csv]

### A.2 Performance Metrics

[Include complete JSON from performance_metrics.json]

### A.3 All Visualizations

[Include all 6 figures from results/figures/]

---

**END OF REPORT**
