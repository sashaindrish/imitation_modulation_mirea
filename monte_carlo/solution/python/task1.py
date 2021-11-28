import random

from TaskMonteCarlo import TaskMonteCarlo


def execute():
    random.seed(13071995)
    variant = random.randint(1, 12)
    print("Вариант: ", variant)

    task = TaskMonteCarlo()

    task.set_variant(variant)
    task.set_output_volume(5500, 270)
    task.set_tax(0.4)
    task.set_residual_value(0.00005)
    task.set_depreciation(2000)
    task.set_variable_costs(100, 160, 130)
    task.set_discount_rate(8, 16)
    task.set_fixed_costs(40000, 60000)
    task.set_price_for_one(180, 230, 210)
    task.set_start_up_investment(400000)

    task.solution_model()
    task.print_cf_npv_pi()
    task.print_statistics()
