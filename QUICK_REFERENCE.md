# Quick Reference Guide

This guide provides quick code snippets and common use cases for rapid development with the simulation framework.

## Monte Carlo Simulation

### Basic Investment Analysis
```python
from monte_carlo.solution.python.monte_carlo import Task2
import monte_carlo.solution.python.allocation as al

# Quick setup with constant values
values = {
    'tax': al.constant(0.2, nums=1000),
    'output_volume': al.constant(1000, nums=1000),
    'price_for_one': al.constant(100, nums=1000),
    'discount_rate': al.constant(0.1, nums=1000),
    'start_up_investment': al.constant(1000000, nums=1000),
    'residual_value': al.constant(50000, nums=1000)
}

sim = Task2(values, years=5)
results = sim.calculate_all()
print(f"NPV: {sum(results['npv'])/len(results['npv']):.2f}")
```

### Risk Analysis with Distributions
```python
# Risk analysis with uncertain parameters
values = {
    'tax': al.uniform_distribution(0.15, 0.25, size=1000),
    'output_volume': al.normal_distribution(1000, 100, nums=1000),
    'price_for_one': al.triangular_distribution(80, 100, 120, nums=1000),
    'discount_rate': al.uniform_distribution(0.08, 0.12, size=1000),
    'start_up_investment': al.constant(1000000, nums=1000)
}

sim = Task2(values, years=5)
results = sim.calculate_all()

# Risk metrics
npv_values = results['npv']
print(f"Expected NPV: {sum(npv_values)/len(npv_values):.2f}")
print(f"NPV Std Dev: {np.std(npv_values):.2f}")
print(f"Probability of positive NPV: {sum(1 for x in npv_values if x > 0)/len(npv_values):.1%}")
```

## Queueing System Analysis

### Single-Channel Queue
```python
import smo.soluton.smo2 as smo2

# Basic M/M/1 queue
KZP, SDO, SVOvO, MaxLQ, SVPZvS, _, _, _ = smo2.smo_model(
    avg_time_PinH=6.0,  # 10 customers/hour
    avg_min=5.0,        # 5 minutes service
    size=100,
    print_data=False
)

print(f"Utilization: {KZP:.3f}")
print(f"Avg queue length: {SDO:.2f}")
print(f"Avg wait time: {SVOvO:.2f} min")
```

### Service Level Optimization
```python
# Find service time to meet waiting time target
target_wait = 3.0  # minutes
current_wait = float('inf')
service_time = 10.0

while current_wait > target_wait:
    service_time -= 0.1
    _, _, current_wait, _, _, _, _, _ = smo2.smo_model(
        avg_time_PinH=6.0,
        avg_min=service_time,
        size=100,
        print_data=False
    )

print(f"Required service time: {service_time:.1f} minutes")
```

### Multi-Server Queue
```python
import ciw
from statistics import mean

# M/M/2 queue
network = ciw.create_network(
    arrival_distributions=[ciw.dists.Exponential(rate=10/60)],
    service_distributions=[ciw.dists.Exponential(rate=5/60)],
    number_of_servers=[2]
)

ciw.seed(12345)
simulation = ciw.Simulation(network)
simulation.simulate_until_max_customers(100)
recs = simulation.get_all_records()

print(f"Server utilization: {simulation.transitive_nodes[0].server_utilisation:.3f}")
print(f"Avg waiting time: {mean([r.waiting_time for r in recs]):.2f}")
```

## Non-stationary Process Modeling

### Time-Varying Intensity Analysis
```python
import mnppt.mnppt.solution.main as main
import numpy as np

# Analyze intensity patterns
hours = range(24)
intensities = [main.formula_a(h) for h in hours]

peak_hour = np.argmax(intensities)
off_peak_hour = np.argmin(intensities)

print(f"Peak hour: {peak_hour}:00 ({intensities[peak_hour]:.1f} customers/hour)")
print(f"Off-peak hour: {off_peak_hour}:00 ({intensities[off_peak_hour]:.1f} customers/hour)")
```

