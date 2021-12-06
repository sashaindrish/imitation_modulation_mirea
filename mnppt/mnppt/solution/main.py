import smo2 as smo
import math

from tabulate import tabulate

def formula_a(t):  # время 
    return 15 + 10 * math.sin((3 * math.pi * t) / 24)


def formula_b(t):  # время
    return 40 + 30 * math.sin(((4 * math.pi * t) / 24) - math.pi / 2)


def formula_c(t):  # время 
    return 100 - 50 * abs((6 - math.fmod(t, 12)) / 6)


def formula_d(t):  # время 
    if t >= 6:
        return 15 + 30 * (math.fmod(t, 12))
    else:
        return


hour_modulation = 24
round_n = 2
if __name__ == '__main__':

    PinH = 10  # запросы в 1 времени 
    avg_time_PinH = 60 / PinH  # среднее время интенсивности поступления заявок
    size = 1000  # огранечение запросов
    avg_min = 5  # время на обслуживание (интенсивность обслуживания)
    final_stat = dict()

    end_num_bauer = 1
    t_kumulitive_end = 0.0

    KZP=0
    SDO=0
    SVOvO=0
    MaxLQ = list()
    SVPZvS=0
    aavg_time_PinH = 0
    for i in range(hour_modulation):
        # Вариант а
        lamda = round(formula_a(i), round_n)
        # Вариант б
        #lamda = round(formula_b(i), round_n)
        # Вариант в
        #lamda = round(formula_c(i), round_n)
        # Вариант г
        #i=i+6
        #lamda = round(formula_d(i), round_n)

        avg_time_PinH = round(60 / lamda, round_n)
        print("Лямда = ", lamda)

        (KZPt, SDOt, SVOvOt, MaxLQt, SVPZvSt, temp_stat, end_num_bauer,
        t_kumulitive_end) = smo.smo_model(avg_time_PinH, avg_min, size, 60, print_data=False, start_num_bauer=end_num_bauer,final_kum_time=t_kumulitive_end )
        KZP += KZPt
        SDO += SDOt
        SVOvO += SVOvOt
        MaxLQ.append(MaxLQt)
        SVPZvS += SVPZvSt
        aavg_time_PinH +=avg_time_PinH

        final_stat.update(temp_stat)
        #print(temp_stat)

    headers = ['№ запроса', 'Время поступ', 'Время обслуживания', 'Т кумулятив', 'Начало обслуживания',
               'конец обслуживания',
               'время в сист', 'время в очереди', '№ осбл. заявки', 'Длинна очереди', 'Время простоя']

    print(tabulate([(k,) + v for k, v in final_stat.items()], headers=headers))

    print("Выходные данные :")

    print("Cреднее время интенсивности почступления заявок (временных единиц)= ", round(aavg_time_PinH/hour_modulation, round_n))
    print("Время на обслуживание (интенсивность обслуживания) =", avg_min)


    print("\n Основные параметры системы \n")

    print("Время потраченное на обслуживание(временных единиц) =",t_kumulitive_end)
    print("Коэфициент загружености IP-блока = ", round(KZP/hour_modulation, round_n))
    print("Средняя длинна очереди (запросов) = ", round(SDO/hour_modulation, round_n))
    print("Среднее время ожидания в очереди (временных единиц) = ", round(SVOvO/hour_modulation, round_n))
    print("Максимальная длинна в очереди (запросов) = ", max(MaxLQ))
    print("Среднее время пребывания заявок в системе (временных единиц) = ", round(SVPZvS/hour_modulation, round_n))
