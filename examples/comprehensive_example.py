#!/usr/bin/env python3
"""
Comprehensive Example Script
============================

This script demonstrates all major functionalities of the simulation framework:
1. Monte Carlo financial analysis
2. Queueing system simulation
3. Non-stationary process modeling
4. Statistical analysis and visualization

Run this script to see all features in action.
"""

import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from tabulate import tabulate

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import our modules
from monte_carlo.solution.python.monte_carlo import Task2, Task3
import monte_carlo.solution.python.allocation as al
import smo.soluton.smo2 as smo2
import mnppt.mnppt.solution.main as main
import mnppt.mnppt.solution.smo2 as mnppt_smo2

def monte_carlo_demo():
    """Demonstrate Monte Carlo simulation capabilities"""
    print("\n" + "="*60)
    print("MONTE CARLO SIMULATION DEMONSTRATION")
    print("="*60)
    
    # Define parameter distributions
    print("Setting up parameter distributions...")
    values = {
        'tax': al.uniform_distribution(0.15, 0.25, size=1000, print_graph=False),
        'output_volume': al.normal_distribution(1000, 100, nums=1000, print_graph=False),
        'price_for_one': al.triangular_distribution(80, 100, 120, nums=1000, print_graph=False),
        'self_costs_percent': al.uniform_distribution(0.5, 0.7, size=1000, print_graph=False),
        'operational_fee_percent': al.uniform_distribution(0.05, 0.15, size=1000, print_graph=False),
        'discount_rate': al.uniform_distribution(0.08, 0.12, size=1000, print_graph=False),
        'start_up_investment': al.constant(1000000, nums=1000),
        'residual_value': al.constant(50000, nums=1000)
    }
    
    # Run Task2 simulation
    print("Running Task2 Monte Carlo simulation...")
    task2_sim = Task2(values, years=5)
    task2_results = task2_sim.calculate_all()
    
    # Run Task3 simulation
    print("Running Task3 Monte Carlo simulation...")
    task3_sim = Task3(values, years=5)
    task3_results = task3_sim.calculate_all()
    
    # Analyze results
    print("\nTask2 Results:")
    print(f"  Average NPV: ${np.mean(task2_results['npv']):,.2f}")
    print(f"  NPV Std Dev: ${np.std(task2_results['npv']):,.2f}")
    print(f"  Average PI: {np.mean(task2_results['pi']):.3f}")
    print(f"  Average IRR: {np.mean(task2_results['irr']):.1%}")
    print(f"  Probability of positive NPV: {sum(1 for x in task2_results['npv'] if x > 0)/len(task2_results['npv']):.1%}")
    
    print("\nTask3 Results:")
    print(f"  Average NPV: ${np.mean(task3_results['npv']):,.2f}")
    print(f"  NPV Std Dev: ${np.std(task3_results['npv']):,.2f}")
    print(f"  Average PI: {np.mean(task3_results['pi']):.3f}")
    print(f"  Average IRR: {np.mean(task3_results['irr']):.1%}")
    
    return task2_results, task3_results

def queueing_system_demo():
    """Demonstrate queueing system simulation capabilities"""
    print("\n" + "="*60)
    print("QUEUEING SYSTEM SIMULATION DEMONSTRATION")
    print("="*60)
    
    # Test different scenarios
    scenarios = [
        {"name": "Low Load", "arrival_rate": 8, "service_time": 5},
        {"name": "Medium Load", "arrival_rate": 10, "service_time": 5},
        {"name": "High Load", "arrival_rate": 12, "service_time": 5},
        {"name": "Fast Service", "arrival_rate": 10, "service_time": 3},
        {"name": "Slow Service", "arrival_rate": 10, "service_time": 7}
    ]
    
    results = []
    
    for scenario in scenarios:
        print(f"\nTesting {scenario['name']} scenario...")
        avg_time = 60 / scenario['arrival_rate']
        
        KZP, SDO, SVOvO, MaxLQ, SVPZvS, _, _, _ = smo2.smo_model(
            avg_time_PinH=avg_time,
            avg_min=scenario['service_time'],
            size=100,
            time=None,
            print_data=False
        )
        
        results.append({
            'Scenario': scenario['name'],
            'Arrival Rate (customers/hour)': scenario['arrival_rate'],
            'Service Time (minutes)': scenario['service_time'],
            'Utilization': f"{KZP:.3f}",
            'Avg Queue Length': f"{SDO:.2f}",
            'Avg Wait Time (min)': f"{SVOvO:.2f}",
            'Max Queue Length': MaxLQ,
            'Avg System Time (min)': f"{SVPZvS:.2f}"
        })
    
    # Display results in table
    print("\nQueueing System Results:")
    print(tabulate(results, headers='keys', tablefmt='grid'))
    
    return results

