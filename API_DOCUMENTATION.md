# Comprehensive API Documentation

This document provides comprehensive documentation for all public APIs, functions, and components in the simulation and modeling codebase.

## Table of Contents

1. [Monte Carlo Simulation Module](#monte-carlo-simulation-module)
2. [Distribution Functions Module](#distribution-functions-module)
3. [Queueing System (SMO) Module](#queueing-system-smo-module)
4. [Non-stationary Process Modeling (MNPPT) Module](#non-stationary-process-modeling-mnppt-module)
5. [Dependencies and Installation](#dependencies-and-installation)

---

## Monte Carlo Simulation Module

### Core Classes

#### `MonteCarlo` (Abstract Base Class)

**Location**: `monte_carlo/solution/python/monte_carlo.py`

**Description**: Abstract base class for Monte Carlo simulation implementations.

**Constructor**:
```python
def __init__(self, values, years)
```

**Parameters**:
- `values` (dict): Dictionary containing simulation parameters with their distributions
- `years` (int): Number of years for the simulation period

**Properties**:
- `values` (cached_property): Processed values for all iterations
- `values_dict`: Original input values dictionary
- `years`: Simulation period in years

**Abstract Methods**:
- `calculate_cf_t(i, for_year=None)`: Calculate cash flow for iteration i and year (must be implemented by subclasses)

**Public Methods**:

##### `calculate_npv(i)`
Calculate Net Present Value for iteration i.

**Parameters**:
- `i` (int): Iteration index

**Returns**:
- `float`: Net Present Value

**Example**:
```python
values = {
    'discount_rate': [0.1] * 1000,
    'start_up_investment': [1000000] * 1000,
    'residual_value': [50000] * 1000
}
simulation = Task2(values, 5)
npv = simulation.calculate_npv(0)
```

##### `calculate_pi(i)`
Calculate Profitability Index for iteration i.

**Parameters**:
- `i` (int): Iteration index

**Returns**:
- `float`: Profitability Index

##### `calculate_irr(i)`
Calculate Internal Rate of Return for iteration i.

**Parameters**:
- `i` (int): Iteration index

**Returns**:
- `float`: Internal Rate of Return

##### `calculate_all()`
Calculate all financial metrics for all iterations.

**Returns**:
- `dict`: Dictionary containing arrays of CF, NPV, PI, and IRR values

**Example**:
```python
results = simulation.calculate_all()
npv_values = results['npv']
pi_values = results['pi']
```

#### `Task2` Class

**Inherits from**: `MonteCarlo`

**Description**: Implementation for Task 2 Monte Carlo simulation with specific cash flow calculation.

**Cash Flow Formula**: `(1 - T) * (Q * P * (1 - CP) * (1 - OP))`

**Required Parameters**:
- `tax`: Tax rate
- `output_volume`: Production volume
- `price_for_one`: Unit price
- `self_costs_percent`: Self-cost percentage
- `operational_fee_percent`: Operational fee percentage

**Example**:
```python
values = {
    'tax': [0.2] * 1000,
    'output_volume': [1000] * 1000,
    'price_for_one': [100] * 1000,
    'self_costs_percent': [0.6] * 1000,
    'operational_fee_percent': [0.1] * 1000,
    'discount_rate': [0.1] * 1000,
    'start_up_investment': [1000000] * 1000,
    'residual_value': [50000] * 1000
}
task2_sim = Task2(values, 5)
results = task2_sim.calculate_all()
```

#### `Task3` Class

**Inherits from**: `MonteCarlo`

**Description**: Implementation for Task 3 Monte Carlo simulation with alternative cash flow calculation.

**Cash Flow Formula**: `(1 - T) * (Q * P - (1 - CP) - (1 - OP))`

**Example**:
```python
task3_sim = Task3(values, 5)
results = task3_sim.calculate_all()
```

### Task Monte Carlo Implementation

#### `task_monte_carlo` Class

**Location**: `monte_carlo/solution/python/task_monte_carlo.py`

**Description**: Comprehensive Monte Carlo simulation implementation with statistical analysis and visualization.

**Constructor**:
```python
def __init__(self, number)
```

**Parameters**:
- `number` (int): Task number identifier

**Public Methods**:

##### Parameter Setting Methods

```python
# Set price parameters
set_price_for_one(low_price, high_price, average_price)

# Set variable costs
set_variable_costs(minimum_costs, high_costs, average_costs)

# Set fixed costs
set_fixed_costs(good, worse)

# Set output volume
set_output_volume(good, worse)

# Set depreciation
set_depreciation(depreciation)

# Set tax rate
set_tax(tax)

# Set discount rate
set_discount_rate(good, worse)

# Set residual value coefficient
set_residual_value(coefficient)

# Set startup investment
set_start_up_investment(invest)
```

##### `math_model(Q, P, CV, F)`
Calculate cash flow using mathematical model.

**Parameters**:
- `Q`: Output volume
- `P`: Price per unit
- `CV`: Variable costs
- `F`: Fixed costs

**Returns**:
- `float`: Cash flow value

##### `net_present_value(q, f, r, p, cv, sn)`
Calculate Net Present Value.

**Parameters**:
- `q`: Output volume
- `f`: Fixed costs
- `r`: Discount rate
- `p`: Price per unit
- `cv`: Variable costs
- `sn`: Residual value

**Returns**:
- `float`: NPV value

##### `rate_of_return(q, f, r, p, cv)`
Calculate Profitability Index.

**Returns**:
- `float`: PI value

##### `solution_model()`
Run the complete Monte Carlo simulation.

**Example**:
```python
# Initialize simulation
sim = task_monte_carlo(1)

# Set parameters
sim.set_price_for_one(80, 120, 100)
sim.set_variable_costs(40, 60, 50)
sim.set_fixed_costs(100000, 200000)
sim.set_output_volume(800, 1200)
sim.set_depreciation(50000)
sim.set_tax(0.2)
sim.set_discount_rate(0.08, 0.12)
sim.set_residual_value(0.05)
sim.set_start_up_investment(1000000)

# Run simulation
sim.solution_model()

# Display results
sim.print_cf_npv_pi()
sim.print_statistics()
```

##### `print_cf_npv_pi()`
Print cash flow, NPV, PI, and IRR values in tabular format.

##### `print_statistics()`
Print comprehensive statistical analysis including:
- Mean, median, mode
- Standard deviation, variance
- Kurtosis, skewness
- Min/max values
- Confidence intervals

##### `vue_results()`
Generate and display histogram visualizations for all simulation results.

---

## Distribution Functions Module

**Location**: `monte_carlo/solution/python/allocation.py`

### Public Functions

#### `normal_distribution(mu=0.5, sigma=0.1, nums=1000, print_graph=True)`

Generate normal distribution samples.

**Parameters**:
- `mu` (float): Mean of the distribution (default: 0.5)
- `sigma` (float): Standard deviation (default: 0.1)
- `nums` (int): Number of samples (default: 1000)
- `print_graph` (bool): Whether to display histogram (default: True)

**Returns**:
- `numpy.ndarray`: Array of normally distributed values

**Example**:
```python
import allocation as al
samples = al.normal_distribution(mu=100, sigma=15, nums=1000)
```

#### `triangular_distribution(left=-3, mode=0, right=8, nums=100000, print_graph=True)`

Generate triangular distribution samples.

**Parameters**:
- `left` (float): Left boundary (default: -3)
- `mode` (float): Mode/peak of distribution (default: 0)
- `right` (float): Right boundary (default: 8)
- `nums` (int): Number of samples (default: 100000)
- `print_graph` (bool): Whether to display histogram (default: True)

**Returns**:
- `numpy.ndarray`: Array of triangularly distributed values

**Example**:
```python
samples = al.triangular_distribution(left=80, mode=100, right=120, nums=1000)
```

#### `exponential_distribution(scale=1.0, nums=10000, print_graph=True)`

Generate exponential distribution samples.

**Parameters**:
- `scale` (float): Scale parameter (default: 1.0)
- `nums` (int): Number of samples (default: 10000)
- `print_graph` (bool): Whether to display histogram (default: True)

**Returns**:
- `numpy.ndarray`: Array of exponentially distributed values

**Example**:
```python
samples = al.exponential_distribution(scale=5.0, nums=1000)
```

#### `uniform_distribution(low=0.0, high=1.0, size=10000, print_graph=True)`

Generate uniform distribution samples.

**Parameters**:
- `low` (float): Lower boundary (default: 0.0)
- `high` (float): Upper boundary (default: 1.0)
- `size` (int): Number of samples (default: 10000)
- `print_graph` (bool): Whether to display histogram (default: True)

**Returns**:
- `numpy.ndarray`: Array of uniformly distributed values

**Example**:
```python
samples = al.uniform_distribution(low=10, high=20, size=1000)
```

#### `constant(value, nums=1000)`

Generate constant value array.

**Parameters**:
- `value` (float): Constant value to repeat
- `nums` (int): Number of repetitions (default: 1000)

**Returns**:
- `numpy.ndarray`: Array filled with constant value

**Example**:
```python
constant_array = al.constant(100, nums=1000)
```

---

## Queueing System (SMO) Module

### Core Functions

#### `smo_model(avg_time_PinH, avg_min, size, time, print_data=True, start_num_bauer=1, final_kum_time=0.0)`

**Location**: `smo/soluton/smo2.py`

**Description**: Single-channel queueing system simulation with exponential distributions.

**Parameters**:
- `avg_time_PinH` (float): Average time between arrivals (minutes)
- `avg_min` (float): Average service time (minutes)
- `size` (int): Maximum number of customers
- `time` (float, optional): Time limit for simulation (minutes)
- `print_data` (bool): Whether to print detailed results (default: True)
- `start_num_bauer` (int): Starting customer number (default: 1)
- `final_kum_time` (float): Cumulative time offset (default: 0.0)

**Returns**:
- `tuple`: (KZP, SDO, SVOvO, MaxLQ, SVPZvS, temp_stat, end_num_bauer, t_kumulitive_end)
  - `KZP`: Server utilization coefficient
  - `SDO`: Average queue length
  - `SVOvO`: Average waiting time in queue
  - `MaxLQ`: Maximum queue length
  - `SVPZvS`: Average time in system
  - `temp_stat`: Detailed statistics dictionary
  - `end_num_bauer`: Last customer number
  - `t_kumulitive_end`: Final cumulative time

**Example**:
```python
import smo2

# Basic simulation
KZP, SDO, SVOvO, MaxLQ, SVPZvS, stats, end_num, final_time = smo2.smo_model(
    avg_time_PinH=6.0,  # 10 customers per hour
    avg_min=5.0,        # 5 minutes service time
    size=100,           # 100 customers
    time=None,          # No time limit
    print_data=True
)

print(f"Server utilization: {KZP}")
print(f"Average queue length: {SDO}")
print(f"Average waiting time: {SVOvO}")
```

### Multi-Server Implementation

#### `smo3.py` - CIW Library Implementation

**Location**: `smo/soluton/smo3.py`

**Description**: Multi-server queueing system using the CIW library.

**Dependencies**: `ciw`, `tabulate`

**Features**:
- Multi-server simulation
- Automatic statistics calculation
- Detailed customer records

**Example**:
```python
import ciw
from statistics import mean

# Create network configuration
network = ciw.create_network(
    arrival_distributions=[ciw.dists.Exponential(rate=10/60)],  # 10 customers/hour
    service_distributions=[ciw.dists.Exponential(rate=5/60)],   # 5 minutes service
    number_of_servers=[2]  # 2 servers
)

# Run simulation
ciw.seed(12455623)
simulation = ciw.Simulation(network)
simulation.simulate_until_max_customers(100)
recs = simulation.get_all_records()

# Get statistics
server_utilization = simulation.transitive_nodes[0].server_utilisation
avg_queue_length = mean([r.queue_size_at_arrival for r in recs])
avg_waiting_time = mean([r.waiting_time for r in recs])
```

---

## Non-stationary Process Modeling (MNPPT) Module

### Main Functions

#### `formula_a(t)`, `formula_b(t)`, `formula_c(t)`, `formula_d(t)`

**Location**: `mnppt/mnppt/solution/main.py`

**Description**: Different intensity functions for non-stationary arrival processes.

**Parameters**:
- `t` (float): Time parameter (hours)

**Returns**:
- `float`: Arrival intensity at time t

**Formulas**:
- `formula_a(t)`: `15 + 10 * sin((3 * π * t) / 24)`
- `formula_b(t)`: `40 + 30 * sin(((4 * π * t) / 24) - π/2)`
- `formula_c(t)`: `100 - 50 * abs((6 - (t mod 12)) / 6)`
- `formula_d(t)`: `15 + 30 * (t mod 12)` if t ≥ 6, undefined otherwise

**Example**:
```python
import main

# Calculate intensity for different times
intensity_6am = main.formula_a(6)
intensity_12pm = main.formula_a(12)
intensity_6pm = main.formula_a(18)
```

### Extended SMO Model

#### `smo_model` (MNPPT Version)

**Location**: `mnppt/mnppt/solution/smo2.py`

**Description**: Extended version of SMO model with support for non-stationary processes.

**Additional Parameters**:
- `start_num_bauer`: Starting customer number for continuous simulation
- `final_kum_time`: Cumulative time offset for time-continuous simulation

**Example**:
```python
import smo2

# Non-stationary simulation
KZP, SDO, SVOvO, MaxLQ, SVPZvS, stats, end_num, final_time = smo2.smo_model(
    avg_time_PinH=6.0,
    avg_min=5.0,
    size=100,
    time=60,  # 1 hour time window
    print_data=False,
    start_num_bauer=1,
    final_kum_time=0.0
)
```

### Complete Non-stationary Simulation

**Location**: `mnppt/mnppt/solution/main.py`

**Description**: Complete 24-hour simulation with varying arrival intensities.

**Example**:
```python
import main

# Run complete 24-hour simulation
# The main script automatically:
# 1. Iterates through 24 hours
# 2. Calculates intensity for each hour
# 3. Runs SMO simulation for each time window
# 4. Aggregates results
# 5. Displays comprehensive statistics

# To run with different intensity functions, modify the main script:
# Uncomment the desired formula (a, b, c, or d)
# Run: python main.py
```

---

## Dependencies and Installation

### Required Packages

**Monte Carlo Module**:
```bash
pip install numpy_financial numpy statistics scipy matplotlib
```

**SMO Module**:
```bash
pip install numpy matplotlib tabulate
```

**SMO3 (Multi-server)**:
```bash
pip install ciw tabulate
```

**MNPPT Module**:
```bash
pip install numpy matplotlib tabulate
```

### Complete Requirements File

Create `requirements.txt`:
```
numpy_financial
numpy
statistics
scipy
matplotlib
tabulate
ciw
```

Install all dependencies:
```bash
pip install -r requirements.txt
```

---

## Usage Examples

### Monte Carlo Investment Analysis

```python
from monte_carlo import Task2
import allocation as al

# Define parameter distributions
values = {
    'tax': al.uniform_distribution(0.15, 0.25, size=1000),
    'output_volume': al.normal_distribution(1000, 100, nums=1000),
    'price_for_one': al.triangular_distribution(80, 100, 120, nums=1000),
    'self_costs_percent': al.uniform_distribution(0.5, 0.7, size=1000),
    'operational_fee_percent': al.uniform_distribution(0.05, 0.15, size=1000),
    'discount_rate': al.uniform_distribution(0.08, 0.12, size=1000),
    'start_up_investment': al.constant(1000000, nums=1000),
    'residual_value': al.constant(50000, nums=1000)
}

# Run simulation
sim = Task2(values, years=5)
results = sim.calculate_all()

# Analyze results
npv_values = results['npv']
print(f"Average NPV: {sum(npv_values)/len(npv_values):.2f}")
print(f"NPV Range: {min(npv_values):.2f} to {max(npv_values):.2f}")
```

### Queueing System Analysis

```python
import smo2

# Analyze different service configurations
configurations = [
    (6.0, 3.0),  # Fast service
    (6.0, 5.0),  # Medium service
    (6.0, 7.0),  # Slow service
]

for avg_time, service_time in configurations:
    KZP, SDO, SVOvO, MaxLQ, SVPZvS, _, _, _ = smo2.smo_model(
        avg_time_PinH=avg_time,
        avg_min=service_time,
        size=100,
        time=None,
        print_data=False
    )
    print(f"Service time: {service_time}min, Avg wait: {SVOvO:.2f}min, Queue length: {SDO:.2f}")
```

### Non-stationary Process Analysis

```python
import main
import smo2

# Analyze peak vs off-peak performance
peak_hour = 12  # Noon
off_peak_hour = 3  # 3 AM

# Calculate intensities
peak_intensity = main.formula_a(peak_hour)
off_peak_intensity = main.formula_a(off_peak_hour)

print(f"Peak intensity: {peak_intensity:.2f} customers/hour")
print(f"Off-peak intensity: {off_peak_intensity:.2f} customers/hour")

# Simulate both scenarios
peak_results = smo2.smo_model(60/peak_intensity, 5, 100, 60, False)
off_peak_results = smo2.smo_model(60/off_peak_intensity, 5, 100, 60, False)

print(f"Peak avg wait: {peak_results[2]:.2f}min")
print(f"Off-peak avg wait: {off_peak_results[2]:.2f}min")
```

---

## Error Handling and Best Practices

### Common Issues and Solutions

1. **Memory Issues with Large Simulations**:
   - Reduce `nums` parameter in distribution functions
   - Use smaller `size` values in SMO simulations
   - Consider using generators for very large datasets

2. **Convergence Issues in IRR Calculation**:
   - Check for negative cash flows
   - Verify discount rate ranges
   - Use try-catch blocks for IRR calculations

3. **Visualization Issues**:
   - Ensure matplotlib backend is properly configured
   - Use `plt.show()` after generating plots
   - Consider saving plots to files for batch processing

### Performance Optimization

1. **Use Cached Properties**: The `MonteCarlo` class uses `@cached_property` for efficient value processing
2. **Vectorized Operations**: Distribution functions use NumPy for efficient array operations
3. **Batch Processing**: SMO simulations can be run in batches for large-scale analysis

### Testing and Validation

1. **Unit Tests**: Test individual functions with known inputs
2. **Monte Carlo Validation**: Compare results with analytical solutions where available
3. **Sensitivity Analysis**: Vary parameters to ensure robust results
4. **Statistical Validation**: Verify distribution properties match expected values

---

This documentation provides comprehensive coverage of all public APIs, functions, and components in the simulation and modeling codebase. Each module includes detailed parameter descriptions, return values, usage examples, and best practices for effective implementation.