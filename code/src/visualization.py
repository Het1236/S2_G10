"""
visualization.py
================
Comprehensive visualization module for Milestone 3 results.

Generates:
1. Network topology with attack paths
2. Packet distribution graphs
3. Coverage percentage comparison
4. M2 vs M3 comparison plots
5. Path analysis visualizations
"""

import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
import numpy as np
import pandas as pd
from typing import Dict, List
import matplotlib.patches as mpatches

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 10)
plt.rcParams['font.size'] = 11

class ResultVisualizer:
    """
    Comprehensive visualization for Milestone 3 results.
    """
    
    def __init__(self, network, traced_paths, router_logs, metrics):
        """
        Initialize visualizer.
        
        Args:
            network: NetworkTopology object
            traced_paths: List of traced attack paths
            router_logs: Router packet logs
            metrics: Performance metrics dictionary
        """
        self.network = network
        self.traced_paths = traced_paths
        self.router_logs = router_logs
        self.metrics = metrics
        
    def create_all_visualizations(self, output_dir: str = 'results/figures'):
        """
        Generate all visualization figures.
        
        Args:
            output_dir: Directory to save figures
        """
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        print("\nGenerating visualizations...")
        
        # 1. Network with attack paths
        print("  [1/6] Network topology with traced paths...")
        self.plot_network_with_paths(f'{output_dir}/1_network_traced_paths.png')
        
        # 2. Packet distribution
        print("  [2/6] Packet distribution across routers...")
        self.plot_packet_distribution(f'{output_dir}/2_packet_distribution.png')
        
        # 3. Coverage analysis
        print("  [3/6] Coverage percentage analysis...")
        self.plot_coverage_analysis(f'{output_dir}/3_coverage_analysis.png')
        
        # 4. M2 vs M3 comparison
        print("  [4/6] Milestone 2 vs Milestone 3 comparison...")
        self.plot_m2_vs_m3_comparison(f'{output_dir}/4_m2_vs_m3_comparison.png')
        
        # 5. Path length analysis
        print("  [5/6] Path length distribution...")
        self.plot_path_analysis(f'{output_dir}/5_path_analysis.png')
        
        # 6. Summary dashboard
        print("  [6/6] Summary dashboard...")
        self.create_summary_dashboard(f'{output_dir}/6_summary_dashboard.png')
        
        print(f"\n✓ All visualizations saved to {output_dir}/")
    
    def plot_network_with_paths(self, save_path: str):
        """Plot network topology with all traced attack paths."""
        plt.figure(figsize=(18, 14))
        
        pos = self.network._calculate_layout()
        
        # Draw base network (faded)
        nx.draw_networkx_nodes(self.network.graph, pos,
                               node_size=800,
                               node_color='lightgray',
                               alpha=0.3)
        
        # Draw all edges (faded)
        nx.draw_networkx_edges(self.network.graph, pos,
                               edge_color='gray',
                               alpha=0.1,
                               arrows=True,
                               arrowsize=10)
        
        # Draw labels
        nx.draw_networkx_labels(self.network.graph, pos, 
                                font_size=9, 
                                font_weight='bold')
        
        # Draw attack paths with different colors
        colors = ['red', 'blue', 'green', 'orange', 'purple', 
                  'brown', 'pink', 'cyan', 'magenta']
        
        legend_elements = []
        
        for idx, path_info in enumerate(self.traced_paths):
            path = path_info['path']
            color = colors[idx % len(colors)]
            
            # Draw path edges
            path_edges = [(path[i], path[i+1]) for i in range(len(path)-1)]
            nx.draw_networkx_edges(self.network.graph, pos,
                                   edgelist=path_edges,
                                   edge_color=color,
                                   width=3,
                                   alpha=0.8,
                                   arrows=True,
                                   arrowsize=20)
            
            # Highlight source
            nx.draw_networkx_nodes(self.network.graph, pos,
                                   nodelist=[path[0]],
                                   node_color=color,
                                   node_size=1200,
                                   node_shape='s',
                                   edgecolors='black',
                                   linewidths=2)
            
            # Add to legend
            legend_elements.append(
                mpatches.Patch(color=color, label=f'{path[0]} → {path[-1]}')
            )
        
        # Highlight victim (star shape)
        victim_node = self.traced_paths[0]['victim'] if self.traced_paths else None
        if victim_node:
            nx.draw_networkx_nodes(self.network.graph, pos,
                                   nodelist=[victim_node],
                                   node_color='gold',
                                   node_size=2000,
                                   node_shape='*',
                                   edgecolors='red',
                                   linewidths=3)
        
        plt.title('Deterministic Traceback: All Attack Paths Reconstructed\n' + 
                  f'(Greedy Algorithm - {len(self.traced_paths)} paths found)',
                  fontsize=16, fontweight='bold', pad=20)
        plt.legend(handles=legend_elements, loc='upper left', fontsize=10)
        plt.axis('off')
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
    
    def plot_packet_distribution(self, save_path: str):
        """Plot packet distribution across routers."""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        # Get packet counts
        routers = sorted(self.router_logs.keys())
        counts = [len(self.router_logs[r]) for r in routers]
        
        # Bar plot
        bars = ax1.bar(routers, counts, color='steelblue', edgecolor='black', linewidth=1.5)
        ax1.set_xlabel('Router', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Number of Packets', fontsize=12, fontweight='bold')
        ax1.set_title('Packet Distribution Across Routers\n(Deterministic - ALL Packets Logged)',
                      fontsize=14, fontweight='bold')
        ax1.tick_params(axis='x', rotation=45)
        ax1.grid(axis='y', alpha=0.3)
        
        # Add value labels
        for bar, count in zip(bars, counts):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                     f'{int(count)}',
                     ha='center', va='bottom', fontweight='bold')
        
        # Pie chart for relative distribution
        ax2.pie(counts, labels=routers, autopct='%1.1f%%',
                startangle=90, colors=sns.color_palette("husl", len(routers)))
        ax2.set_title('Relative Packet Distribution', fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
    
    def plot_coverage_analysis(self, save_path: str):
        """Plot coverage percentage analysis."""
        if not self.traced_paths:
            return
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        # Coverage per path
        sources = [p['source'] for p in self.traced_paths]
        coverages = [p['coverage_percentage'] for p in self.traced_paths]
        
        # Bar plot
        bars = ax1.bar(range(len(sources)), coverages, 
                       color='green', alpha=0.7, edgecolor='black')
        ax1.set_xticks(range(len(sources)))
        ax1.set_xticklabels(sources, rotation=45, ha='right')
        ax1.set_xlabel('Attack Source', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Coverage %', fontsize=12, fontweight='bold')
        ax1.set_title('Coverage Percentage per Attack Path\n(Formula from Paper Eq. 3)',
                      fontsize=14, fontweight='bold')
        ax1.grid(axis='y', alpha=0.3)
        ax1.axhline(np.mean(coverages), color='red', linestyle='--', 
                    linewidth=2, label=f'Mean = {np.mean(coverages):.2f}%')
        ax1.legend()
        
        # Add value labels
        for bar, cov in zip(bars, coverages):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                     f'{cov:.1f}%',
                     ha='center', va='bottom', fontsize=9, fontweight='bold')
        
        # Distribution plot
        ax2.hist(coverages, bins=10, color='green', alpha=0.7, edgecolor='black')
        ax2.axvline(np.mean(coverages), color='red', linestyle='--', linewidth=2,
                    label=f'Mean = {np.mean(coverages):.2f}%')
        ax2.set_xlabel('Coverage %', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Frequency', fontsize=12, fontweight='bold')
        ax2.set_title('Coverage Distribution', fontsize=14, fontweight='bold')
        ax2.legend()
        ax2.grid(alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
    
    def plot_m2_vs_m3_comparison(self, save_path: str):
        """Plot comparison between Milestone 2 predictions and Milestone 3 results."""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        
        # Get data
        m2_comp = self.metrics['m2_comparison']
        m2_model = m2_comp['milestone2_model']
        m3_actual = m2_comp['milestone3_actual']
        
        # 1. Packet usage comparison
        categories = ['M2 Predicted\n(with 3% sampling)', 'M3 Actual\n(no sampling)']
        values = [m2_model['expected_packets_with_sampling'], 
                  m3_actual['total_packets_logged']]
        colors_bar = ['#FF6B6B', '#4ECDC4']
        
        bars = ax1.bar(categories, values, color=colors_bar, edgecolor='black', linewidth=2)
        ax1.set_ylabel('Number of Packets', fontsize=12, fontweight='bold')
        ax1.set_title('Packet Usage: M2 (Probabilistic) vs M3 (Deterministic)',
                      fontsize=14, fontweight='bold')
        ax1.grid(axis='y', alpha=0.3)
        
        for bar, val in zip(bars, values):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                     f'{int(val)}',
                     ha='center', va='bottom', fontsize=12, fontweight='bold')
        
        # 2. Binomial distribution from M2 with M3 point
        k_values = np.arange(30, 81)
        from scipy.stats import binom
        pmf = binom.pmf(k_values, 1800, 0.03)
        
        ax2.bar(k_values, pmf, alpha=0.6, color='steelblue', label='M2: Binomial(1800, 0.03)')
        ax2.axvline(m2_model['expected_packets_with_sampling'], 
                    color='red', linestyle='--', linewidth=2, label='M2: E[N] = 54')
        ax2.axvline(m2_model['ci_95'][0], color='orange', linestyle=':', linewidth=2)
        ax2.axvline(m2_model['ci_95'][1], color='orange', linestyle=':', linewidth=2,
                    label='M2: 95% CI')
        ax2.set_xlabel('Number of Packets (with sampling)', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Probability', fontsize=12, fontweight='bold')
        ax2.set_title('M2 Probabilistic Model: Binomial Distribution',
                      fontsize=14, fontweight='bold')
        ax2.legend()
        ax2.grid(alpha=0.3)
        
        # 3. Sampling rate comparison
        sampling_rates = ['M2\n(3% sampling)', 'M3\n(100% - no sampling)']
        rates = [m2_model['sampling_rate'] * 100, 100]
        
        bars = ax3.bar(sampling_rates, rates, color=['#FF6B6B', '#4ECDC4'],
                       edgecolor='black', linewidth=2)
        ax3.set_ylabel('Sampling Rate (%)', fontsize=12, fontweight='bold')
        ax3.set_title('Sampling Rate Comparison', fontsize=14, fontweight='bold')
        ax3.set_ylim([0, 110])
        ax3.grid(axis='y', alpha=0.3)
        
        for bar, rate in zip(bars, rates):
            height = bar.get_height()
            ax3.text(bar.get_x() + bar.get_width()/2., height,
                     f'{rate:.0f}%',
                     ha='center', va='bottom', fontsize=12, fontweight='bold')
        
        # 4. Summary table
        ax4.axis('off')
        table_data = [
            ['Metric', 'Milestone 2', 'Milestone 3'],
            ['Approach', 'Probabilistic', 'Deterministic'],
            ['Sampling Rate', '3%', '100%'],
            ['Expected Packets', '54 ± 7.24', f'{m3_actual["total_packets_logged"]}'],
            ['Randomness', 'Yes (Binomial)', 'No'],
            ['Accuracy', 'Variable', '100% (baseline)'],
            ['Paths Found', 'Stochastic', f'{m3_actual["paths_found"]}']
        ]
        
        table = ax4.table(cellText=table_data, cellLoc='center', loc='center',
                          colWidths=[0.3, 0.35, 0.35])
        table.auto_set_font_size(False)
        table.set_fontsize(11)
        table.scale(1, 2.5)
        
        # Style header row
        for i in range(3):
            table[(0, i)].set_facecolor('#4ECDC4')
            table[(0, i)].set_text_props(weight='bold', color='white')
        
        # Alternate row colors
        for i in range(1, len(table_data)):
            for j in range(3):
                if i % 2 == 0:
                    table[(i, j)].set_facecolor('#F0F0F0')
        
        ax4.set_title('Milestone 2 vs Milestone 3: Comparison Summary',
                      fontsize=14, fontweight='bold', pad=20)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
    
    def plot_path_analysis(self, save_path: str):
        """Plot path length and quality analysis."""
        if not self.traced_paths:
            return
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        # Path length distribution
        path_lengths = [p['path_length'] for p in self.traced_paths]
        sources = [p['source'] for p in self.traced_paths]
        
        bars = ax1.bar(range(len(sources)), path_lengths,
                       color='purple', alpha=0.7, edgecolor='black')
        ax1.set_xticks(range(len(sources)))
        ax1.set_xticklabels(sources, rotation=45, ha='right')
        ax1.set_xlabel('Attack Source', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Path Length (hops)', fontsize=12, fontweight='bold')
        ax1.set_title('Path Length per Attack Source', fontsize=14, fontweight='bold')
        ax1.axhline(np.mean(path_lengths), color='red', linestyle='--',
                    linewidth=2, label=f'Mean = {np.mean(path_lengths):.2f} hops')
        ax1.legend()
        ax1.grid(axis='y', alpha=0.3)
        
        # Add value labels
        for bar, length in zip(bars, path_lengths):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                     f'{int(length)}',
                     ha='center', va='bottom', fontsize=9, fontweight='bold')
        
        # Path length histogram
        ax2.hist(path_lengths, bins=max(path_lengths)-min(path_lengths)+1,
                 color='purple', alpha=0.7, edgecolor='black')
        ax2.set_xlabel('Path Length (hops)', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Frequency', fontsize=12, fontweight='bold')
        ax2.set_title('Path Length Distribution', fontsize=14, fontweight='bold')
        ax2.grid(alpha=0.3)
        
        # Add statistics text
        stats_text = f'Mean: {np.mean(path_lengths):.2f}\n'
        stats_text += f'Std: {np.std(path_lengths):.2f}\n'
        stats_text += f'Min: {np.min(path_lengths)}\n'
        stats_text += f'Max: {np.max(path_lengths)}'
        ax2.text(0.95, 0.95, stats_text, transform=ax2.transAxes,
                 verticalalignment='top', horizontalalignment='right',
                 bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5),
                 fontsize=10)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
    
    def create_summary_dashboard(self, save_path: str):
        """Create a comprehensive summary dashboard."""
        fig = plt.figure(figsize=(20, 12))
        gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
        
        # Title
        fig.suptitle('MILESTONE 3: DETERMINISTIC BASELINE - SUMMARY DASHBOARD',
                     fontsize=18, fontweight='bold', y=0.98)
        
        # 1. Key metrics (top left)
        ax1 = fig.add_subplot(gs[0, 0])
        ax1.axis('off')
        
        acc = self.metrics['accuracy']
        cov = self.metrics['coverage']
        pkt = self.metrics['packet_usage']
        
        metrics_text = f"""
KEY METRICS

Traceback Accuracy:
  • Paths Found: {acc['total_paths_found']}
  • Accuracy: {acc['accuracy_percentage']:.1f}%
  
Coverage:
  • Mean: {cov['mean_coverage']:.2f}%
  • Range: [{cov['min_coverage']:.2f}%, {cov['max_coverage']:.2f}%]
  
Packet Usage:
  • Total Logged: {pkt['total_packets_logged']}
  • Avg per Path: {pkt['packets_per_path_mean']:.0f}
        """
        
        ax1.text(0.1, 0.9, metrics_text, transform=ax1.transAxes,
                 verticalalignment='top', fontsize=11, family='monospace',
                 bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
        
        # 2. Network topology (top middle and right)
        ax2 = fig.add_subplot(gs[0, 1:])
        pos = self.network._calculate_layout()
        nx.draw(self.network.graph, pos, ax=ax2,
                node_size=300, font_size=7, with_labels=True,
                node_color='lightblue', edge_color='gray', alpha=0.6)
        ax2.set_title('Network Topology Overview', fontweight='bold')
        
        # 3. Packet distribution (middle left)
        ax3 = fig.add_subplot(gs[1, 0])
        routers = sorted(self.router_logs.keys())
        counts = [len(self.router_logs[r]) for r in routers]
        ax3.bar(routers, counts, color='steelblue', edgecolor='black')
        ax3.set_title('Packet Distribution', fontweight='bold')
        ax3.set_xlabel('Router', fontsize=9)
        ax3.set_ylabel('Packets', fontsize=9)
        ax3.tick_params(axis='x', rotation=45, labelsize=8)
        ax3.grid(axis='y', alpha=0.3)
        
        # 4. Coverage (middle center)
        ax4 = fig.add_subplot(gs[1, 1])
        if self.traced_paths:
            coverages = [p['coverage_percentage'] for p in self.traced_paths]
            ax4.hist(coverages, bins=8, color='green', alpha=0.7, edgecolor='black')
            ax4.axvline(np.mean(coverages), color='red', linestyle='--', linewidth=2)
            ax4.set_title('Coverage Distribution', fontweight='bold')
            ax4.set_xlabel('Coverage %', fontsize=9)
            ax4.set_ylabel('Frequency', fontsize=9)
            ax4.grid(alpha=0.3)
        
        # 5. Path lengths (middle right)
        ax5 = fig.add_subplot(gs[1, 2])
        if self.traced_paths:
            path_lengths = [p['path_length'] for p in self.traced_paths]
            ax5.hist(path_lengths, bins=max(path_lengths)-min(path_lengths)+1,
                     color='purple', alpha=0.7, edgecolor='black')
            ax5.set_title('Path Lengths', fontweight='bold')
            ax5.set_xlabel('Hops', fontsize=9)
            ax5.set_ylabel('Frequency', fontsize=9)
            ax5.grid(alpha=0.3)
        
        # 6. M2 vs M3 comparison (bottom)
        ax6 = fig.add_subplot(gs[2, :])
        m2_comp = self.metrics['m2_comparison']
        
        comparison_data = [
            ['', 'Milestone 2 (Probabilistic)', 'Milestone 3 (Deterministic)'],
            ['Packets Used', 
             f"{m2_comp['milestone2_model']['expected_packets_with_sampling']} (with 3% sampling)",
             f"{m2_comp['milestone3_actual']['total_packets_logged']} (no sampling)"],
            ['Sampling Rate', 
             f"{m2_comp['milestone2_model']['sampling_rate']*100:.0f}%",
             f"{m2_comp['milestone3_actual']['sampling_rate']*100:.0f}%"],
            ['Nature', 'Stochastic (random)', 'Deterministic (fixed)'],
            ['Paths Found', 'Variable', f"{m2_comp['milestone3_actual']['paths_found']}"],
            ['Accuracy', 'Depends on samples', '100% (baseline)']
        ]
        
        table = ax6.table(cellText=comparison_data, cellLoc='center', loc='center',
                          colWidths=[0.2, 0.4, 0.4])
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1, 2)
        
        for i in range(3):
            table[(0, i)].set_facecolor('#4ECDC4')
            table[(0, i)].set_text_props(weight='bold', color='white')
        
        for i in range(1, len(comparison_data)):
            for j in range(3):
                if i % 2 == 0:
                    table[(i, j)].set_facecolor('#F0F0F0')
        
        ax6.axis('off')
        ax6.set_title('Milestone Comparison', fontweight='bold', pad=20, fontsize=12)
        
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()


# Example usage
if __name__ == "__main__":
    import os
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Create output directories
    os.makedirs(os.path.join(PROJECT_ROOT, 'results', 'figures'), exist_ok=True)
    
    from network_topology import NetworkTopology
    from attack_simulator import DeterministicAttackSimulator
    from deterministic_traceback import GreedyTraceback
    from performance_metrics import PerformanceEvaluator
    
    # Run complete pipeline
    network = NetworkTopology()
    network.create_topology()
    
    simulator = DeterministicAttackSimulator(network)
    simulator.run_attack()
    
    traceback = GreedyTraceback(network, simulator.router_logs)
    paths = traceback.trace_all_attacks()
    
    evaluator = PerformanceEvaluator(paths, simulator.router_logs)
    metrics = evaluator.evaluate_all_metrics()
    
    # Create visualizations
    visualizer = ResultVisualizer(network, paths, simulator.router_logs, metrics)
    visualizer.create_all_visualizations(os.path.join(PROJECT_ROOT, 'results', 'figures'))