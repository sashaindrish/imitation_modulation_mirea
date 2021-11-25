import allocation as al
import random
import math
PinH = 10 # клиенты в час
avg_time_PinH = 60/PinH # среднее время
avg_min = 5  # время между

if __name__ == '__main__':
    random.seed(12045)
    duration_of_service = al.exponential_distribution(scale=avg_min, nums=100, print_graph=False) # ожидание обслуживания
    clients = al.exponential_distribution(scale=avg_time_PinH, nums=100, print_graph=False) # приход клиентов

    print("ожидание обслуживания = \n", duration_of_service)
    print("\nвремя прихода клиентов = \n", clients)

    t_kumulitive = sum(clients)
    print("время поступления комулятивное = ", t_kumulitive)


    # for x

