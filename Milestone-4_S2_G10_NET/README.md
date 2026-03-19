# Milestone 4: PSO-Based IP Traceback with Probabilistic Sampling

## CSE 400: Fundamentals of Probability in Computing — Group 10

---

## 🎯 Overview

**Milestone 4** transforms the deterministic baseline (M3) into a **realistic probabilistic system** using:

1. **Probabilistic Packet Sampling (3%)** — `S ~ Bernoulli(p=0.03)` instead of logging all packets
2. **PSO Algorithm** — Particle Swarm Optimization for intelligent path search instead of greedy shortest path

### M3 → M4 Key Differences

| Aspect | M3 (Deterministic) | M4 (Probabilistic) |
|--------|-------------------|-------------------|
| Sampling | 100% (all 1800) | 3% (~54 packets) |
| Algorithm | Greedy (Dijkstra) | PSO (swarm intelligence) |
| Accuracy | 100% (perfect) | 95-98% (realistic) |
| Variance | σ = 0 | σ > 0 (stochastic) |
| Memory | Baseline | 97% savings |

---

## 📁 Folder Structure

```
Milestone-4_S2_G10_NET/
├── network_topology.py          # ✅ Reused from M3
├── attack_simulator.py          # 🔄 Probabilistic 3% sampling
├── pso_traceback.py             # ⭐ NEW — PSO algorithm
├── performance_metrics.py       # 🔄 M3 vs M4 comparison
├── visualization.py             # 🔄 PSO convergence plots
├── main.py                      # 🔄 M4 orchestrator
├── requirements.txt             # ✅ Same as M3
├── README.md                    # This file
├── data/
│   ├── network_config.json
│   └── attack_logs/
├── results/
│   ├── figures/
│   │   ├── pso_convergence.png
│   │   ├── m3_vs_m4_accuracy.png
│   │   ├── sampling_distribution.png
│   │   └── particle_evolution.png
│   ├── pso_convergence.csv
│   ├── m3_vs_m4_comparison.csv
│   ├── performance_metrics.json
│   └── traced_paths.csv
└── docs/
    ├── Milestone4_Report.md
    ├── MILESTONE4_WORKFLOW.md
    └── M4_QUICK_START.md
```

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run M4

```bash
python main.py
```

### 3. Check Results

```bash
# View metrics
cat results/performance_metrics.json

# View figures
start results/figures/pso_convergence.png
start results/figures/m3_vs_m4_accuracy.png
```

---

## 📊 Expected Output

```
══════════════════════════════════════════════════════════════════
 MILESTONE 4: PSO-BASED IP TRACEBACK WITH 3% SAMPLING
══════════════════════════════════════════════════════════════════

[1/5] Creating Network Topology...
  ✓ 24 nodes created

[2/5] Simulating DDoS Attack (Probabilistic 3% Sampling)...
  ✓ Sampled 52/1800 packets

[3/5] PSO-Based Traceback...
  ✓ 9/9 sources traced
  ✓ Average accuracy: ~96%

[4/5] Evaluating Performance (M3 vs M4)...
  ✓ Memory savings: 97%

[5/5] Generating Visualizations...
  ✓ 4 figures saved

══════════════════════════════════════════════════════════════════
 M4 SIMULATION COMPLETE!
══════════════════════════════════════════════════════════════════
```

---

## 📚 References

- **Paper**: Lin, H.C., Wang, P., Lin, W.H. (2019). *Implementation of a PSO-Based Security Defense Mechanism for Tracing the Sources of DDoS Attacks.* Computers, 8(4), 88.
- **PSO Videos**: [Visualization](https://www.youtube.com/watch?v=JhgDMAm-imI) | [Implementation](https://www.youtube.com/watch?v=vhSBqk6SAB4)

---

## 📖 Documentation

- **Full Workflow**: See `docs/MILESTONE4_WORKFLOW.md`
- **Quick Start**: See `docs/M4_QUICK_START.md`
- **Report**: See `docs/Milestone4_Report.md`
