import allocation as al
import numpy_financial as npf

size = 100
years = 4


class output_volume:  # выходной объём
    def __init__(self):
        self.worse = 0
        self.good = 0

    def distribution(self):
        return al.normal_distribution(self.good, self.worse, nums=size, print_graph=False)


class price_for_one:  # цена заштуку
    def __init__(self):
        self.low_price = 0
        self.high_price = 0
        self.average_price = 0

    def distribution(self):
        return al.triangular_distribution(self.low_price, self.average_price, self.high_price, nums=size,
                                          print_graph=False)


class variable_costs:  # переменные затраты
    def __init__(self):
        self.minimum_costs = 0
        self.high_costs = 0
        self.average_costs = 0

    def distribution(self):
        return al.triangular_distribution(self.minimum_costs, self.average_costs, self.high_costs, nums=size,
                                          print_graph=False)


class fixed_costs(output_volume):  # постоянные затраты
    def distribution(self):
        return al.uniform_distribution(self.worse, self.good, size=size, print_graph=False)


class discount_rate(output_volume):  # норм дисконта
    def distribution(self):
        return al.uniform_distribution(self.worse, self.good, size=size, print_graph=False)


class residual_value:  # амортизация
    def __init__(self):
        self.coefficient = 0.01

    def distribution(self):
        return al.exponential_distribution(self.coefficient, nums=size, print_graph=False)


class task_monte_carlo:

    def __init__(self, number):
        self.PI = list()
        self.NPV = list()
        self.CF = list()
        self.irr = list()
        self.output_volume = output_volume()
        self.price_for_one = price_for_one()
        self.variable_costs = variable_costs()
        self.fixed_costs = fixed_costs()
        self.depreciation = 0
        self.tax = 0
        self.discount_rate = discount_rate()
        self.residual_value = residual_value()
        self.start_up_investment = 0
        self.number_task = number

    # цена за одну штуку
    def set_price_for_one(self, low_price, high_price, average_price):
        self.price_for_one.low_price = low_price
        self.price_for_one.high_price = high_price
        self.price_for_one.average_price = average_price

    # переменные затраты
    def set_variable_costs(self, minimum_costs, high_costs, average_costs):
        self.variable_costs.minimum_costs = minimum_costs
        self.variable_costs.high_costs = high_costs
        self.variable_costs.average_costs = average_costs

    # постоянные затрвты
    def set_fixed_costs(self, good, worse):
        self.fixed_costs.good = good
        self.fixed_costs.worse = worse

    # обЪём выпуска
    def set_output_volume(self, good, worse):
        self.output_volume.good = good
        self.output_volume.worse = worse

    # амортизация
    def set_depreciation(self, depreciation):
        self.depreciation = depreciation

    # налоговая ставка
    def set_tax(self, tax):
        self.tax = tax

    # норма дисконта
    def set_discount_rate(self, good, worse):
        self.discount_rate.worse = worse
        self.discount_rate.good = good

    # остаточная стоймость
    def set_residual_value(self, coefficient):
        self.residual_value.coefficient = coefficient

    # начальные инвестиции
    def set_start_up_investment(self, invest):
        self.start_up_investment = invest

    # математическя модель CF(t)
    def math_model(self, Q, P, CV, F):
        T = self.tax
        A = self.depreciation
        ce_t = (1 - T) * (Q * P - CV * Q + A - F)
        return ce_t

    #  NPV
    def net_present_value(self, q, f, r, p, cv, sn):  # Чистая приведенная стоимость
        i = r / 100
        NPV = 0
        for t in range(1, years):
            NPV = NPV + ((self.math_model(q, p, cv, f)) / ((1 - i) ** t))
        NPV = NPV + (self.math_model(q, p, cv, f) + sn) / ((1 - i) ** years) - self.start_up_investment
        return NPV

    # PI
    def rate_of_return(self, q, f, r, p, cv):
        PI = 0
        i = r / 100
        for t in range(1, years + 1):
            PI = PI + ((self.math_model(q, p, cv, f)) / ((1 + i) ** t))
        PI = PI / self.start_up_investment
        return PI

    def calculate_irr(self, i):
        e = [self.CF[i] for number in range(years)]
        l = [(-1)*self.start_up_investment]
        final_list = [*l, *e]
        return round(npf.irr(final_list), 2)

    def solution_model(self):
        q = self.output_volume.distribution()
        f = self.fixed_costs.distribution()
        r = self.discount_rate.distribution()
        p = self.price_for_one.distribution()
        cv = self.variable_costs.distribution()
        sn = self.residual_value.distribution()

        for i in range(size):
            self.CF.append(self.math_model(q[i], p[i], cv[i], f[i]))
            self.NPV.append(self.net_present_value(q[i], f[i], r[i], p[i], cv[i], sn[i]))
            self.PI.append(self.rate_of_return(q[i], f[i], r[i], p[i], cv[i]))
            self.irr.append(self.calculate_irr(i))

   # https: // docs.python.org / 3.4 / library / statistics.html  # statistics.median
   # https://tproger.ru/translations/basic-statistics-in-python-descriptive-statistics/

    def print_cf_npv_pi(self):
        print("N  |   CF   |    NPV   |    PI   ")
        for i in range(size):
            print(str(i) + " | " + str(self.CF[i]) + " | " + str(self.NPV[i]) + " | " + str(self.PI[i]) +\
                  " | " + str(self.irr[i]))
