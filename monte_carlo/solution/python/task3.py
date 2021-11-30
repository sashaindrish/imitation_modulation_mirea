import allocation as al

from monte_carlo import Task3
from results import print_statistics, print_graphs
ITERATIONS = 1_000

if __name__ == '__main__':
    years = 3

    input_ = {
        'output_volume': (
            al.normal_distribution(802_000, 25_000, ITERATIONS, False),
            al.normal_distribution(967_000, 30_000, ITERATIONS, False),
            al.normal_distribution(1_132_000, 25_000, ITERATIONS, False)
        ),  # выходной объём
        'price_for_one': (
           al.triangular_distribution(left=5.90, right=6.10, mode=6.00, nums=ITERATIONS, print_graph=False),
           al.triangular_distribution(left=5.95, right=6.15, mode=6.05, nums=ITERATIONS, print_graph=False),
           al.triangular_distribution(left=6.00, right=6.20, mode=6.10, nums=ITERATIONS, print_graph=False)
        ),  # цена за штуку, руб.
        'tax': al.constant(0.32),  # налог на прибыль, %
        'discount_rate': al.constant(0.1),  # норма дисконта, %
        'start_up_investment': al.constant(3_400_000),  # начальные инвестиции
        'self_costs_percent': (  # Себестоимость, %
           al.triangular_distribution(left=0.50, right=0.65, mode=0.55, nums=ITERATIONS, print_graph=False),
           al.triangular_distribution(left=0.50, right=0.65, mode=0.55, nums=ITERATIONS, print_graph=False),
           al.triangular_distribution(left=0.50, right=0.65, mode=0.55, nums=ITERATIONS, print_graph=False)
        ),
        'operational_fee_percent': (  # Операционные издержки, %
            al.normal_distribution(0.15, 0.02, ITERATIONS, False),
            al.normal_distribution(0.15, 0.02, ITERATIONS, False),
            al.normal_distribution(0.15, 0.02, ITERATIONS, False)
        ),
        'residual_value': al.exponential_distribution(scale=0.0, nums=ITERATIONS, print_graph=False),  # остаточная стоимость, руб.
        'depreciation': al.constant(0)
    }

    monte_carlo = Task3(input_, years=3)

    output = monte_carlo.calculate_all()
    all_data = {**input_, **output}

    graphs = [
        {
            'title': 'Выход продукции',
            'data_key': 'output_volume',
            'x': 'Продукция',
            'y': 'Частота возникновения'
        },
        {
            'title': 'Платежи',
            'data_key': 'cf_t',
            'x': 'у.е.',
            'y': 'Частота возникновения'
        },
        {
            'title': 'Чистая приведенная стоимость',
            'data_key': 'npv',
            'x': 'у.е.',
            'y': 'Частота возникновения'
        },
        {
            'title': 'Норма доходности',
            'data_key': 'pi',
            'x': 'Коэф.',
            'y': 'Частота возникновения'
        },
    ]

    print_statistics(output)
    print_graphs(graphs, all_data)
