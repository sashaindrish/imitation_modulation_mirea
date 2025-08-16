# Simulation and Modeling Framework

A comprehensive Python framework for Monte Carlo simulations, queueing system analysis, and non-stationary process modeling.

## Overview

This project contains three main simulation modules:

1. **Monte Carlo Simulation** - Financial modeling and investment analysis
2. **Queueing System (SMO)** - Single and multi-server queueing system simulation
3. **Non-stationary Process Modeling (MNPPT)** - Time-varying arrival process analysis

## Quick Start

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Basic Usage Examples

#### Monte Carlo Investment Analysis
```python
from monte_carlo.solution.python.monte_carlo import Task2
import monte_carlo.solution.python.allocation as al

# Define parameter distributions
values = {
    'tax': al.uniform_distribution(0.15, 0.25, size=1000),
    'output_volume': al.normal_distribution(1000, 100, nums=1000),
    'price_for_one': al.triangular_distribution(80, 100, 120, nums=1000),
    'discount_rate': al.uniform_distribution(0.08, 0.12, size=1000),
    'start_up_investment': al.constant(1000000, nums=1000)
}

# Run simulation
sim = Task2(values, years=5)
results = sim.calculate_all()
print(f"Average NPV: {sum(results['npv'])/len(results['npv']):.2f}")
```

#### Queueing System Analysis
```python
import smo.soluton.smo2 as smo2

# Run single-channel queueing simulation
KZP, SDO, SVOvO, MaxLQ, SVPZvS, _, _, _ = smo2.smo_model(
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

#### Non-stationary Process Analysis
```python
import mnppt.mnppt.solution.main as main
import mnppt.mnppt.solution.smo2 as smo2

# Calculate arrival intensity for different times
peak_intensity = main.formula_a(12)  # Noon
off_peak_intensity = main.formula_a(3)  # 3 AM

print(f"Peak intensity: {peak_intensity:.2f} customers/hour")
print(f"Off-peak intensity: {off_peak_intensity:.2f} customers/hour")
```

## Project Structure

```
├── monte_carlo/                 # Monte Carlo simulation module
│   └── solution/python/
│       ├── monte_carlo.py      # Core Monte Carlo classes
│       ├── task_monte_carlo.py # Comprehensive implementation
│       ├── allocation.py       # Distribution functions
│       └── requirements.txt    # Dependencies
├── smo/                        # Queueing system module
│   └── soluton/
│       ├── smo.py             # Basic single-channel SMO
│       ├── smo2.py            # Enhanced SMO with parameters
│       ├── smo3.py            # Multi-server SMO (CIW)
│       └── allocation.py      # Distribution functions
├── mnppt/                      # Non-stationary process module
│   └── mnppt/solution/
│       ├── main.py            # Main simulation script
│       ├── smo2.py            # Extended SMO for MNPPT
│       └── allocation.py      # Distribution functions
├── API_DOCUMENTATION.md        # Comprehensive API documentation
└── README.md                   # This file
```

## Key Features

### Monte Carlo Module
- **Financial Metrics**: NPV, PI, IRR calculations
- **Multiple Distributions**: Normal, triangular, exponential, uniform
- **Statistical Analysis**: Mean, variance, confidence intervals
- **Visualization**: Histogram plots and statistical charts

### Queueing System Module
- **Single-Channel**: M/M/1 queueing system
- **Multi-Server**: M/M/c queueing system using CIW library
- **Performance Metrics**: Utilization, queue length, waiting times
- **Time-Limited Simulation**: Support for time-bounded analysis

### Non-stationary Process Module
- **Time-Varying Intensity**: Four different intensity functions
- **24-Hour Simulation**: Complete daily cycle analysis
- **Continuous Simulation**: Seamless time-window transitions
- **Aggregated Statistics**: Comprehensive performance metrics

## Dependencies

### Core Dependencies
- `numpy` - Numerical computations
- `matplotlib` - Visualization
- `scipy` - Statistical functions
- `numpy_financial` - Financial calculations

### Optional Dependencies
- `ciw` - Queueing network simulation
- `tabulate` - Formatted table output

## Documentation

For detailed API documentation, examples, and usage instructions, see:
- **[Complete API Documentation](API_DOCUMENTATION.md)** - Comprehensive reference for all functions and classes
- **[Monte Carlo Examples](monte_carlo/solution/python/)** - Sample implementations and use cases
- **[SMO Examples](smo/soluton/)** - Queueing system analysis examples
- **[MNPPT Examples](mnppt/mnppt/solution/)** - Non-stationary process modeling examples

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For questions, issues, or contributions, please:
1. Check the [API Documentation](API_DOCUMENTATION.md) first
2. Review existing examples in the respective module directories
3. Open an issue with detailed description of your problem

## Academic Use

This framework was developed for academic research in:
- Financial modeling and investment analysis
- Queueing theory and operations research
- Non-stationary stochastic processes
- Simulation and modeling methodologies

The code includes comprehensive documentation and examples suitable for educational purposes and research applications.
