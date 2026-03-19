# Walkthrough: Milestone 4 Folder Setup

## What Was Done

Created the complete `Milestone-4_S2_G10_NET/` folder with all code, documentation, and directory structure for the PSO-based IP Traceback system.

### Files Created

| File | Source | Purpose |
|------|--------|---------|
| [network_topology.py](file:///c:/Users/hetpa/OneDrive%20-%20Ahmedabad%20University/Desktop/Submissions%202025/SEM-4/CSE400/S2_G10/S2_G10/code/src/network_topology.py) | Copied from M3 `code/src/` | 24-node network topology (unchanged) |
| `attack_simulator.py` | From `context/m4_attack_simulator.py` | Probabilistic 3% Bernoulli sampling |
| `pso_traceback.py` | From `context/m4_pso_traceback.py` | PSO algorithm (w=0.8, c1=c2=2.0) |
| `performance_metrics.py` | New (adapted from M3) | M3 vs M4 comparison metrics |
| `visualization.py` | New (adapted from M3) | 4 M4-specific figures |
| `main.py` | New | Full M4 pipeline orchestrator |
| `requirements.txt` | Same as M3 | Dependencies |
| `README.md` | New | M4 setup/run guide |
| `docs/MILESTONE4_WORKFLOW.md` | From context | Full workflow guide |
| `docs/M4_QUICK_START.md` | From context | Quick start guide |
| `docs/Milestone4_Report.md` | New | Report template (fill after run) |

### Bug Fix

Added `sys.stdout.reconfigure(encoding='utf-8')` to `main.py`, `attack_simulator.py`, and `pso_traceback.py` to fix Windows cp1252 Unicode encoding errors with emoji/symbol characters.

## Verification

Ran `python main.py` from the `Milestone-4_S2_G10_NET/` folder — **exit code 0** ✅

### Key Results

| Metric | Value |
|--------|-------|
| Packets sampled | 58 (expected ~54) |
| Attack sources traced | 9/9 (100%) |
| Mean coverage | 66.67% |
| Avg PSO iterations | 51 |
| Memory savings | 96.8% |

### Generated Output Files

- `results/performance_metrics.json` — Full metrics JSON
- `results/m3_vs_m4_comparison.csv` — Comparison table
- `results/pso_convergence.csv` — Per-iteration convergence data
- `results/traced_paths.csv` — Traced attack paths
- `results/figures/pso_convergence.png`
- `results/figures/m3_vs_m4_accuracy.png`
- `results/figures/sampling_distribution.png`
- `results/figures/particle_evolution.png`
- `data/attack_logs/*.json` — Router sampled logs
