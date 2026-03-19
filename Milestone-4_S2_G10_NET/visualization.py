"""
visualization.py
================
Visualization module for Milestone 4 PSO-based IP Traceback results.

Generates:
1. PSO convergence plot
2. M3 vs M4 accuracy comparison
3. Sampling distribution histogram
4. Particle evolution visualization
"""

import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for saving figures
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from typing import Dict, List
import os

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 10)
plt.rcParams['font.size'] = 11


class M4Visualizer:
    """
    Visualization suite for Milestone 4 PSO traceback results.
    
    Generates 4 key figures:
    1. PSO convergence curve
    2. M3 vs M4 accuracy comparison
    3. Sampling distribution
    4. Particle evolution / coverage comparison
    """
    
    def __init__(self, pso_results: List[Dict], m4_metrics: Dict,
                 comparison: Dict, attack_stats: Dict):
        """
        Initialize visualizer.
        
        Args:
            pso_results: List of PSO trace results
            m4_metrics: M4 performance metrics
            comparison: M3 vs M4 comparison dict
            attack_stats: Attack simulation statistics
        """
        self.pso_results = pso_results
        self.m4_metrics = m4_metrics
        self.comparison = comparison
        self.attack_stats = attack_stats
    
    def create_all_visualizations(self, output_dir: str = 'results/figures'):
        """Generate all M4 visualization figures."""
        os.makedirs(output_dir, exist_ok=True)
        
        print("\nGenerating M4 visualizations...")
        
        print("  [1/4] PSO convergence plot...")
        self.plot_pso_convergence(os.path.join(output_dir, 'pso_convergence.png'))
        
        print("  [2/4] M3 vs M4 accuracy comparison...")
        self.plot_m3_vs_m4_accuracy(os.path.join(output_dir, 'm3_vs_m4_accuracy.png'))
        
        print("  [3/4] Sampling distribution...")
        self.plot_sampling_distribution(os.path.join(output_dir, 'sampling_distribution.png'))
        
        print("  [4/4] Particle evolution / coverage comparison...")
        self.plot_particle_evolution(os.path.join(output_dir, 'particle_evolution.png'))
        
        print(f"\n✅ All M4 visualizations saved to {output_dir}/")
    
    def plot_pso_convergence(self, save_path: str):
        """
        Plot PSO convergence curve for all attack sources.
        
        Shows how fitness (coverage %) improves over iterations.
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        colors = ['red', 'blue', 'green', 'orange', 'purple',
                  'brown', 'pink', 'cyan', 'magenta']
        
        # Plot convergence for each source
        for idx, result in enumerate(self.pso_results):
            if 'convergence_history' in result and result['convergence_history']:
                history = result['convergence_history']
                iterations = [h['iteration'] for h in history]
                best_fitness = [h['best_fitness'] for h in history]
                
                color = colors[idx % len(colors)]
                ax1.plot(iterations, best_fitness, color=color, alpha=0.7,
                        linewidth=1.5, label=result['source'])
        
        ax1.set_xlabel('PSO Iteration', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Best Fitness (Coverage %)', fontsize=12, fontweight='bold')
        ax1.set_title('PSO Convergence: Fitness vs Iteration\n(Per Attack Source)',
                      fontsize=14, fontweight='bold')
        ax1.legend(fontsize=8, loc='lower right')
        ax1.grid(alpha=0.3)
        
        # Summary convergence statistics
        iterations_list = [r['iterations'] for r in self.pso_results]
        coverages = [r['coverage'] for r in self.pso_results]
        sources = [r['source'] for r in self.pso_results]
        
        bars = ax2.bar(range(len(sources)), iterations_list,
                       color='steelblue', edgecolor='black', alpha=0.8)
        ax2.set_xticks(range(len(sources)))
        ax2.set_xticklabels(sources, rotation=45, ha='right', fontsize=9)
        ax2.set_xlabel('Attack Source', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Iterations to Converge', fontsize=12, fontweight='bold')
        ax2.set_title('PSO Convergence Speed per Source',
                      fontsize=14, fontweight='bold')
        ax2.axhline(np.mean(iterations_list), color='red', linestyle='--',
                    linewidth=2, label=f'Mean = {np.mean(iterations_list):.0f}')
        ax2.legend()
        ax2.grid(axis='y', alpha=0.3)
        
        # Add value labels
        for bar, val in zip(bars, iterations_list):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                     f'{int(val)}', ha='center', va='bottom',
                     fontsize=9, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
    
    def plot_m3_vs_m4_accuracy(self, save_path: str):
        """
        Plot M3 vs M4 accuracy and performance comparison.
        
        Shows bar charts comparing key metrics.
        """
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        
        # 1. Accuracy comparison
        categories = ['M3\n(Deterministic)', 'M4\n(PSO + 3%)']
        accuracies = [100.0, self.m4_metrics['accuracy']['accuracy_percentage']]
        colors_bar = ['#4ECDC4', '#FF6B6B']
        
        bars = ax1.bar(categories, accuracies, color=colors_bar,
                       edgecolor='black', linewidth=2)
        ax1.set_ylabel('Accuracy (%)', fontsize=12, fontweight='bold')
        ax1.set_title('Traceback Accuracy: M3 vs M4',
                      fontsize=14, fontweight='bold')
        ax1.set_ylim([0, 110])
        ax1.grid(axis='y', alpha=0.3)
        
        for bar, val in zip(bars, accuracies):
            ax1.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 1,
                     f'{val:.1f}%', ha='center', va='bottom',
                     fontsize=14, fontweight='bold')
        
        # 2. Packets used comparison
        packets = [1800, self.m4_metrics['sampling']['sampled_packets']]
        bars = ax2.bar(categories, packets, color=colors_bar,
                       edgecolor='black', linewidth=2)
        ax2.set_ylabel('Packets Used', fontsize=12, fontweight='bold')
        ax2.set_title('Packet Usage: M3 vs M4\n(Memory Efficiency)',
                      fontsize=14, fontweight='bold')
        ax2.grid(axis='y', alpha=0.3)
        
        for bar, val in zip(bars, packets):
            ax2.text(bar.get_x() + bar.get_width()/2., bar.get_height(),
                     f'{int(val)}', ha='center', va='bottom',
                     fontsize=14, fontweight='bold')
        
        # 3. Coverage comparison per source
        sources = [r['source'] for r in self.pso_results]
        m4_coverages = [r['coverage'] for r in self.pso_results]
        m3_coverages = [33.33] * len(sources)
        
        x = np.arange(len(sources))
        width = 0.35
        
        ax3.bar(x - width/2, m3_coverages, width, label='M3', color='#4ECDC4',
                edgecolor='black', alpha=0.8)
        ax3.bar(x + width/2, m4_coverages, width, label='M4', color='#FF6B6B',
                edgecolor='black', alpha=0.8)
        ax3.set_xticks(x)
        ax3.set_xticklabels(sources, rotation=45, ha='right', fontsize=9)
        ax3.set_ylabel('Coverage %', fontsize=12, fontweight='bold')
        ax3.set_title('Coverage per Source: M3 vs M4',
                      fontsize=14, fontweight='bold')
        ax3.legend()
        ax3.grid(axis='y', alpha=0.3)
        
        # 4. Summary comparison table
        ax4.axis('off')
        table_data = [
            ['Metric', 'M3 (Baseline)', 'M4 (PSO + 3%)'],
            ['Sampling', '100%', '3%'],
            ['Packets', '1800', f'{self.m4_metrics["sampling"]["sampled_packets"]}'],
            ['Accuracy', '100%',
             f'{self.m4_metrics["accuracy"]["accuracy_percentage"]:.1f}%'],
            ['Coverage',
             f'33.33% ± 0%',
             f'{self.m4_metrics["coverage"]["mean_coverage"]:.2f}% ± '
             f'{self.m4_metrics["coverage"]["std_coverage"]:.2f}%'],
            ['Algorithm', 'Greedy', 'PSO'],
            ['Iterations', '1', 
             f'{self.m4_metrics["convergence"]["mean_iterations"]:.0f}'],
            ['Memory Savings', '0%',
             f'{self.m4_metrics["memory"]["memory_savings_percent"]:.1f}%']
        ]
        
        table = ax4.table(cellText=table_data, cellLoc='center', loc='center',
                          colWidths=[0.25, 0.35, 0.35])
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1, 2.5)
        
        for i in range(3):
            table[(0, i)].set_facecolor('#4ECDC4')
            table[(0, i)].set_text_props(weight='bold', color='white')
        
        for i in range(1, len(table_data)):
            for j in range(3):
                if i % 2 == 0:
                    table[(i, j)].set_facecolor('#F0F0F0')
        
        ax4.set_title('M3 vs M4 Summary', fontsize=14, fontweight='bold', pad=20)
        
        fig.suptitle('MILESTONE 4: PSO-BASED IP TRACEBACK RESULTS',
                     fontsize=18, fontweight='bold', y=1.02)
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
    
    def plot_sampling_distribution(self, save_path: str):
        """
        Plot the sampling distribution.
        
        Shows Binomial(1800, 0.03) distribution with actual sample marked.
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        # 1. Theoretical Binomial distribution with actual value
        from scipy.stats import binom
        
        k_values = np.arange(25, 85)
        pmf = binom.pmf(k_values, 1800, 0.03)
        
        ax1.bar(k_values, pmf, alpha=0.6, color='steelblue',
                label='Binomial(1800, 0.03)')
        ax1.axvline(54, color='red', linestyle='--', linewidth=2,
                    label='E[N] = 54')
        ax1.axvline(self.attack_stats['sampled_packets'], color='green',
                    linestyle='-', linewidth=3,
                    label=f'Actual = {self.attack_stats["sampled_packets"]}')
        ax1.axvline(40, color='orange', linestyle=':', linewidth=1.5)
        ax1.axvline(68, color='orange', linestyle=':', linewidth=1.5,
                    label='95% CI [40, 68]')
        
        ax1.set_xlabel('Number of Sampled Packets', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Probability', fontsize=12, fontweight='bold')
        ax1.set_title('M2 Probabilistic Model vs M4 Actual\n'
                      'S ~ Bernoulli(0.03), N ~ Binomial(1800, 0.03)',
                      fontsize=14, fontweight='bold')
        ax1.legend(fontsize=10)
        ax1.grid(alpha=0.3)
        
        # 2. Sampling comparison pie chart
        sampled = self.attack_stats['sampled_packets']
        not_sampled = self.attack_stats['total_packets'] - sampled
        
        labels = [f'Sampled ({sampled})', f'Not Sampled ({not_sampled})']
        sizes = [sampled, not_sampled]
        explode = (0.1, 0)
        colors_pie = ['#FF6B6B', '#E0E0E0']
        
        ax2.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
                colors=colors_pie, startangle=90, shadow=True,
                textprops={'fontweight': 'bold'})
        ax2.set_title('Packet Sampling Distribution\n'
                      f'(p = 0.03, Total = {self.attack_stats["total_packets"]})',
                      fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
    
    def plot_particle_evolution(self, save_path: str):
        """
        Plot particle / coverage evolution visualization.
        
        Shows per-source convergence analysis.
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        # 1. Coverage per source with error-like representation
        sources = [r['source'] for r in self.pso_results]
        coverages = [r['coverage'] for r in self.pso_results]
        iterations = [r['iterations'] for r in self.pso_results]
        
        # Scatter: iterations vs coverage
        scatter = ax1.scatter(iterations, coverages, 
                             c=range(len(sources)), cmap='viridis',
                             s=200, edgecolors='black', linewidth=1.5, zorder=5)
        
        for i, src in enumerate(sources):
            short_name = src.replace('host', 'H')
            ax1.annotate(short_name, (iterations[i], coverages[i]),
                        textcoords="offset points", xytext=(8, 5),
                        fontsize=9, fontweight='bold')
        
        ax1.set_xlabel('PSO Iterations', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Final Coverage (%)', fontsize=12, fontweight='bold')
        ax1.set_title('PSO Performance: Iterations vs Coverage\n'
                      '(Each point = one attack source)',
                      fontsize=14, fontweight='bold')
        ax1.grid(alpha=0.3)
        
        # Add mean lines
        ax1.axhline(np.mean(coverages), color='red', linestyle='--',
                    alpha=0.5, label=f'Mean Coverage = {np.mean(coverages):.2f}%')
        ax1.axvline(np.mean(iterations), color='blue', linestyle='--',
                    alpha=0.5, label=f'Mean Iterations = {np.mean(iterations):.0f}')
        ax1.legend(fontsize=9)
        
        # 2. Path traced for each source shown as horizontal bars
        source_names = [r['source'] for r in self.pso_results]
        path_lengths = [len(r['path']) for r in self.pso_results]
        
        y_pos = np.arange(len(source_names))
        bars = ax2.barh(y_pos, path_lengths, color='purple', alpha=0.7,
                        edgecolor='black')
        ax2.set_yticks(y_pos)
        ax2.set_yticklabels(source_names, fontsize=10)
        ax2.set_xlabel('Path Length (hops)', fontsize=12, fontweight='bold')
        ax2.set_title('Traced Path Lengths by Source',
                      fontsize=14, fontweight='bold')
        ax2.grid(axis='x', alpha=0.3)
        
        for bar, val in zip(bars, path_lengths):
            ax2.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2,
                     f'{val}', va='center', fontsize=10, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
    
    def save_convergence_csv(self, filepath: str):
        """Save convergence data to CSV."""
        rows = []
        for result in self.pso_results:
            if 'convergence_history' in result:
                for h in result['convergence_history']:
                    rows.append({
                        'source': result['source'],
                        'iteration': h['iteration'],
                        'best_fitness': h['best_fitness'],
                        'avg_fitness': h['avg_fitness']
                    })
        
        if rows:
            df = pd.DataFrame(rows)
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            df.to_csv(filepath, index=False)
            print(f"✅ Convergence data saved to {filepath}")
    
    def save_traced_paths_csv(self, filepath: str):
        """Save traced paths to CSV."""
        rows = []
        for result in self.pso_results:
            rows.append({
                'source': result['source'],
                'path': ' → '.join(result['path']) if result['path'] else 'N/A',
                'coverage': result['coverage'],
                'iterations': result['iterations'],
                'converged': result['converged']
            })
        
        df = pd.DataFrame(rows)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        df.to_csv(filepath, index=False)
        print(f"✅ Traced paths saved to {filepath}")


# Example usage
if __name__ == "__main__":
    print("M4 Visualization Module")
    print("Use in main.py pipeline")
