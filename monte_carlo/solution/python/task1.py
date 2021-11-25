from task_monte_carlo import task_monte_carlo
import random


def task():
    random.seed(23051993)
    print("Вариант: ", random.randint(1, 12))

    # example = task_monte_carlo(0)
    #
    # example.set_output_volume(5500, 270)
    # example.set_tax(0.4)
    # example.set_residual_value(0.00005)
    # example.set_depreciation(2000)
    # example.set_variable_costs(100, 160, 130)
    # example.set_discount_rate(16, 8)
    # example.set_fixed_costs(40000, 60000)
    # example.set_price_for_one(180, 230, 210)
    # example.set_start_up_investment(400000)
    #
    # example.solution_model()
    # example.print_cf_npv_pi()
    # example.print_statistics()
    random.seed(23051993)
    t = task_monte_carlo(6)
    
    t.set_output_volume(6700, 450)
    t.set_tax(0.4)
    t.set_residual_value(0.00007)
    t.set_depreciation(2500)
    t.set_variable_costs(100, 160, 130)
    t.set_discount_rate(14.5, 6.5)
    t.set_fixed_costs(40000, 60000)
    t.set_price_for_one(180, 230, 210)
    t.set_start_up_investment(500000)

    t.solution_model()
    t.print_cf_npv_pi()
    t.print_statistics()
