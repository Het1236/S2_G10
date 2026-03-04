"""
main.py
=======
Main execution script for Milestone 3: Deterministic Baseline Simulation.

This script orchestrates the entire simulation pipeline:
1. Create network topology
2. Simulate DDoS attack (deterministic)
3. Execute greedy traceback algorithm
4. Evaluate performance
5. Generate visualizations
6. Create reports

Usage:
    python main.py
"""

import os
import sys
from datetime import datetime
import argparse

# Project root directory (where main.py lives)
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Add src/ to Python path so we can import our modules
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'src'))

# Import our modules
from network_topology import NetworkTopology
from attack_simulator import DeterministicAttackSimulator
from deterministic_traceback import GreedyTraceback
from performance_metrics import PerformanceEvaluator
from visualization import ResultVisualizer

def setup_directories():
    """Create necessary directories for output."""
    directories = [
        os.path.join(PROJECT_ROOT, 'data'),
        os.path.join(PROJECT_ROOT, 'data', 'attack_logs'),
        os.path.join(PROJECT_ROOT, 'results'),
        os.path.join(PROJECT_ROOT, 'results', 'figures'),
        os.path.join(PROJECT_ROOT, 'results', 'logs')
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    
    print("✓ Directories set up")

def print_banner():
    """Print welcome banner."""
    print("\n" + "="*80)
    print(" "*20 + "MILESTONE 3: DETERMINISTIC BASELINE SIMULATION")
    print(" "*25 + "PSO-Based IP Traceback for DDoS Attacks")
    print("="*80)
    print("\nCSE 400: Fundamentals of Probability in Computing")
    print("Group 10")
    print(f"Execution Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n" + "="*80 + "\n")

def run_simulation(verbose=True):
    """
    Run the complete deterministic baseline simulation.
    
    Args:
        verbose: Print detailed progress information
        
    Returns:
        Dictionary with all results
    """
    results = {}
    
    # STEP 1: Create Network Topology
    if verbose:
        print("\n" + "─"*80)
        print("STEP 1: CREATING NETWORK TOPOLOGY")
        print("─"*80)
    
    network = NetworkTopology()
    network.create_topology()
    network.save_topology(os.path.join(PROJECT_ROOT, 'data', 'network_config.json'))
    
    if verbose:
        print(f"✓ Network created: {network.graph.number_of_nodes()} nodes, "
              f"{network.graph.number_of_edges()} edges")
        print(f"  Attack sources: {len(network.attack_sources)}")
        print(f"  Victim: {network.victim}")
    
    results['network'] = network
    
    # STEP 2: Simulate DDoS Attack (Deterministic)
    if verbose:
        print("\n" + "─"*80)
        print("STEP 2: SIMULATING DDOS ATTACK (DETERMINISTIC)")
        print("─"*80)
        print("NOTE: This is deterministic - we log ALL packets (not 3% sample)")
    
    simulator = DeterministicAttackSimulator(network)
    packet_df = simulator.run_attack()
    simulator.save_logs(os.path.join(PROJECT_ROOT, 'data', 'attack_logs', 'packet_logs.csv'))
    
    results['simulator'] = simulator
    results['packet_df'] = packet_df
    
    # STEP 3: Execute Greedy Traceback
    if verbose:
        print("\n" + "─"*80)
        print("STEP 3: EXECUTING DETERMINISTIC GREEDY TRACEBACK")
        print("─"*80)
        print("Algorithm: Always choose neighbor with MOST packets")
    
    traceback = GreedyTraceback(network, simulator.router_logs)
    paths = traceback.trace_all_attacks()
    
    results['traceback'] = traceback
    results['paths'] = paths
    
    # Generate traceback report
    report_df = traceback.generate_report()
    report_df.to_csv(os.path.join(PROJECT_ROOT, 'results', 'traceback_report.csv'), index=False)
    
    if verbose:
        print("\n✓ Traceback Report:")
        print(report_df.to_string(index=False))
    
    # STEP 4: Evaluate Performance
    if verbose:
        print("\n" + "─"*80)
        print("STEP 4: EVALUATING PERFORMANCE")
        print("─"*80)
    
    evaluator = PerformanceEvaluator(paths, simulator.router_logs)
    metrics = evaluator.evaluate_all_metrics()
    evaluator.save_metrics(os.path.join(PROJECT_ROOT, 'results', 'performance_metrics.json'))
    
    results['evaluator'] = evaluator
    results['metrics'] = metrics
    
    # Print summary
    evaluator.print_summary()
    
    # Generate comparison table
    comparison_df = evaluator.generate_comparison_table()
    comparison_df.to_csv(os.path.join(PROJECT_ROOT, 'results', 'm2_vs_m3_comparison.csv'), index=False)
    
    if verbose:
        print("\n✓ M2 vs M3 Comparison:")
        print(comparison_df.to_string(index=False))
    
    # STEP 5: Generate Visualizations
    if verbose:
        print("\n" + "─"*80)
        print("STEP 5: GENERATING VISUALIZATIONS")
        print("─"*80)
    
    visualizer = ResultVisualizer(network, paths, simulator.router_logs, metrics)
    visualizer.create_all_visualizations(os.path.join(PROJECT_ROOT, 'results', 'figures'))
    
    results['visualizer'] = visualizer
    
    return results

def print_final_summary(results):
    """Print final summary of the simulation."""
    print("\n" + "="*80)
    print(" "*25 + "SIMULATION COMPLETE!")
    print("="*80)
    
    print("\n📁 OUTPUT FILES:")
    print("─"*80)
    print("  Data:")
    print("    • data/network_config.json - Network topology configuration")
    print("    • data/attack_logs/packet_logs.csv - All packet logs")
    print("\n  Results:")
    print("    • results/traceback_report.csv - Detailed traceback report")
    print("    • results/performance_metrics.json - All performance metrics")
    print("    • results/m2_vs_m3_comparison.csv - Milestone comparison")
    print("\n  Figures:")
    print("    • results/figures/1_network_traced_paths.png")
    print("    • results/figures/2_packet_distribution.png")
    print("    • results/figures/3_coverage_analysis.png")
    print("    • results/figures/4_m2_vs_m3_comparison.png")
    print("    • results/figures/5_path_analysis.png")
    print("    • results/figures/6_summary_dashboard.png")
    
    print("\n📊 KEY RESULTS:")
    print("─"*80)
    metrics = results['metrics']
    print(f"  • Paths Found: {metrics['accuracy']['total_paths_found']}")
    print(f"  • Accuracy: {metrics['accuracy']['accuracy_percentage']:.1f}%")
    print(f"  • Mean Coverage: {metrics['coverage']['mean_coverage']:.2f}%")
    print(f"  • Total Packets: {metrics['packet_usage']['total_packets_logged']}")
    
    print("\n" + "="*80)
    print("Next Steps:")
    print("  1. Review generated visualizations in results/figures/")
    print("  2. Check performance metrics in results/performance_metrics.json")
    print("  3. Compare M2 vs M3 results in results/m2_vs_m3_comparison.csv")
    print("  4. Prepare Milestone 3 report and scribe answers")
    print("="*80 + "\n")

def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(
        description='Milestone 3: Deterministic Baseline Simulation for IP Traceback'
    )
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Print detailed progress information')
    parser.add_argument('--quiet', '-q', action='store_true',
                        help='Suppress most output')
    
    args = parser.parse_args()
    
    verbose = args.verbose or not args.quiet
    
    if verbose:
        print_banner()
    
    # Setup
    setup_directories()
    
    # Run simulation
    try:
        results = run_simulation(verbose=verbose)
        
        if verbose:
            print_final_summary(results)
        
        print("\n✅ Simulation completed successfully!\n")
        return 0
        
    except Exception as e:
        print(f"\n❌ Error during simulation: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())