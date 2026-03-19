"""
main.py
=======
Main execution script for Milestone 4: PSO-Based IP Traceback with 3% Sampling.

This script orchestrates the entire M4 pipeline:
1. Create network topology (reuse from M3)
2. Simulate DDoS attack with probabilistic sampling (3%)
3. Execute PSO-based traceback algorithm
4. Evaluate performance (M3 vs M4 comparison)
5. Generate visualizations (convergence, accuracy, sampling, evolution)
6. Save all results

Usage:
    python main.py
    python main.py --verbose
"""

import os
import sys
from datetime import datetime
import argparse

# Fix Windows terminal encoding for Unicode characters
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

# Project root directory (where main.py lives)
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Add current directory to Python path
sys.path.insert(0, PROJECT_ROOT)

# Import M4 components
from network_topology import NetworkTopology
from attack_simulator import ProbabilisticAttackSimulator
from pso_traceback import PSOTraceback
from performance_metrics import PerformanceEvaluator
from visualization import M4Visualizer


def setup_directories():
    """Create necessary directories for output."""
    directories = [
        os.path.join(PROJECT_ROOT, 'data'),
        os.path.join(PROJECT_ROOT, 'data', 'attack_logs'),
        os.path.join(PROJECT_ROOT, 'results'),
        os.path.join(PROJECT_ROOT, 'results', 'figures'),
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    
    print("✓ Directories set up")


def print_banner():
    """Print welcome banner."""
    print("\n" + "=" * 70)
    print(" " * 5 + "MILESTONE 4: PSO-BASED IP TRACEBACK WITH 3% SAMPLING")
    print(" " * 10 + "Based on Lin et al. (2019) - Computers 8(4) 88")
    print("=" * 70)
    print("\nCSE 400: Fundamentals of Probability in Computing")
    print("Group 10")
    print(f"Execution Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n" + "=" * 70 + "\n")


def run_simulation(verbose=True):
    """
    Run the complete M4 PSO-based traceback simulation.
    
    Args:
        verbose: Print detailed progress information
        
    Returns:
        Dictionary with all results
    """
    results = {}
    
    # ──────────────────────────────────────────────────────────────────
    # STEP 1: Create Network Topology (reuse from M3)
    # ──────────────────────────────────────────────────────────────────
    if verbose:
        print("\n" + "─" * 70)
        print("[1/5] CREATING NETWORK TOPOLOGY")
        print("─" * 70)
    
    network = NetworkTopology()
    network.create_topology()
    network.save_topology(os.path.join(PROJECT_ROOT, 'data', 'network_config.json'))
    
    attack_sources = network.attack_sources
    victim = network.victim
    
    if verbose:
        print(f"✓ Network created: {network.graph.number_of_nodes()} nodes, "
              f"{network.graph.number_of_edges()} edges")
        print(f"  Attack sources: {len(attack_sources)} → {attack_sources}")
        print(f"  Victim: {victim}")
    
    results['network'] = network
    
    # ──────────────────────────────────────────────────────────────────
    # STEP 2: Simulate DDoS Attack with Probabilistic Sampling
    # ──────────────────────────────────────────────────────────────────
    if verbose:
        print("\n" + "─" * 70)
        print("[2/5] SIMULATING DDOS ATTACK (PROBABILISTIC 3% SAMPLING)")
        print("─" * 70)
        print("NOTE: S ~ Bernoulli(p=0.03) for each packet")
        print("NOTE: Expected sampled packets: E[N] = 54 ± 7.24")
    
    simulator = ProbabilisticAttackSimulator(
        network_graph=network.graph,
        sampling_probability=0.03
    )
    attack_stats = simulator.simulate_ddos_attack(
        attack_sources=attack_sources,
        victim=victim,
        packets_per_source=200
    )
    
    # Save attack logs
    simulator.save_attack_logs(os.path.join(PROJECT_ROOT, 'data', 'attack_logs'))
    
    # Get sampling statistics
    sampling_stats = simulator.get_sampling_statistics()
    
    if verbose:
        print(f"\n  Sampling Statistics:")
        print(f"    Expected N:  {sampling_stats['expected_samples']:.1f}")
        print(f"    Actual N:    {sampling_stats['sampled_packets']}")
        print(f"    Variance:    {sampling_stats['variance']:.2f}")
        print(f"    Std Dev:     {sampling_stats['std_dev']:.2f}")
        print(f"    95% CI:      [{sampling_stats['ci_95'][0]:.1f}, "
              f"{sampling_stats['ci_95'][1]:.1f}]")
        print(f"    Within CI:   {'✓ Yes' if sampling_stats['within_ci'] else '✗ No'}")
    
    results['simulator'] = simulator
    results['attack_stats'] = attack_stats
    results['sampling_stats'] = sampling_stats
    
    # Get router packet counts for PSO
    router_counts = simulator.get_all_router_counts()
    total_sampled = attack_stats['sampled_packets']
    
    # ──────────────────────────────────────────────────────────────────
    # STEP 3: PSO-Based Traceback
    # ──────────────────────────────────────────────────────────────────
    if verbose:
        print("\n" + "─" * 70)
        print("[3/5] PSO-BASED IP TRACEBACK")
        print("─" * 70)
        print("Parameters: w=0.8, c1=2.0, c2=2.0 (from paper Section 3.2)")
        print(f"Swarm size: 30 particles, Max iterations: 500")
    
    pso = PSOTraceback(
        network_graph=network.graph,
        router_packet_counts=router_counts,
        total_sampled_packets=total_sampled,
        w=0.8,
        c1=2.0,
        c2=2.0,
        max_iterations=500,
        num_particles=30
    )
    
    pso_results = pso.trace_all_attacks(
        suspected_sources=attack_sources,
        victim=victim,
        verbose=verbose
    )
    
    results['pso'] = pso
    results['pso_results'] = pso_results
    
    # ──────────────────────────────────────────────────────────────────
    # STEP 4: Evaluate Performance (M3 vs M4 Comparison)
    # ──────────────────────────────────────────────────────────────────
    if verbose:
        print("\n" + "─" * 70)
        print("[4/5] EVALUATING PERFORMANCE (M3 vs M4)")
        print("─" * 70)
    
    evaluator = PerformanceEvaluator()
    m4_metrics = evaluator.evaluate_m4_results(pso_results, attack_stats, attack_sources)
    comparison = evaluator.compare_m3_vs_m4(m4_metrics)
    
    # Print summary
    evaluator.print_summary(m4_metrics, comparison)
    
    # Save metrics
    evaluator.save_metrics(
        m4_metrics, comparison,
        os.path.join(PROJECT_ROOT, 'results', 'performance_metrics.json')
    )
    
    # Generate comparison table
    comparison_df = evaluator.generate_comparison_table(m4_metrics)
    comparison_df.to_csv(
        os.path.join(PROJECT_ROOT, 'results', 'm3_vs_m4_comparison.csv'),
        index=False
    )
    
    if verbose:
        print("\n✓ M3 vs M4 Comparison Table:")
        print(comparison_df.to_string(index=False))
    
    results['evaluator'] = evaluator
    results['m4_metrics'] = m4_metrics
    results['comparison'] = comparison
    
    # ──────────────────────────────────────────────────────────────────
    # STEP 5: Generate Visualizations
    # ──────────────────────────────────────────────────────────────────
    if verbose:
        print("\n" + "─" * 70)
        print("[5/5] GENERATING VISUALIZATIONS")
        print("─" * 70)
    
    visualizer = M4Visualizer(pso_results, m4_metrics, comparison, attack_stats)
    visualizer.create_all_visualizations(
        os.path.join(PROJECT_ROOT, 'results', 'figures')
    )
    
    # Save convergence data
    visualizer.save_convergence_csv(
        os.path.join(PROJECT_ROOT, 'results', 'pso_convergence.csv')
    )
    
    # Save traced paths
    visualizer.save_traced_paths_csv(
        os.path.join(PROJECT_ROOT, 'results', 'traced_paths.csv')
    )
    
    results['visualizer'] = visualizer
    
    return results


def print_final_summary(results):
    """Print final summary of the simulation."""
    print("\n" + "=" * 70)
    print(" " * 20 + "M4 SIMULATION COMPLETE!")
    print("=" * 70)
    
    print("\n📁 OUTPUT FILES:")
    print("─" * 70)
    print("  Data:")
    print("    • data/network_config.json")
    print("    • data/attack_logs/*.json")
    print("\n  Results:")
    print("    • results/performance_metrics.json")
    print("    • results/m3_vs_m4_comparison.csv")
    print("    • results/pso_convergence.csv")
    print("    • results/traced_paths.csv")
    print("\n  Figures:")
    print("    • results/figures/pso_convergence.png")
    print("    • results/figures/m3_vs_m4_accuracy.png")
    print("    • results/figures/sampling_distribution.png")
    print("    • results/figures/particle_evolution.png")
    
    m4 = results['m4_metrics']
    print("\n📊 KEY RESULTS:")
    print("─" * 70)
    print(f"  • Attack sources: {m4['accuracy']['total_sources']}")
    print(f"  • Packets sampled: {m4['sampling']['sampled_packets']} "
          f"(expected ~54)")
    print(f"  • Successfully traced: {m4['accuracy']['successfully_traced']}/"
          f"{m4['accuracy']['total_sources']}")
    print(f"  • Accuracy: {m4['accuracy']['accuracy_percentage']:.1f}%")
    print(f"  • Mean coverage: {m4['coverage']['mean_coverage']:.2f}%")
    print(f"  • Avg iterations: {m4['convergence']['mean_iterations']:.0f}")
    print(f"  • Memory savings: {m4['memory']['memory_savings_percent']:.1f}%")
    
    print("\n" + "=" * 70)
    print("Next Steps:")
    print("  1. Review visualizations in results/figures/")
    print("  2. Check performance_metrics.json for detailed metrics")
    print("  3. Update Milestone4_Report.md in docs/")
    print("  4. Prepare M4 presentation")
    print("=" * 70 + "\n")


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(
        description='Milestone 4: PSO-Based IP Traceback with 3% Sampling'
    )
    parser.add_argument('--verbose', '-v', action='store_true', default=True,
                        help='Print detailed progress information')
    parser.add_argument('--quiet', '-q', action='store_true',
                        help='Suppress most output')
    
    args = parser.parse_args()
    verbose = not args.quiet
    
    if verbose:
        print_banner()
    
    # Setup
    setup_directories()
    
    # Run simulation
    try:
        results = run_simulation(verbose=verbose)
        
        if verbose:
            print_final_summary(results)
        
        print("\n✅ Milestone 4 simulation completed successfully!\n")
        return 0
        
    except Exception as e:
        print(f"\n❌ Error during simulation: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
