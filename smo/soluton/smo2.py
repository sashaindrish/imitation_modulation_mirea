import allocation as al
import random
from tabulate import tabulate
import math

round_n = 3


def smo_model(avg_time_PinH, avg_min, size, time, print_data=True):
    index_stop = None
    #################################################################################################
    # список покупателей
    list_bauers = list()
    for i in range(1, size + 1):
        list_bauers.append(i)
    #################################################################################################
    random.seed(105531)
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

    if time != None:
        for i in range(size):
            if t_kumulitive_list[i] >= time:
                index_stop = i
                break
        if (index_stop == None):
            index_stop = size
        print("Ограничение по времени (мин) = ", time)
        print("Пcледний клиент по времени = ", index_stop)

        for i in range(index_stop, size):
            clients[i] = None
            duration_of_service[i] = None
            t_kumulitive_list[i] = None

        size = index_stop
    #################################################################################################
    #################################################################################################
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
            for j in reversed(range(i - 1)):
                if t_start_service[j] <= round(t_kumulitive_list[i], round_n) < t_end_service[j]:
                    num_obs[i] = j + 1
    #################################################################################################
    # определяем длинну очереди
    len_queue = list()
    for i in range(0, size):
        len_queue.append(list_bauers[i] - num_obs[i] - 1)
    #################################################################################################
    # определяем время простоя

    downtime = list()
    downtime.append(t_kumulitive_list[0])
    for i in range(1, size):
        if t_end_service[i - 1] < t_start_service[i]:
            downtime.append(round(t_start_service[i] - t_start_service[i - 1], round_n))
        else:
            downtime.append(0)
    #################################################################################################
    # Таблица на печать
    all_stat = dict()

    for i in range(size):
        all_stat.update({list_bauers[i]: (
            round(clients[i], round_n), round(duration_of_service[i], round_n), t_kumulitive_list[i],
            t_start_service[i],
            t_end_service[i], system_in_time[i], time_in_queue[i], num_obs[i], len_queue[i], downtime[i])})

    headers = ['№ клиента', 'Время поступ', 'Время обслуживания', 'Т кумулятив', 'Начало обслуживания',
               'конец обслуживания',
               'время в сист', 'время в очереди', '№ осбл. покуп', 'Длинна очереди', 'Время простоя']
    if print_data:
        print(tabulate([(k,) + v for k, v in all_stat.items()], headers=headers))
    else:
        print("Итерация пройдена")
    #################################################################################################
    #
    for i in range(size):
        all_stat.update({list_bauers[i]: (
            round(clients[i], round_n), round(duration_of_service[i], round_n), t_kumulitive_list[i])})
    #################################################################################################
    # подведение итогов

    KZP = round(1 - sum(downtime) / t_end_service[size - 1], 3)
    SDO = round(sum(len_queue) / size, 3)
    SVOvO = round(sum(time_in_queue) / size, round_n)
    MaxLQ = max(len_queue)
    SVPZvS = round(sum(system_in_time) / size, round_n)

    return (KZP, SDO, SVOvO, MaxLQ, SVPZvS)


#################################################################################################

if __name__ == '__main__':
    print("Однокональная СМО \n Входные данные \n")

    PinH = 10  # клиенты в час / начало вариант б - 20 ч/ч
    avg_time_PinH = 60 / PinH  # среднее время интенсивности почступления заявок

    size = 100  # огранечение посетителей #вариант в 1000
    avg_min = 5  # время на обслуживание (интенсивность обслуживания)

    KZP = 0
    SDO = 4  # Средняя длинна очереди
    SVOvO = 10  # Среднее время ожидания в очереди
    MaxLQ = 0
    SVPZvS = 0

    print("Клиентов за час = ", PinH)
    print("Время на обслуживание (интенсивность обслуживания) =", avg_min)
    print("Интенсивность поступления = ", avg_time_PinH)
    print("Ограничение посетителей =", size)

    (KZP, SDO, SVOvO, MaxLQ, SVPZvS) = smo_model(avg_time_PinH, avg_min, size, None, True)

    # вариант а
    # print(" вариант а")
    # print("Среднее время ожидание в очереди должно быть меньше чем 5 ")
    # avg_min = 10
    # while SVOvO >= 5:
    #     avg_min = round(avg_min - 0.1, 2)
    #     (KZP, SDO, SVOvO, MaxLQ, SVPZvS) = smo_model(avg_time_PinH, avg_min, size, None, False)

    #################################################################################################
    # вариант Б
    # print(" вариант Б")
    # print("Средняя длинна очереди должна быть меньше чем 3 \n")
    # PinH = 20
    # while  SDO >= 3:
    #     PinH = round(PinH - 0.1, 2)  # клиенты в час
    #     avg_time_PinH = round(60 / PinH, 2) # среднее время интенсивности почступления заявок
    #     (KZP, SDO, SVOvO, MaxLQ, SVPZvS) = smo_model(avg_time_PinH, avg_min, size, time=None, print_data=False)
    # print()
    #################################################################################################
    # вариант B
    # print(" вариант B")
    # print("1000 клиентов ограничение \n")
    # size = 1000
    # (KZP, SDO, SVOvO, MaxLQ, SVPZvS) = smo_model(avg_time_PinH, avg_min, size, time=None, print_data=True)
    # print()
    #################################################################################################
    # вариант Г
    # print(" вариант Г")
    # print(" Ограничение по времени 10 часов")
    # hour = 10
    # (KZP, SDO, SVOvO, MaxLQ, SVPZvS) = smo_model(avg_time_PinH, avg_min, size, time=hour*60)

    print("Выходные данные :")

    print("Клиентов за час = ", PinH)
    print("Время на обслуживание (интенсивность обслуживания) =", avg_min)
    print("Интенсивность поступления = ", avg_time_PinH)
    # print("Ограничение посетителей =", size)

    print("\n Основные параметры системы \n")

    print("Коэфициент загружености продавца = ", KZP)
    print("Средняя длинна очереди = ", SDO)
    print("Среднее время ожидания в очереди = ", SVOvO)
    print("Максимальная длинна в очереди = ", MaxLQ)
    print("Среднее время пребывания заявок в системе = ", SVPZvS)
