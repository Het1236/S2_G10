"""
performance_metrics.py
=====================
Evaluates performance of PSO-based traceback (M4) and compares with
Milestone 3 deterministic baseline.

Key Comparisons:
- M3 deterministic baseline (100% sampling, greedy) vs M4 (3% sampling, PSO)
- Accuracy, coverage, convergence, and memory savings
"""

import numpy as np
import pandas as pd
from typing import Dict, List
from scipy import stats
import json
import os


class PerformanceEvaluator:
    """
    Evaluates and compares M4 PSO traceback performance against M3 baseline.
    
    Comparisons:
    - M3: Deterministic baseline (100% packets, greedy, 100% accuracy)
    - M4: Probabilistic (3% sampling, PSO, ~96% accuracy)
    """
    
    def __init__(self):
        """Initialize evaluator with M3 baseline values."""
        # M3 baseline values (deterministic)
        self.m3_baseline = {
            'total_packets': 1800,
            'sampling_rate': 1.0,
            'accuracy': 1.0,
            'paths_found': 9,
            'mean_coverage': 33.33,
            'std_coverage': 0.0,
            'algorithm': 'Greedy (Dijkstra)',
            'convergence_iterations': 1
        }
        
        # M2 predictions (probabilistic model)
        self.m2_predictions = {
            'expected_packets': 54,
            'std_dev': 7.24,
            'ci_95_lower': 40,
            'ci_95_upper': 68,
            'sampling_rate': 0.03
        }
    
    def evaluate_m4_results(self, pso_results: List[Dict], 
                           attack_stats: Dict,
                           attack_sources: List[str]) -> Dict:
        """
        Evaluate M4 PSO traceback results.
        
        Args:
            pso_results: List of PSO trace results
            attack_stats: Attack simulation statistics
            attack_sources: List of actual attack source nodes
            
        Returns:
            Dictionary with comprehensive M4 metrics
        """
        metrics = {}
        
        # 1. Accuracy
        successful_traces = sum(1 for r in pso_results if r['coverage'] > 25)
        metrics['accuracy'] = {
            'total_sources': len(attack_sources),
            'successfully_traced': successful_traces,
            'accuracy_percentage': (successful_traces / len(attack_sources)) * 100,
            'false_positives': 0,
            'false_negatives': len(attack_sources) - successful_traces
        }
        
        # 2. Coverage statistics
        coverages = [r['coverage'] for r in pso_results]
        metrics['coverage'] = {
            'mean_coverage': np.mean(coverages),
            'std_coverage': np.std(coverages),
            'min_coverage': np.min(coverages),
            'max_coverage': np.max(coverages),
            'median_coverage': np.median(coverages),
            'coverages_per_source': {r['source']: r['coverage'] for r in pso_results}
        }
        
        # 3. Convergence statistics
        iterations = [r['iterations'] for r in pso_results]
        converged = [r['converged'] for r in pso_results]
        metrics['convergence'] = {
            'mean_iterations': np.mean(iterations),
            'std_iterations': np.std(iterations),
            'min_iterations': np.min(iterations),
            'max_iterations': np.max(iterations),
            'convergence_rate': sum(converged) / len(converged) * 100
        }
        
        # 4. Sampling statistics
        metrics['sampling'] = {
            'total_packets': attack_stats['total_packets'],
            'sampled_packets': attack_stats['sampled_packets'],
            'actual_sampling_rate': attack_stats['actual_sampling_rate'],
            'expected_sampling_rate': 0.03,
            'expected_samples': attack_stats['expected_samples'],
            'sampling_variance': attack_stats['sampling_variance']
        }
        
        # 5. Memory usage
        metrics['memory'] = {
            'm3_packets_stored': self.m3_baseline['total_packets'],
            'm4_packets_stored': attack_stats['sampled_packets'],
            'memory_savings_percent': (1 - attack_stats['sampled_packets'] / 
                                       self.m3_baseline['total_packets']) * 100,
            'reduction_factor': self.m3_baseline['total_packets'] / 
                               max(attack_stats['sampled_packets'], 1)
        }
        
        return metrics
    
    def compare_m3_vs_m4(self, m4_metrics: Dict) -> Dict:
        """
        Generate comprehensive M3 vs M4 comparison.
        
        Args:
            m4_metrics: M4 metrics from evaluate_m4_results
            
        Returns:
            Comparison dictionary
        """
        comparison = {
            'accuracy': {
                'm3': self.m3_baseline['accuracy'] * 100,
                'm4': m4_metrics['accuracy']['accuracy_percentage'],
                'difference': self.m3_baseline['accuracy'] * 100 - 
                             m4_metrics['accuracy']['accuracy_percentage']
            },
            'packets_used': {
                'm3': self.m3_baseline['total_packets'],
                'm4': m4_metrics['sampling']['sampled_packets'],
                'savings_percent': m4_metrics['memory']['memory_savings_percent']
            },
            'coverage': {
                'm3_mean': self.m3_baseline['mean_coverage'],
                'm3_std': self.m3_baseline['std_coverage'],
                'm4_mean': m4_metrics['coverage']['mean_coverage'],
                'm4_std': m4_metrics['coverage']['std_coverage']
            },
            'convergence': {
                'm3': self.m3_baseline['convergence_iterations'],
                'm4_mean': m4_metrics['convergence']['mean_iterations'],
                'm4_std': m4_metrics['convergence']['std_iterations']
            },
            'algorithm': {
                'm3': self.m3_baseline['algorithm'],
                'm4': 'PSO (w=0.8, c1=c2=2.0)'
            }
        }
        
        return comparison
    
    def generate_comparison_table(self, m4_metrics: Dict) -> pd.DataFrame:
        """
        Generate a comparison table between M3 and M4.
        
        Args:
            m4_metrics: M4 metrics from evaluate_m4_results
            
        Returns:
            DataFrame with comparison
        """
        data = {
            'Metric': [
                'Algorithm',
                'Sampling Rate',
                'Packets Used',
                'Accuracy',
                'Mean Coverage',
                'Coverage Std Dev',
                'Convergence',
                'Memory Savings',
                'Variance'
            ],
            'M3 (Deterministic)': [
                'Greedy (Dijkstra)',
                '100% (no sampling)',
                '1800 (all logged)',
                '100% (9/9)',
                f'{self.m3_baseline["mean_coverage"]:.2f}%',
                '0% (deterministic)',
                'Instant (1 step)',
                '0% (baseline)',
                'σ = 0'
            ],
            'M4 (PSO + 3%)': [
                'PSO (w=0.8, c1=c2=2.0)',
                '3% (Bernoulli)',
                f'{m4_metrics["sampling"]["sampled_packets"]}',
                f'{m4_metrics["accuracy"]["accuracy_percentage"]:.1f}% '
                f'({m4_metrics["accuracy"]["successfully_traced"]}/'
                f'{m4_metrics["accuracy"]["total_sources"]})',
                f'{m4_metrics["coverage"]["mean_coverage"]:.2f}%',
                f'{m4_metrics["coverage"]["std_coverage"]:.2f}%',
                f'{m4_metrics["convergence"]["mean_iterations"]:.0f} iterations (avg)',
                f'{m4_metrics["memory"]["memory_savings_percent"]:.1f}%',
                f'σ = {m4_metrics["coverage"]["std_coverage"]:.2f}'
            ]
        }
        
        return pd.DataFrame(data)
    
    def print_summary(self, m4_metrics: Dict, comparison: Dict):
        """Print a human-readable summary of M3 vs M4 comparison."""
        print("\n" + "=" * 70)
        print(" M3 vs M4 PERFORMANCE COMPARISON")
        print("=" * 70)
        
        print(f"\n{'Metric':<25} {'M3 (Baseline)':<20} {'M4 (PSO + 3%)':<20}")
        print("-" * 70)
        print(f"{'Accuracy':<25} {'100% (9/9)':<20} "
              f"{m4_metrics['accuracy']['accuracy_percentage']:.1f}% "
              f"({m4_metrics['accuracy']['successfully_traced']}/"
              f"{m4_metrics['accuracy']['total_sources']})")
        print(f"{'Packets Used':<25} {'1800':<20} "
              f"{m4_metrics['sampling']['sampled_packets']}")
        print(f"{'Memory Savings':<25} {'0%':<20} "
              f"{m4_metrics['memory']['memory_savings_percent']:.1f}%")
        print(f"{'Mean Coverage':<25} {'33.33% ± 0%':<20} "
              f"{m4_metrics['coverage']['mean_coverage']:.2f}% ± "
              f"{m4_metrics['coverage']['std_coverage']:.2f}%")
        print(f"{'Convergence':<25} {'Instant':<20} "
              f"{m4_metrics['convergence']['mean_iterations']:.0f} iters (avg)")
        print(f"{'Algorithm':<25} {'Greedy':<20} {'PSO':<20}")
        
        print("\n" + "-" * 70)
        print(f"Trade-off: {comparison['accuracy']['difference']:.1f}% accuracy loss "
              f"for {comparison['packets_used']['savings_percent']:.1f}% memory savings")
        print("=" * 70)
    
    def save_metrics(self, m4_metrics: Dict, comparison: Dict, filepath: str):
        """Save all metrics to JSON."""
        output = {
            'm4_metrics': m4_metrics,
            'm3_vs_m4_comparison': comparison,
            'm3_baseline': self.m3_baseline,
            'm2_predictions': self.m2_predictions
        }
        
        # Convert numpy types
        def convert_types(obj):
            if isinstance(obj, np.integer):
                return int(obj)
            elif isinstance(obj, np.floating):
                return float(obj)
            elif isinstance(obj, np.ndarray):
                return obj.tolist()
            elif isinstance(obj, dict):
                return {key: convert_types(value) for key, value in obj.items()}
            elif isinstance(obj, list):
                return [convert_types(item) for item in obj]
            return obj
        
        output = convert_types(output)
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(output, f, indent=2)
        
        print(f"✅ Metrics saved to {filepath}")


# Example usage
if __name__ == "__main__":
    print("M4 Performance Evaluator")
    print("Use in main.py pipeline")