def non_stationary_process_demo():
    """Demonstrate non-stationary process modeling capabilities"""
    print("\n" + "="*60)
    print("NON-STATIONARY PROCESS MODELING DEMONSTRATION")
    print("="*60)
    
    # Analyze different intensity functions
    hours = range(24)
    functions = [
        ("Formula A", main.formula_a),
        ("Formula B", main.formula_b),
        ("Formula C", main.formula_c)
    ]
    
    intensity_results = []
    
    for func_name, func in functions:
        print(f"\nAnalyzing {func_name}...")
        intensities = [func(h) for h in hours]
        
        peak_hour = np.argmax(intensities)
        off_peak_hour = np.argmin(intensities)
        
        intensity_results.append({
            'Function': func_name,
            'Peak Hour': f"{peak_hour}:00",
            'Peak Intensity': f"{intensities[peak_hour]:.1f}",
            'Off-Peak Hour': f"{off_peak_hour}:00",
            'Off-Peak Intensity': f"{intensities[off_peak_hour]:.1f}",
            'Avg Intensity': f"{np.mean(intensities):.1f}"
        })
    
    print("\nIntensity Function Analysis:")
    print(tabulate(intensity_results, headers='keys', tablefmt='grid'))
    
    # Simulate 24-hour performance with Formula A
    print("\nSimulating 24-hour performance with Formula A...")
    hourly_stats = []
    
    for hour in range(24):
        intensity = main.formula_a(hour)
        avg_time = 60 / intensity
        
        KZP, SDO, SVOvO, MaxLQ, SVPZvS, _, _, _ = mnppt_smo2.smo_model(
            avg_time_PinH=avg_time,
            avg_min=5.0,
            size=50,
            time=60,
            print_data=False
        )
        
        hourly_stats.append({
            'hour': hour,
            'intensity': intensity,
            'utilization': KZP,
            'avg_wait': SVOvO,
            'max_queue': MaxLQ
        })
    
    # Find worst and best performing hours
    worst_hour = max(hourly_stats, key=lambda x: x['avg_wait'])
    best_hour = min(hourly_stats, key=lambda x: x['avg_wait'])
    
    print(f"\nWorst performing hour: {worst_hour['hour']}:00")
    print(f"  Intensity: {worst_hour['intensity']:.1f} customers/hour")
    print(f"  Average wait: {worst_hour['avg_wait']:.2f} minutes")
    print(f"  Max queue length: {worst_hour['max_queue']}")
    
    print(f"\nBest performing hour: {best_hour['hour']}:00")
    print(f"  Intensity: {best_hour['intensity']:.1f} customers/hour")
    print(f"  Average wait: {best_hour['avg_wait']:.2f} minutes")
    print(f"  Max queue length: {best_hour['max_queue']}")
    
    return hourly_stats

