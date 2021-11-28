import allocation as al
import random
from tabulate import tabulate
import math
PinH = 10 # клиенты в час
avg_time_PinH = 60/PinH # среднее время
avg_min = 5  # время на обслуживание
size = 100

if __name__ == '__main__':
#################################################################################################
# список покупателей
    list_buers = list()
    for i in range(1, size+1):
        list_buers.append(i)
#################################################################################################
    random.seed(12045)
    duration_of_service = al.exponential_distribution(scale=avg_min, nums=size, print_graph=False) # время обслуживания
    clients = al.exponential_distribution(scale=avg_time_PinH, nums=size, print_graph=False) # время поступления клиента

    # print("ожидание обслуживания = \n", duration_of_service)
    # print("\nвремя прихода клиентов = \n", clients)
#################################################################################################
# t пос кумулятивное
    t_kumulitive_list = list() # время комулетивное
    t_kumulitive_list.append(round(clients[0], 2))
    for i in range(1, size):
        t_kumulitive_list.append(round(clients[i]+t_kumulitive_list[i-1], 2))
    # print("время поступления комулятивное = \n", t_kumulitive_list)
#################################################################################################
# время окончания обслуживания
#
    t_end_service = list()
    for i in range(size):
        t_kum = t_kumulitive_list[i]
        t_serv = duration_of_service[i]
        #print(t_kum, "  ", t_serv, "Time")
        t_end_service.append(round((t_kum+t_serv), 2))
    # print("Время окончания обслуживания = \n", t_end_service)
#################################################################################################
# t начало обслуживания, осслуживание начинается после завершение предидущих, первый ослуживается сразу(время прихода)
# если время
    t_start_service = list()
    t_start_service.append(t_kumulitive_list[0])
    for i in range(1, size):
        if t_kumulitive_list[i] > t_end_service[i-1]:
            t_start_service.append(t_kumulitive_list[i])
        else:
            t_start_service.append(t_end_service[i-1])
        if(t_end_service[i - 1] + duration_of_service[i] > t_end_service[i]):
            t_end_service[i] = t_end_service[i - 1] + duration_of_service[i]
    # print("Время начало обслуживания = \n", t_start_service )
#################################################################################################
# Время в системе разница между временим поступления и обслуживанием
#
    system_in_time = list()
    for i in range(size):
        system_in_time.append(round(t_end_service[i] - t_kumulitive_list[i], 2))
    # print("Время в системе = \n", system_in_time)
#################################################################################################
# время в очереди
    time_in_queue = list()
    for i in range(size):
        time_in_queue.append(round(t_start_service[i] - t_kumulitive_list[i], 3)) # ошибка
    # print("Время в очереди = \n", time_in_queue)
#################################################################################################
# определяем номер предидущего обслуженного покупателя в момент прихода следующего
    num_obs = list()
    for i in list_buers:
        if(t_kumulitive_list[i]==t_start_service[i]):
            num_obs.append(i)
        

    all_stat = dict()

    for i in range(size):
        all_stat.update({list_buers[i]: (round(clients[i],2) ,round(duration_of_service[i],2), t_kumulitive_list[i],t_start_service[i],
                                     t_end_service[i],system_in_time[i],time_in_queue[i] )})
    headers = ['№ клиента','Время поступ','Время обслуживания','Т кумулятив','Начало обслуживания','конец обслуживания',
               'время в сист','время в очереди']

    print(tabulate([(k,) + v for k,v in all_stat.items()], headers=headers))