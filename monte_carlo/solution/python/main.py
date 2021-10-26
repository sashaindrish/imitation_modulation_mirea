from task_monte_carlo import task_monte_carlo

t = task_monte_carlo(0)

t.set_output_volume(5500, 270)
t.set_tax(0.4)
t.set_residual_value(0.00005)
t.set_depreciation(2000)
t.set_variable_costs(100, 160, 130)
t.set_discount_rate(16, 8)
t.set_fixed_costs(40000, 60000)
t.set_price_for_one(180,230,210)
t.set_start_up_investment(400000)

t.solution_model()
t.print_cf_npv_pi()
