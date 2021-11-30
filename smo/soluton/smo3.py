from statistics import mean

import ciw
from tabulate import tabulate


network = ciw.create_network(
    arrival_distributions=[ciw.dists.Exponential(rate=10 / 60)],
    service_distributions=[ciw.dists.Exponential(rate=5 / 60)],
    number_of_servers=[2]
)

ciw.seed(12455623)
simulation = ciw.Simulation(network)
simulation.simulate_until_max_customers(100)
recs = simulation.get_all_records()

stats = [['Коэф. загруженности работников', simulation.transitive_nodes[0].server_utilisation],
         ['Средняя длина очереди', mean([r.queue_size_at_arrival for r in recs])],
         ['Максимальная длина ожидания', max([r.queue_size_at_arrival for r in recs])],
         ['Средняя время ожидания', mean([r.waiting_time for r in recs])],
         ['Средняя время пребывания', mean([r.exit_date - r.arrival_date for r in recs])]]

print(tabulate(stats, headers=['Параметр системы', 'Значение'], floatfmt='.2f',
               tablefmt='pretty', numalign='right'))

clients_headers = ['№ клиента', 'Время прибытия', 'Время ожидания',
                   'Начало обслуживания', 'Конец обслуживания', 'Время обслуживания',
                   'Время в системе', 'Длина очереди']
clients_stats = []

for client in recs:
    clients_stats.append([
        client.id_number,
        client.arrival_date,
        client.waiting_time,
        client.service_start_date,
        client.service_end_date,
        client.service_time,
        client.exit_date - client.arrival_date,
        client.queue_size_at_arrival,
    ])

print(tabulate(clients_stats, headers=clients_headers, floatfmt='.2f',
               tablefmt='pretty', numalign='right'))