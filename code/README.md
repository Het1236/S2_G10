
# MILESTONE 3: DETERMINISTIC BASELINE SIMULATION

## PSO-Based IP Traceback for DDoS Attacks

**CSE 400: Fundamentals of Probability in Computing**
**Group 10**
**Submission Date: [Your Date]**

---

## 📋 TABLE OF CONTENTS

1. [Overview](#overview)
2. [What is Milestone 3?](#what-is-milestone-3)
3. [How This Relates to Previous Milestones](#milestone-connections)
4. [Installation &amp; Setup](#installation)
5. [How to Run](#how-to-run)
6. [Understanding the Results](#understanding-results)
7. [File Structure](#file-structure)
8. [Key Concepts Explained](#key-concepts)
9. [Troubleshooting](#troubleshooting)
10. [References](#references)

---

## `<a name="overview"></a>`1. OVERVIEW

This project implements a **deterministic baseline simulation** for IP traceback in DDoS attack scenarios. The goal is to establish a reference point for comparison with future randomized algorithms (like PSO).

### What We're Solving

**Problem**: During a DDoS attack, attackers spoof IP addresses, making it difficult to trace the attack back to its source.

**Our Solution (Milestone 3)**:

- Implement a **deterministic greedy traceback** algorithm
- Use **ALL packets** (no probabilistic sampling)
- Always choose the "greedy" path (most packets)
- Establish a baseline for future comparison

---

## `<a name="what-is-milestone-3"></a>`2. WHAT IS MILESTONE 3?

### Objective

> "Simulate the complete end-to-end scenario with a fixed, deterministic baseline strategy."

### Key Requirements

✅ **No Randomness**

- No rand() calls
- No probabilistic sampling
- Same input → Same output

✅ **Deterministic Algorithm**

- Greedy traceback: Always choose router with most packets
- Shortest path routing
- Predictable behavior

✅ **Complete Simulation Pipeline**

1. Network topology creation (24 nodes, 4 LANs)
2. DDoS attack simulation (1800 packets)
3. Packet routing and logging
4. Traceback execution
5. Performance evaluation

✅ **Comparison with Milestone 2**

- Compare deterministic results with probabilistic predictions
- Show relationship between E[N] = 54 (M2) and actual packet usage (M3)

---

## `<a name="milestone-connections"></a>`3. HOW THIS RELATES TO PREVIOUS MILESTONES

### Connection Flow

```
MILESTONE 1: Problem Identification
    ↓
    Identified 4 random variables:
    - S ~ Bernoulli(0.03)
    - N ~ Binomial(1800, 0.03)
    - X_i (particle positions)
    - r1, r2 ~ Uniform(0,1)
  
    ↓
  
MILESTONE 2: Mathematical Modeling
    ↓
    Derived probability distributions:
    - E[N] = 54 packets (expected with 3% sampling)
    - σ = 7.24 packets
    - 95% CI: [40, 68]
    - Jensen's inequality for risk
    - CLT validation
  
    ↓
  
MILESTONE 3: Deterministic Baseline ← WE ARE HERE
    ↓
    Implementation WITHOUT randomness:
    - Use ALL packets (not 3% sample)
    - Greedy algorithm (deterministic)
    - Establishes baseline accuracy
    - Compare with M2 predictions
```

### Key Differences from Paper

| Aspect                     | Paper (Lin et al. 2019)  | Our Milestone 3        |
| -------------------------- | ------------------------ | ---------------------- |
| **Sampling**         | 3% probabilistic (SPIE)  | 100% (all packets)     |
| **Algorithm**        | PSO (randomized)         | Greedy (deterministic) |
| **Random Variables** | Yes (Bernoulli, Uniform) | No (fixed choices)     |
| **Purpose**          | Find optimal routes      | Establish baseline     |
| **Accuracy**         | 98.33% (24 nodes)        | 100% (deterministic)   |

---

## `<a name="installation"></a>`4. INSTALLATION & SETUP

### Prerequisites

- **Python**: 3.8 or higher
- **Operating System**: Windows, macOS, or Linux
- **RAM**: At least 4GB
- **Storage**: ~100MB for project files

### Step 1: Install Python

**Check if Python is installed:**

```bash
python --version
```

If not installed, download from: https://www.python.org/downloads/

### Step 2: Clone/Download Project

Option A - If you have the files:

```bash
cd path/to/milestone3_deterministic_traceback
```

Option B - If starting fresh:

```bash
mkdir milestone3_deterministic_traceback
cd milestone3_deterministic_traceback
```

Then copy all the files I provided into this directory.

### Step 3: Install Dependencies

```bash
# Install required packages
pip install -r requirements.txt
```

This installs:

- numpy, pandas, scipy (numerical computing)
- matplotlib, seaborn (visualization)
- networkx (graph algorithms)
- simpy (simulation)

### Step 4: Verify Installation

```bash
python -c "import numpy, pandas, matplotlib, networkx, scipy; print('✓ All packages installed!')"
```

If you see "✓ All packages installed!" you're ready to go!

---

## `<a name="how-to-run"></a>`5. HOW TO RUN

### Quick Start (Easiest Way)

**Just run this command:**

```bash
python main.py
```

That's it! The script will:

1. Create the network (24 nodes)
2. Simulate the attack (1800 packets)
3. Trace back to attack sources
4. Generate all visualizations
5. Create performance reports

### Expected Output

```
================================================================================
             MILESTONE 3: DETERMINISTIC BASELINE SIMULATION
                    PSO-Based IP Traceback for DDoS Attacks
================================================================================

CSE 400: Fundamentals of Probability in Computing
Group 10
Execution Date: 2026-03-02 10:30:45

================================================================================

✓ Directories set up

────────────────────────────────────────────────────────────────────────────────
STEP 1: CREATING NETWORK TOPOLOGY
────────────────────────────────────────────────────────────────────────────────
Creating network topology...
Network created: 24 nodes, 56 edges
✓ Network created: 24 nodes, 56 edges
  Attack sources: 9
  Victim: host4

────────────────────────────────────────────────────────────────────────────────
STEP 2: SIMULATING DDOS ATTACK (DETERMINISTIC)
────────────────────────────────────────────────────────────────────────────────
NOTE: This is deterministic - we log ALL packets (not 3% sample)

======================================================================
STARTING DETERMINISTIC DDOS ATTACK SIMULATION
======================================================================

[Step 1/3] Generating attack packets...
  Generated 1800 packets from 9 sources

[Step 2/3] Routing packets (deterministic shortest paths)...

[Step 3/3] Logging packets at routers (ALL packets, no sampling)...

  Packets logged per router:
    router1: 600 packets
    router2: 600 packets
    router3: 300 packets
    ...

======================================================================
ATTACK COMPLETE:
  Total packets sent: 1800
  Routers with logs: 8
======================================================================

... (continues with traceback and evaluation)

✅ Simulation completed successfully!
```

### Run Individual Components

If you want to run components separately:

```bash
# 1. Create network only
python -c "from network_topology import NetworkTopology; n = NetworkTopology(); n.create_topology(); n.visualize()"

# 2. Simulate attack only
python attack_simulator.py

# 3. Run traceback only
python deterministic_traceback.py

# 4. Generate visualizations only
python visualization.py
```

### Verbose Mode (More Details)

```bash
python main.py --verbose
```

### Quiet Mode (Less Output)

```bash
python main.py --quiet
```

---

## `<a name="understanding-results"></a>`6. UNDERSTANDING THE RESULTS

After running `main.py`, you'll have several output files. Here's what each one means:

### 📁 Generated Files

```
milestone3_deterministic_traceback/
│
├── data/
│   ├── network_config.json          ← Network structure
│   └── attack_logs/
│       └── packet_logs.csv          ← All packet information
│
└── results/
    ├── traceback_report.csv         ← Detailed path report
    ├── performance_metrics.json     ← All metrics
    ├── m2_vs_m3_comparison.csv      ← Milestone comparison
    │
    └── figures/                     ← All visualizations
        ├── 1_network_traced_paths.png
        ├── 2_packet_distribution.png
        ├── 3_coverage_analysis.png
        ├── 4_m2_vs_m3_comparison.png
        ├── 5_path_analysis.png
        └── 6_summary_dashboard.png
```

### 📊 Key Results Files

#### 1. `traceback_report.csv`

**What it shows**: Detailed information about each traced attack path.

**Example content**:

```csv
Attack Source,Victim,Path,Path Length (hops),Packets on Path,Coverage %
host1,host4,host1 → switch1 → router1 → router5 → router8 → router2 → switch2 → host4,8,600,33.33%
host2,host4,host2 → switch1 → router1 → router5 → router8 → router2 → switch2 → host4,8,600,33.33%
...
```

**How to read it**:

- Each row = one attack path
- Path shows the route packets took
- Coverage % = how well this path is covered by packets

#### 2. `performance_metrics.json`

**What it shows**: Comprehensive performance statistics.

**Key metrics**:

```json
{
  "accuracy": {
    "total_paths_found": 9,
    "correctly_traced": 9,
    "accuracy_percentage": 100.0
  },
  "coverage": {
    "mean_coverage": 33.33,
    "std_coverage": 0.0,
    "min_coverage": 33.33,
    "max_coverage": 33.33
  },
  "packet_usage": {
    "total_packets_logged": 1800,
    "m2_predicted_with_sampling": 54,
    "m3_actual_no_sampling": 1800,
    "ratio_m3_to_m2": 33.33
  }
}
```

**How to interpret**:

- **accuracy_percentage**: 100% means all attacks were traced correctly
- **mean_coverage**: Average coverage across all paths
- **ratio_m3_to_m2**: M3 uses 33x more packets than M2 predicted (because no sampling)

#### 3. `m2_vs_m3_comparison.csv`

**What it shows**: Side-by-side comparison of Milestone 2 vs Milestone 3.

**Example**:

```csv
Metric,Milestone 2 (Probabilistic),Milestone 3 (Deterministic)
Packets Used,1800 total,1800 (all logged)
Sampling Rate,3%,100% (no sampling)
Expected Packets (with sampling),54,1800
Accuracy,Variable (depends on samples),100% (perfect for baseline)
```

---

### 📈 Visualization Explanations

#### Figure 1: `1_network_traced_paths.png`

**What it shows**: The network topology with all traced attack paths overlaid.

**How to read it**:

- **Red/Blue/Green lines**: Different attack paths
- **Squares**: Attack sources
- **Gold star**: Victim (host4)
- **Arrows**: Direction of attack traffic

**What to look for**:

- Do all paths converge at the victim?
- Are paths diverse or similar?
- Which routers are most heavily used?

---

#### Figure 2: `2_packet_distribution.png`

**What it shows**: How many packets were logged at each router.

**Left panel (Bar chart)**:

- Height = number of packets at that router
- Routers on attack paths have more packets

**Right panel (Pie chart)**:

- Shows relative distribution
- Helps identify critical routers

**Interpretation**:

```
If router8 has 1800 packets:
→ ALL attack paths pass through router8
→ router8 is a "chokepoint" in the network
→ Good place to deploy defenses
```

---

#### Figure 3: `3_coverage_analysis.png`

**What it shows**: Coverage percentage for each attack path.

**Formula (from paper Equation 3)**:

```
Coverage % = (Average packets per hop / Total packets) × 100
```

**Left panel**: Bar chart per attack source
**Right panel**: Distribution histogram

**Good coverage** = 30-40% (from paper experiments)

**Interpretation**:

```
If mean coverage = 33.33%:
→ Matches paper results for 24-node network
→ Indicates balanced packet distribution
→ Good traceback quality
```

---

#### Figure 4: `4_m2_vs_m3_comparison.png`

**THE MOST IMPORTANT FIGURE FOR YOUR REPORT**

**What it shows**: Direct comparison between probabilistic model (M2) and deterministic implementation (M3).

**Panel 1 (Top Left)**: Packet usage comparison

- M2 predicted 54 packets (with 3% sampling)
- M3 used 1800 packets (no sampling)
- Ratio: 33.33x difference

**Panel 2 (Top Right)**: Binomial distribution from M2

- Shows E[N] = 54 as the expected value
- 95% CI [40, 68]
- M3 uses ALL packets outside this range

**Panel 3 (Bottom Left)**: Sampling rate

- M2: 3% (probabilistic)
- M3: 100% (deterministic)

**Panel 4 (Bottom Right)**: Summary table

- Side-by-side comparison
- Use this in your report!

---

#### Figure 5: `5_path_analysis.png`

**What it shows**: Statistics about path lengths.

**Left panel**: Path length per attack source
**Right panel**: Distribution of path lengths

**Key metric**: Mean path length

```
If mean = 8 hops:
→ On average, attacks travel through 8 nodes
→ Longer paths = more opportunities for detection
→ Shorter paths = faster attacks
```

---

#### Figure 6: `6_summary_dashboard.png`

**What it shows**: Everything at a glance!

This is your **executive summary** - use it in presentations.

**Sections**:

1. Key metrics (top left)
2. Network overview (top center/right)
3. Packet distribution (middle left)
4. Coverage distribution (middle center)
5. Path lengths (middle right)
6. M2 vs M3 table (bottom)

---

## `<a name="file-structure"></a>`7. FILE STRUCTURE

### Core Python Files

#### `network_topology.py`

**Purpose**: Creates the 24-node network structure.

**Key classes**:

- `NetworkTopology`: Main network class

**What it does**:

```python
network = NetworkTopology()
network.create_topology()
# → Creates 24 nodes, 56 edges, 4 LANs
```

---

#### `attack_simulator.py`

**Purpose**: Simulates deterministic DDoS attack.

**Key difference from paper**:

- Paper: Only logs 3% of packets (probabilistic)
- Us: Logs ALL packets (deterministic)

**Key classes**:

- `DeterministicAttackSimulator`: Simulates attack
- `Packet`: Represents a network packet

---

#### `deterministic_traceback.py`

**Purpose**: Implements the greedy traceback algorithm.

**Algorithm**:

```
For each attack source:
  1. Find shortest path to victim
  2. Count packets on path
  3. Calculate coverage %
  4. Record the path
```

**Key classes**:

- `GreedyTraceback`: Main traceback algorithm

---

#### `performance_metrics.py`

**Purpose**: Evaluates performance and compares with M2.

**Key metrics**:

- Accuracy (%)
- Coverage (%)
- Packet usage
- Path quality
- M2 vs M3 comparison

---

#### `visualization.py`

**Purpose**: Generates all figures.

**Creates 6 figures**:

1. Network with paths
2. Packet distribution
3. Coverage analysis
4. M2 vs M3 comparison
5. Path analysis
6. Summary dashboard

---

#### `main.py`

**Purpose**: Orchestrates everything.

**Runs the complete pipeline**:

```bash
python main.py
```

---

## `<a name="key-concepts"></a>`8. KEY CONCEPTS EXPLAINED

### For Complete Beginners

#### What is "Deterministic"?

**Definition**: Same input always gives same output. No randomness.

**Example**:

```python
# Deterministic
def add(a, b):
    return a + b

add(5, 3)  # Always returns 8

# Non-deterministic (random)
import random
def random_add(a, b):
    return a + b + random.randint(0, 10)

random_add(5, 3)  # Could return 8, 9, 10, ..., 18
```

**In our project**:

- Deterministic: Always choose router with MOST packets
- Non-deterministic (PSO): Use rand() to explore different routes

---

#### What is a "Baseline"?

**Definition**: A simple, standard approach used for comparison.

**Analogy**:

```
You want to test if a new running shoe makes you faster.

Baseline: Run in your old shoes → 10 minutes per mile
Test: Run in new shoes → 9 minutes per mile
Conclusion: New shoes are 10% better than baseline
```

**In our project**:

- Baseline (M3): Greedy deterministic traceback
- Advanced (M4/M5): PSO with randomization
- Goal: Show PSO is better than simple greedy approach

---

#### What is "Coverage Percentage"?

**From paper (Equation 3)**:

```
Coverage % = (Average packets per hop / Total packets) × 100
```

**Example**:

```
Attack path: host1 → router1 → router5 → router8 → router2 → host4
Path length: 5 hops
Total packets on this path: 600
Average per hop: 600 / 5 = 120 packets

Total attack packets: 1800

Coverage % = (120 / 1800) × 100 = 6.67%
```

**But wait!** In the paper, coverage is calculated differently across ALL paths:

```
If we have 3 attack paths, each with 600 packets:
Each path covers: 600 / 1800 = 33.33%
```

**Good coverage** (from paper): 31-33% for 24-node network

---

#### Understanding the Network

**Network Structure (from paper Figure 5)**:

```
LAN 1 (Attack)          Internet Backbone          LAN 2 (Victim)
  
host1 ─┐                                              ┌─ host4 (VICTIM)
host2 ─┼─ switch1 ─ router1 ─ router5 ─┐        ┌─ router2 ─ switch2 ─┼─ host5
host3 ─┘                                │        │                      └─ host6
                                        │        │
LAN 3 (Attack)                         router8 ─┤           LAN 4
                                        │        │
host7 ─┐                                │        │
host8 ─┼─ switch3 ─ router3 ─ router6 ─┘        │
host9 ─┘                                         │
                                                 │
host10 ─┐                                        │
host11 ─┼─ switch4 ─ router4 ─ router7 ─────────┘
host12 ─┘
```

**Key insight**: All attack paths converge at router8 before reaching victim!

---

## `<a name="troubleshooting"></a>`9. TROUBLESHOOTING

### Common Issues

#### Issue 1: "ModuleNotFoundError: No module named 'numpy'"

**Solution**:

```bash
pip install -r requirements.txt
```

---

#### Issue 2: "FileNotFoundError: No such file or directory: 'results/'"

**Solution**: The directory structure wasn't created.

```bash
mkdir -p data/attack_logs results/figures results/logs
python main.py
```

---

#### Issue 3: "AttributeError: 'NetworkTopology' object has no attribute '_calculate_layout'"

**Solution**: Make sure you're using the COMPLETE `network_topology.py` file I provided, not a partial version.

---

#### Issue 4: Figures don't display

**If running on a server or headless system**:

```python
# Add this at the top of visualization.py
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
```

---

#### Issue 5: "ValueError: too many values to unpack"

**Cause**: Likely a networkx version issue.

**Solution**:

```bash
pip install --upgrade networkx
```

---

### Getting Help

If you encounter issues:

1. **Check Python version**: `python --version` (must be 3.8+)
2. **Reinstall packages**: `pip install --force-reinstall -r requirements.txt`
3. **Run with verbose mode**: `python main.py --verbose`
4. **Check error message**: Read the full traceback

---

## `<a name="references"></a>`10. REFERENCES

### Academic Papers

[1] **H.-C. Lin, P. Wang, and W.-H. Lin**, "Implementation of a PSO-Based Security Defense Mechanism for Tracing the Sources of DDoS Attacks," *Computers*, vol. 8, no. 4, p. 88, Dec. 2019.
**DOI**: 10.3390/computers8040088
**Our base paper** - provides network topology, attack scenarios, PSO algorithm

[2] **K. Park and H. Lee**, "On the Effectiveness of Probabilistic Packet Marking for IP Traceback under Denial of Service Attack," *Proc. IEEE INFOCOM 2001*, Anchorage, AK, USA, Apr. 2001, pp. 338–347.
**Used for**: Probabilistic sampling theory (3% rate)

[3] **A. C. Snoeren et al.**, "Hash-Based IP Traceback," *Proc. ACM SIGCOMM 2001*, San Diego, CA, USA, Aug. 2001, pp. 3–14.
**DOI**: 10.1145/383059.383060
**Used for**: SPIE mechanism, packet logging

[4] **Y. Shi and R. Eberhart**, "A modified particle swarm optimizer," *Proc. IEEE ICEC 1998*, Anchorage, AK, USA, May 1998, pp. 69–73.
**Used for**: PSO parameters (w=0.8, c1=c2=2.0)

### Online Resources

- **NetworkX Documentation**: https://networkx.org/documentation/stable/
- **NumPy Documentation**: https://numpy.org/doc/stable/
- **Matplotlib Gallery**: https://matplotlib.org/stable/gallery/
- **Python Graph Gallery**: https://www.python-graph-gallery.com/

---

## 11. NEXT STEPS

### For Your Milestone 3 Submission

✅ **1. Run the simulation**

```bash
python main.py
```

✅ **2. Review all generated files**

- Check `results/figures/` for visualizations
- Review `results/performance_metrics.json`
- Study `results/m2_vs_m3_comparison.csv`

✅ **3. Prepare your report**
Use the template in `docs/Milestone3_Report.md`

✅ **4. Answer scribe questions**
Use the template in `docs/Milestone3_Scribe.docx`

✅ **5. Create presentation slides** (if needed)
Use figures from `results/figures/`

### Understanding for Future Milestones

This deterministic baseline (M3) sets the stage for:

**Milestone 4**: Implement PSO with randomization

- Compare PSO vs Greedy baseline
- Measure improvement
- Analyze convergence

**Milestone 5**: Full evaluation and optimization

- Multiple algorithms comparison
- Parameter tuning
- Final conclusions

---

## 12. QUICK REFERENCE COMMANDS

```bash
# Complete simulation
python main.py

# Verbose output
python main.py --verbose

# Quiet mode
python main.py --quiet

# Test individual components
python network_topology.py
python attack_simulator.py
python deterministic_traceback.py

# View results
ls -lh results/figures/
cat results/performance_metrics.json
```

---

**END OF README**

For questions or issues, please refer to the troubleshooting section or consult course TAs.