def visualization_demo(task2_results, task3_results, queue_results, hourly_stats):
    """Demonstrate visualization capabilities"""
    print("\n" + "="*60)
    print("VISUALIZATION DEMONSTRATION")
    print("="*60)
    
    # Create comprehensive visualization
    fig = plt.figure(figsize=(20, 15))
    
    # 1. Monte Carlo NPV Comparison
    ax1 = plt.subplot(3, 3, 1)
    ax1.hist(task2_results['npv'], bins=30, alpha=0.7, label='Task2', color='blue')
    ax1.hist(task3_results['npv'], bins=30, alpha=0.7, label='Task3', color='red')
    ax1.set_xlabel('NPV ($)')
    ax1.set_ylabel('Frequency')
    ax1.set_title('NPV Distribution Comparison')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # 2. Monte Carlo PI Distribution
    ax2 = plt.subplot(3, 3, 2)
    ax2.hist(task2_results['pi'], bins=30, alpha=0.7, color='blue')
    ax2.axvline(np.mean(task2_results['pi']), color='red', linestyle='--', label='Mean')
    ax2.set_xlabel('Profitability Index')
    ax2.set_ylabel('Frequency')
    ax2.set_title('PI Distribution (Task2)')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # 3. Monte Carlo IRR Distribution
    ax3 = plt.subplot(3, 3, 3)
    ax3.hist(task2_results['irr'], bins=30, alpha=0.7, color='green')
    ax3.axvline(np.mean(task2_results['irr']), color='red', linestyle='--', label='Mean')
    ax3.set_xlabel('Internal Rate of Return')
    ax3.set_ylabel('Frequency')
    ax3.set_title('IRR Distribution (Task2)')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # 4. Queue Performance Comparison
    ax4 = plt.subplot(3, 3, 4)
    scenarios = [r['Scenario'] for r in queue_results]
    wait_times = [float(r['Avg Wait Time (min)']) for r in queue_results]
    ax4.bar(scenarios, wait_times, color='orange', alpha=0.7)
    ax4.set_xlabel('Scenario')
    ax4.set_ylabel('Average Wait Time (minutes)')
    ax4.set_title('Queue Performance by Scenario')
    ax4.tick_params(axis='x', rotation=45)
    ax4.grid(True, alpha=0.3)
    
    # 5. Queue Utilization
    ax5 = plt.subplot(3, 3, 5)
    utilizations = [float(r['Utilization']) for r in queue_results]
    ax5.bar(scenarios, utilizations, color='purple', alpha=0.7)
    ax5.set_xlabel('Scenario')
    ax5.set_ylabel('Server Utilization')
    ax5.set_title('Server Utilization by Scenario')
    ax5.tick_params(axis='x', rotation=45)
    ax5.grid(True, alpha=0.3)
    
    # 6. Queue Length Comparison
    ax6 = plt.subplot(3, 3, 6)
    queue_lengths = [float(r['Avg Queue Length']) for r in queue_results]
    ax6.bar(scenarios, queue_lengths, color='brown', alpha=0.7)
    ax6.set_xlabel('Scenario')
    ax6.set_ylabel('Average Queue Length')
    ax6.set_title('Queue Length by Scenario')
    ax6.tick_params(axis='x', rotation=45)
    ax6.grid(True, alpha=0.3)
    
    # 7. 24-Hour Intensity Pattern
    ax7 = plt.subplot(3, 3, 7)
    hours = [stat['hour'] for stat in hourly_stats]
    intensities = [stat['intensity'] for stat in hourly_stats]
    ax7.plot(hours, intensities, 'b-o', linewidth=2, markersize=4)
    ax7.set_xlabel('Hour of Day')
    ax7.set_ylabel('Arrival Intensity (customers/hour)')
    ax7.set_title('24-Hour Arrival Pattern (Formula A)')
    ax7.grid(True, alpha=0.3)
    ax7.set_xticks(range(0, 24, 3))
    
    # 8. 24-Hour Wait Times
    ax8 = plt.subplot(3, 3, 8)
    wait_times_24h = [stat['avg_wait'] for stat in hourly_stats]
    ax8.plot(hours, wait_times_24h, 'r-o', linewidth=2, markersize=4)
    ax8.set_xlabel('Hour of Day')
    ax8.set_ylabel('Average Wait Time (minutes)')
    ax8.set_title('24-Hour Wait Time Pattern')
    ax8.grid(True, alpha=0.3)
    ax8.set_xticks(range(0, 24, 3))
    
    # 9. 24-Hour Utilization
    ax9 = plt.subplot(3, 3, 9)
    utilizations_24h = [stat['utilization'] for stat in hourly_stats]
    ax9.plot(hours, utilizations_24h, 'g-o', linewidth=2, markersize=4)
    ax9.set_xlabel('Hour of Day')
    ax9.set_ylabel('Server Utilization')
    ax9.set_title('24-Hour Utilization Pattern')
    ax9.grid(True, alpha=0.3)
    ax9.set_xticks(range(0, 24, 3))
    
    plt.tight_layout()
    plt.show()
    
    print("Visualization completed! Check the generated plots.")

