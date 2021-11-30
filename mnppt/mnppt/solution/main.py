import smo2 as smo
import math

from tabulate import tabulate

def formula_a(t):  # время в часах
    return 15 + 10 * math.sin((3 * math.pi * t) / 24)


def formula_b(t):  # время в часах
    return 40 + 30 * math.sin(((4 * math.pi * t) / 24) - math.pi / 2)


def formula_c(t):  # время в часах
    return 100 - 50 * abs((6 - math.fmod(t, 12)) / 6)


def formula_d(t):  # время в часах
    if t >= 6:
        return 15 + 30 * (math.fmod(t, 12))
    else:
        return


hour_modulation = 24
round_n = 2
if __name__ == '__main__':

    PinH = 10  # клиенты в час / начало вариант б - 20 ч/ч
    avg_time_PinH = 60 / PinH  # среднее время интенсивности почступления заявок
    size = 1000  # огранечение посетителей
    avg_min = 5  # время на обслуживание (интенсивность обслуживания)
    final_stat = dict()

    end_num_bauer = 1
    t_kumulitive_end = 0.0

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
        print("Лямда в. а = ", lamda)

        (KZP, SDO, SVOvO, MaxLQ, SVPZvS, temp_stat, end_num_bauer,
        t_kumulitive_end) = smo.smo_model(avg_time_PinH, avg_min, size, 60, print_data=False, start_num_bauer=end_num_bauer,final_kum_time=t_kumulitive_end )
        print("Последний клиент ", end_num_bauer, "Время ", t_kumulitive_end)
        final_stat.update(temp_stat)
        #print(temp_stat)

    headers = ['№ клиента', 'Время поступ', 'Время обслуживания', 'Т кумулятив', 'Начало обслуживания',
               'конец обслуживания',
               'время в сист', 'время в очереди', '№ осбл. покуп', 'Длинна очереди', 'Время простоя']

    print(tabulate([(k,) + v for k, v in final_stat.items()], headers=headers))