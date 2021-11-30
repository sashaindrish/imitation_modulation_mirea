import allocation as al

from monte_carlo import Task2
from results import print_statistics, print_graphs

ITERATIONS = 1_000
if __name__ == '__main__':
    years = 3
    input_ = {
        'output_volume': (
            al.normal_distribution(1_500, 300, ITERATIONS, False),
            al.normal_distribution(1_600, 325, ITERATIONS, False),
            al.normal_distribution(1_700, 350, ITERATIONS, False)
        ),  # выходной объём
        'price_for_one': (
            al.uniform_distribution(low=8_500, high=10_500, size=ITERATIONS, print_graph=False),
            al.uniform_distribution(low=9_000, high=11_000, size=ITERATIONS, print_graph=False),
            al.uniform_distribution(low=9_500, high=11_500, size=ITERATIONS, print_graph=False)
        ),  # цена за штуку, руб.
        'self_costs_percent': (  # Себестоимость %
            al.normal_distribution(0.55, 0.05, ITERATIONS, False),
            al.normal_distribution(0.55, 0.05, ITERATIONS, False),
            al.normal_distribution(0.55, 0.05, ITERATIONS, False)
        ),
        'operational_fee_percent': (  # Операционные издержки, %
            al.normal_distribution(0.15, 0.05, ITERATIONS, False),
            al.normal_distribution(0.15, 0.05, ITERATIONS, False),
            al.normal_distribution(0.15, 0.05, ITERATIONS, False)
        ),
        'tax': al.constant(0.2),  # налог на прибыль, %
        'discount_rate': al.constant(0.08),  # норма дисконта, %
        'residual_value': al.constant(0),  # остаточная стоимость, руб.
        'start_up_investment': al.constant(0.01),
        'depreciation': al.constant(0)
    }

    monte_carlo = Task2(input_, years=3)

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