### 24-Hour Performance Analysis
```python
import mnppt.mnppt.solution.smo2 as smo2

# Simulate each hour with different intensities
hourly_stats = []
for hour in range(24):
    intensity = main.formula_a(hour)
    avg_time = 60 / intensity
    
    KZP, SDO, SVOvO, MaxLQ, SVPZvS, _, _, _ = smo2.smo_model(
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

# Find worst performing hour
worst_hour = max(hourly_stats, key=lambda x: x['avg_wait'])
print(f"Worst hour: {worst_hour['hour']}:00 (wait: {worst_hour['avg_wait']:.2f} min)")
```

## Distribution Functions

### Quick Distribution Generation
```python
import monte_carlo.solution.python.allocation as al

# Common distributions
normal_data = al.normal_distribution(mu=100, sigma=15, nums=1000)
uniform_data = al.uniform_distribution(low=80, high=120, size=1000)
triangular_data = al.triangular_distribution(left=90, mode=100, right=110, nums=1000)
exponential_data = al.exponential_distribution(scale=5.0, nums=1000)
constant_data = al.constant(100, nums=1000)

# Without graphs (for batch processing)
normal_data = al.normal_distribution(mu=100, sigma=15, nums=1000, print_graph=False)
```

## Statistical Analysis

### Monte Carlo Results Analysis
```python
import numpy as np
from scipy import stats

# Analyze simulation results
npv_values = results['npv']
pi_values = results['pi']
irr_values = results['irr']

# Basic statistics
print(f"NPV - Mean: {np.mean(npv_values):.2f}, Std: {np.std(npv_values):.2f}")
print(f"PI - Mean: {np.mean(pi_values):.3f}, Std: {np.std(pi_values):.3f}")

# Confidence intervals
npv_ci = stats.t.interval(0.95, len(npv_values)-1, loc=np.mean(npv_values), scale=stats.sem(npv_values))
print(f"NPV 95% CI: [{npv_ci[0]:.2f}, {npv_ci[1]:.2f}]")

# Percentiles
print(f"NPV 5th percentile: {np.percentile(npv_values, 5):.2f}")
print(f"NPV 95th percentile: {np.percentile(npv_values, 95):.2f}")
```

### Queue Performance Metrics
```python
# Calculate queue performance metrics
def queue_metrics(arrival_rate, service_rate, num_servers=1):
    """Calculate theoretical queue metrics"""
    rho = arrival_rate / (service_rate * num_servers)
    
    if num_servers == 1:
        # M/M/1 formulas
        Lq = (rho**2) / (1 - rho)  # Average queue length
        Wq = Lq / arrival_rate     # Average waiting time
        Ls = rho / (1 - rho)       # Average customers in system
        Ws = Ls / arrival_rate     # Average time in system
    else:
        # M/M/c formulas (simplified)
        Lq = (rho**(num_servers + 1)) / (num_servers * (1 - rho/num_servers)**2)
        Wq = Lq / arrival_rate
        Ls = Lq + rho
        Ws = Ls / arrival_rate
    
    return {
        'utilization': rho,
        'avg_queue_length': Lq,
        'avg_waiting_time': Wq,
        'avg_system_customers': Ls,
        'avg_system_time': Ws
    }

# Compare theoretical vs simulated
theoretical = queue_metrics(10/60, 1/5)  # 10 customers/hour, 5 min service
print(f"Theoretical avg wait: {theoretical['avg_waiting_time']:.2f} min")
```

## Visualization

