import allocation as al
import random
import math
PinH = 10 # клиенты в час
avg_time_PinH = 60/PinH # среднее время
avg_min = 5  # время на обслуживание
size = 100

if __name__ == '__main__':
#################################################################################################
# список покупателей
    list_buers = list()
    for i in range(size):
        list_buers.append(i)
#################################################################################################
    random.seed(12045)
    duration_of_service = al.exponential_distribution(scale=avg_min, nums=size, print_graph=False) # время обслуживания
    clients = al.exponential_distribution(scale=avg_time_PinH, nums=size, print_graph=False) # время поступления клиента

    print("ожидание обслуживания = \n", duration_of_service)
    print("\nвремя прихода клиентов = \n", clients)
#################################################################################################
# t пос кумулятивное
    t_kumulitive_list = list() # время комулетивное
    sum = 0
    for t_ob in clients:
        sum +=t_ob
        t_kumulitive_list.append(round(sum, 2))
    print("время поступления комулятивное = \n", t_kumulitive_list)
#################################################################################################
# время окончания обслуживания
#
    t_end_service = list()
    for i in range(size):
        t_kum = t_kumulitive_list[i]
        t_serv = duration_of_service[i]
        #print(t_kum, "  ", t_serv, "Time")
        t_end_service.append(round((t_kum+t_serv), 2))
    print("Время окончания обслуживания = \n", t_end_service)
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
    print("Время начало обслуживания = \n", t_start_service )
#################################################################################################
# Время в системе разница между временим поступления и обслуживанием
#
    system_in_time = list()
    for i in range(size):
        system_in_time.append(round(t_end_service[i] - t_kumulitive_list[i], 2))
    print("Время в системе = \n", system_in_time)
#################################################################################################
# время в очереди
    time_in_queue = list()
    for i in range(size):
        time_in_queue.append(round(system_in_time[i] - duration_of_service[i], 3)) # ошибка
print("Время в очереди = \n", time_in_queue)
#################################################################################################
# определяем номер предидущего обслуженного покупателя в момент прихода следующего
#    number_buer_