def statistical_analysis_demo(task2_results, task3_results):
    """Demonstrate statistical analysis capabilities"""
    print("\n" + "="*60)
    print("STATISTICAL ANALYSIS DEMONSTRATION")
    print("="*60)
    
    from scipy import stats
    
    # Comprehensive statistical analysis
    metrics = {
        'NPV': task2_results['npv'],
        'PI': task2_results['pi'],
        'IRR': task2_results['irr']
    }
    
    analysis_results = []
    
    for metric_name, values in metrics.items():
        # Basic statistics
        mean_val = np.mean(values)
        std_val = np.std(values)
        median_val = np.median(values)
        
        # Percentiles
        p5 = np.percentile(values, 5)
        p25 = np.percentile(values, 25)
        p75 = np.percentile(values, 75)
        p95 = np.percentile(values, 95)
        
        # Confidence interval
        ci = stats.t.interval(0.95, len(values)-1, loc=mean_val, scale=stats.sem(values))
        
        # Skewness and kurtosis
        skewness = stats.skew(values)
        kurtosis = stats.kurtosis(values)
        
        analysis_results.append({
            'Metric': metric_name,
            'Mean': f"{mean_val:.4f}",
            'Std Dev': f"{std_val:.4f}",
            'Median': f"{median_val:.4f}",
            '5th %ile': f"{p5:.4f}",
            '25th %ile': f"{p25:.4f}",
            '75th %ile': f"{p75:.4f}",
            '95th %ile': f"{p95:.4f}",
            '95% CI Lower': f"{ci[0]:.4f}",
            '95% CI Upper': f"{ci[1]:.4f}",
            'Skewness': f"{skewness:.4f}",
            'Kurtosis': f"{kurtosis:.4f}"
        })
    
    print("Comprehensive Statistical Analysis:")
    print(tabulate(analysis_results, headers='keys', tablefmt='grid'))
    
    # Risk analysis
    npv_values = task2_results['npv']
    positive_npv_prob = sum(1 for x in npv_values if x > 0) / len(npv_values)
    var_95 = np.percentile(npv_values, 5)  # Value at Risk (95% confidence)
    
    print(f"\nRisk Analysis:")
    print(f"  Probability of positive NPV: {positive_npv_prob:.1%}")
    print(f"  Value at Risk (95%): ${var_95:,.2f}")
    print(f"  Expected NPV: ${np.mean(npv_values):,.2f}")
    print(f"  NPV Range: ${np.min(npv_values):,.2f} to ${np.max(npv_values):,.2f}")

def main():
    """Main demonstration function"""
    print("SIMULATION AND MODELING FRAMEWORK")
    print("Comprehensive Demonstration Script")
    print("="*60)
    
    try:
        # Run all demonstrations
        task2_results, task3_results = monte_carlo_demo()
        queue_results = queueing_system_demo()
        hourly_stats = non_stationary_process_demo()
        
        # Statistical analysis
        statistical_analysis_demo(task2_results, task3_results)
        
        # Visualization
        visualization_demo(task2_results, task3_results, queue_results, hourly_stats)
        
        print("\n" + "="*60)
        print("DEMONSTRATION COMPLETED SUCCESSFULLY!")
        print("="*60)
        print("\nThis demonstration showcased:")
        print("✓ Monte Carlo financial analysis with risk assessment")
        print("✓ Queueing system simulation with multiple scenarios")
        print("✓ Non-stationary process modeling with 24-hour analysis")
        print("✓ Comprehensive statistical analysis")
        print("✓ Advanced visualization capabilities")
        print("\nFor more detailed information, see:")
        print("- API_DOCUMENTATION.md for complete API reference")
        print("- QUICK_REFERENCE.md for common use cases")
        print("- README.md for project overview and installation")
        
    except Exception as e:
        print(f"\nError during demonstration: {e}")
        print("Please check that all dependencies are installed:")
        print("pip install -r requirements.txt")

if __name__ == "__main__":
    main()