### Monte Carlo Results Plotting
```python
import matplotlib.pyplot as plt

# Plot NPV distribution
plt.figure(figsize=(10, 6))
plt.hist(results['npv'], bins=50, alpha=0.7, edgecolor='black')
plt.axvline(np.mean(results['npv']), color='red', linestyle='--', label='Mean')
plt.xlabel('NPV')
plt.ylabel('Frequency')
plt.title('NPV Distribution')
plt.legend()
plt.show()

# Plot multiple metrics
fig, axes = plt.subplots(2, 2, figsize=(12, 8))
metrics = ['npv', 'pi', 'irr', 'cf_t']
titles = ['NPV', 'Profitability Index', 'IRR', 'Cash Flow']

for i, (metric, title) in enumerate(zip(metrics, titles)):
    row, col = i // 2, i % 2
    if metric == 'cf_t':
        # Cash flow is tuple of arrays
        cf_data = [item for sublist in results[metric] for item in sublist]
        axes[row, col].hist(cf_data, bins=30, alpha=0.7)
    else:
        axes[row, col].hist(results[metric], bins=30, alpha=0.7)
    axes[row, col].set_title(title)
    axes[row, col].set_xlabel('Value')

plt.tight_layout()
plt.show()
```

### Queue Performance Over Time
```python
# Plot queue performance over 24 hours
hours = [stat['hour'] for stat in hourly_stats]
waits = [stat['avg_wait'] for stat in hourly_stats]
utilizations = [stat['utilization'] for stat in hourly_stats]

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

ax1.plot(hours, waits, 'b-o')
ax1.set_ylabel('Average Wait Time (min)')
ax1.set_title('Queue Performance Over 24 Hours')
ax1.grid(True)

ax2.plot(hours, utilizations, 'r-o')
ax2.set_xlabel('Hour of Day')
ax2.set_ylabel('Server Utilization')
ax2.grid(True)

plt.tight_layout()
plt.show()
```

## Error Handling

### Robust Monte Carlo Simulation
```python
def safe_monte_carlo(values, years, max_iterations=1000):
    """Run Monte Carlo simulation with error handling"""
    try:
        sim = Task2(values, years)
        results = sim.calculate_all()
        
        # Check for invalid results
        valid_npv = [x for x in results['npv'] if not np.isnan(x) and not np.isinf(x)]
        valid_irr = [x for x in results['irr'] if not np.isnan(x) and not np.isinf(x)]
        
        if len(valid_npv) < len(results['npv']) * 0.9:
            print(f"Warning: {len(results['npv']) - len(valid_npv)} invalid NPV values")
        
        return {
            'npv': valid_npv,
            'pi': results['pi'],
            'irr': valid_irr,
            'cf_t': results['cf_t']
        }
    except Exception as e:
        print(f"Simulation failed: {e}")
        return None
```

### Queue Simulation Validation
```python
def validate_queue_params(arrival_rate, service_rate, num_servers=1):
    """Validate queue parameters before simulation"""
    rho = arrival_rate / (service_rate * num_servers)
    
    if rho >= 1:
        print(f"Warning: System is unstable (ρ = {rho:.3f} >= 1)")
        return False
    
    if arrival_rate <= 0 or service_rate <= 0:
        print("Error: Rates must be positive")
        return False
    
    return True

# Use validation before simulation
if validate_queue_params(10/60, 1/5):
    results = smo2.smo_model(6.0, 5.0, 100, None, False)
```

## Performance Optimization

### Batch Processing
```python
# Process multiple scenarios efficiently
scenarios = [
    {'arrival_rate': 8/60, 'service_time': 4},
    {'arrival_rate': 10/60, 'service_time': 5},
    {'arrival_rate': 12/60, 'service_time': 6}
]

results = []
for scenario in scenarios:
    avg_time = 60 / scenario['arrival_rate']
    KZP, SDO, SVOvO, MaxLQ, SVPZvS, _, _, _ = smo2.smo_model(
        avg_time_PinH=avg_time,
        avg_min=scenario['service_time'],
        size=100,
        print_data=False
    )
    results.append({
        'scenario': scenario,
        'utilization': KZP,
        'avg_wait': SVOvO,
        'max_queue': MaxLQ
    })

# Find best scenario
best_scenario = min(results, key=lambda x: x['avg_wait'])
print(f"Best scenario: {best_scenario['scenario']}")
```

This quick reference guide provides the most common use cases and code patterns for rapid development with the simulation framework.