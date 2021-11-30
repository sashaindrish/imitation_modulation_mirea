import itertools
import statistics
from collections.abc import Iterable

import numpy as np
from matplotlib import pyplot as plt
from scipy import stats
from tabulate import tabulate

stat_methods = {
    'Среднее': np.average,
    'Стандартная ошибка': np.std,
    'Медиана': np.median,
    'Мода': statistics.mode,
    'Стандартное отклонение': lambda array: np.std(array, ddof=1),
    'Дисперсия выборки': np.var,
    'Эксцесс': stats.kurtosis,
    'Минимум': min,
    'Максимум': max,
    'Сумма': sum,
}


def _get_merged_data(output_data):
    is_multi_year = isinstance(output_data[0], Iterable)
    return list(itertools.chain(*output_data)) if is_multi_year else output_data


def print_statistics(data: dict[iter]):
    headers = data.keys()

    rows = [[name, *map(lambda l: fn(_get_merged_data(l)), data.values())]
            for name, fn in stat_methods.items()]

    print(tabulate(rows, headers=['', *headers], floatfmt='.2f',
                   tablefmt='pretty', numalign='right', stralign='left'))


def print_graphs(plots: list, data: dict[iter]):
    fig, axs = plt.subplots(1, len(plots), figsize=(35, 4), num='Монте Карло')
    axs = axs if isinstance(axs, Iterable) else [axs]

    for i, plot in enumerate(plots):
        values = data.get(plot['data_key'])
        axs[i].hist(values, bins=10)

        axs[i].set_title(f'{plot["title"]}\n ({plot["data_key"]})')
        if isinstance(values[0], Iterable):
            years_count = len(values)
            axs[i].legend([f'Год {year+1}' for year in range(years_count)])

        axs[i].set_xlabel(plot['x'])
        axs[i].set_ylabel(plot['y'])

    plt.show()
