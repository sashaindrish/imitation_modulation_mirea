import allocation as al
import random
from tabulate import tabulate
import math

PinH = 10  # клиенты в час
avg_time_PinH = 60 / PinH  # среднее время
avg_min = 5  # время на обслуживание
size = 100
round_n = 3

if __name__ == '__main__':
    print("Однокональная СМО \n")
    #################################################################################################
    # список покупателей
    list_bauers = list()
    for i in range(1, size + 1):
        list_bauers.append(i)
    #################################################################################################
    random.seed(10)
    duration_of_service = al.exponential_distribution(scale=avg_min, nums=size, print_graph=False)  # время обслуживания
    clients = al.exponential_distribution(scale=avg_time_PinH, nums=size,
                                          print_graph=False)  # время поступления клиента

    # print("ожидание обслуживания = \n", duration_of_service)
    # print("\nвремя прихода клиентов = \n", clients)
    #################################################################################################
    # t пос кумулятивное
    t_kumulitive_list = list()  # время комулетивное
    t_kumulitive_list.append(round(clients[0], round_n))
    for i in range(1, size):
        t_kumulitive_list.append(round(clients[i] + t_kumulitive_list[i - 1], round_n))
    # print("время поступления комулятивное = \n", t_kumulitive_list)
    #################################################################################################
    # время окончания обслуживания
    #
    t_end_service = list()
    for i in range(size):
        t_kum = t_kumulitive_list[i]
        t_serv = duration_of_service[i]
        # print(t_kum, "  ", t_serv, "Time")
        t_end_service.append(round((t_kum + t_serv), round_n))
    # print("Время окончания обслуживания = \n", t_end_service)
    #################################################################################################
    # t начало обслуживания, осслуживание начинается после завершение предидущих, первый ослуживается сразу(время прихода)
    #
    t_start_service = list()
    t_start_service.append(t_kumulitive_list[0])
    for i in range(1, size):
        if t_kumulitive_list[i] > t_end_service[i - 1]:
            t_start_service.append(t_kumulitive_list[i])
        else:
            t_start_service.append(t_end_service[i - 1])
        if (t_end_service[i - 1] + duration_of_service[i] > t_end_service[i]):
            t_end_service[i] = t_end_service[i - 1] + duration_of_service[i]
    # print("Время начало обслуживания = \n", t_start_service )
    #################################################################################################
    # Время в системе разница между временим поступления и обслуживанием
    #
    system_in_time = list()
    for i in range(size):
        system_in_time.append(round(t_end_service[i] - t_kumulitive_list[i], round_n))
    # print("Время в системе = \n", system_in_time)
    #################################################################################################
    # время в очереди
    time_in_queue = list()
    for i in range(size):
        time_in_queue.append(round(t_start_service[i] - t_kumulitive_list[i], round_n))
    # print("Время в очереди = \n", time_in_queue)
    #################################################################################################
    # определяем номер предидущего обслуженного покупателя в момент прихода следующего
    num_obs = [i for i in range(size)]
    
    # print(num_obs)
    for i in range(1, size):
        if time_in_queue[i] > 0:
            for j in reversed(range(i-1)):
                if t_start_service[j] <= round(t_kumulitive_list[i], round_n) < t_end_service[j]:
                    num_obs[i] = j+1
    #################################################################################################
    # определяем длинну очереди 
    len_queue = list()
    for i in range(0, size):
        len_queue.append(list_bauers[i] - num_obs[i] -1)
    #################################################################################################
    # определяем время простоя

    downtime=list()
    downtime.append(t_kumulitive_list[0])
    for i in range(1, size):
        if t_end_service[i-1] < t_start_service[i]:
            downtime.append(round(t_start_service[i]-t_start_service[i-1], round_n))
        else:
            downtime.append(0)
#################################################################################################
# Таблица на печать
    all_stat = dict()

    for i in range(size):
        all_stat.update({list_bauers[i]: (
        round(clients[i], round_n), round(duration_of_service[i], round_n), t_kumulitive_list[i], t_start_service[i],
        t_end_service[i], system_in_time[i], time_in_queue[i], num_obs[i], len_queue[i], downtime[i])})
    headers = ['№ клиента', 'Время поступ', 'Время обслуживания', 'Т кумулятив', 'Начало обслуживания',
               'конец обслуживания',
               'время в сист', 'время в очереди','№ осбл. покуп', 'Длинна очереди', 'Время простоя']

    print(tabulate([(k,) + v for k, v in all_stat.items()], headers=headers))
#################################################################################################
#
    for i in range(size):
        all_stat.update({list_bauers[i]: (
            round(clients[i], round_n), round(duration_of_service[i], round_n), t_kumulitive_list[i])})
#################################################################################################
# подведение итогов
    print("\n Основные параметры системы \n")
    print("Коэфициент загружености продавца = ", round(1 - sum(downtime)/t_end_service[size-1], 3))
    print("Средняя длинна очереди = ", round(sum(len_queue)/size,3))
    print("Среднее время ожидания в очереди = ", round(sum(time_in_queue)/size, round_n))
    print("Максимальная длинна в очереди = ", max(len_queue))
    print("Среднее время пребывания заявок в системе = ", round(sum(system_in_time)/size, round_n))