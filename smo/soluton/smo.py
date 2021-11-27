import allocation as al
import random
import math
PinH = 10 # клиенты в час
avg_time_PinH = 60/PinH # среднее время
avg_min = 5  # время на обслуживание

if __name__ == '__main__':
    random.seed(12045)
    duration_of_service = al.exponential_distribution(scale=avg_min, nums=100, print_graph=False) # ожидание обслуживания
    clients = al.exponential_distribution(scale=avg_time_PinH, nums=100, print_graph=False) # приход клиентов время прихода каждого

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
    for i in range(len(t_kumulitive_list)):
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
    for i in range(1, len(t_kumulitive_list)):
        if t_kumulitive_list[i] > t_end_service[i-1]:
            t_start_service.append(t_kumulitive_list[i]) # error
        else:
            t_start_service.append(t_end_service[i-1])
    print("Время начало обслуживания = \n",t_end_service )


