from abc import abstractmethod, ABC
from functools import cached_property

import numpy_financial as npf

ITERATIONS = 1_000

class MonteCarlo(ABC):
    def __init__(self, values, years):
        self.values_dict = values
        self.years = years

    @cached_property
    def values(self):
        def get_value(val, iteration: int):
            return tuple([v[iteration] for v in val]) if isinstance(val, tuple) else val[iteration]

        return [{key: get_value(val, i) for (key, val) in
                 self.values_dict.items()} for i in range(ITERATIONS)]

    def _get_values_for_year(self, name: str, iteration: int, year: int):
        return self.values[iteration][name][year] \
            if isinstance(self.values[iteration][name], tuple) \
            else self.values[iteration][name]

    @abstractmethod
    def calculate_cf_t(self, i: int, for_year: int = None) -> float:
        pass

    def calculate_npv(self, i: int) -> float:
        r = self.values[i].get('discount_rate')
        npv = 0

        for t in range(0, self.years):
            cf_t = self.calculate_cf_t(i, for_year=t)
            sn = self.values[i].get('residual_value') if t == self.years - 1 else 0
            npv = npv + (cf_t + sn) / (1 + r) ** (t + 1)

        npv = npv - self.values[i].get('start_up_investment')

        return npv

    def calculate_pi(self, i: int) -> float:
        r = self.values[i].get('discount_rate')
        pi = 0

        for t in range(0, self.years):
            cf_t = self.calculate_cf_t(i, for_year=t)
            pi = pi + cf_t / (1 + r) ** (t + 1)

        pi = pi / self.values[i].get('start_up_investment')

        return pi

    def calculate_irr(self, i: int):
        return npf.irr([-1 * self.values[i].get('start_up_investment')] +
                       [self.calculate_cf_t(i, for_year=for_year) for for_year in
                        range(self.years)])

    def calculate_all(self):
        return {
            'cf_t': tuple([self.calculate_cf_t(i, year) for i in range(ITERATIONS)]
                          for year in range(self.years)),
            'npv': [self.calculate_npv(i) for i in range(ITERATIONS)],
            'pi': [self.calculate_pi(i) for i in range(ITERATIONS)],
            'irr': [self.calculate_irr(i) for i in range(ITERATIONS)],
        }


class Task2(MonteCarlo):
    def calculate_cf_t(self, i: int, for_year: int = None) -> float:
        v = lambda name: self._get_values_for_year(name, i, for_year)  # noqa: E731
        # (1 - T) * (Q * P - (1 - CP) - (1 - OPEX))
        return (1 - v('tax')) * (
                v('output_volume') * v('price_for_one') -
                (1 - (v('price_for_one') * v('self_costs_percent'))) -
                (1 - (v('price_for_one') * v('operational_fee_percent'))))


class Task3(MonteCarlo):
    def calculate_cf_t(self, i: int, for_year: int = None) -> float:
        v = lambda name: self._get_values_for_year(name, i, for_year)  # noqa: E731
        # (1 - T) * (Q * P - (1 - CP) - (1 - OPEX))
        return (1 - v('tax')) * (
                v('output_volume') * v('price_for_one') -
                (1 - (v('price_for_one') * v('self_costs_percent'))) -
                (1 - (v('price_for_one') * v('operational_fee_percent'))))
