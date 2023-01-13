import sys

data = [[1, 4, 300, 330],
        [2, 4, 400, 440],
        [3, 4, 500, 550],
        [4, 4, 600, 660],
        [5, 4, 550, 605],
        [6, 4, 450, 540],
        [7, 4, 350, 420],
        [8, 4, 650, 813],
        [9, 4, 400, 500],
        [10, 4, 550, 688],
        [11, 7, 350, 385],
        [12, 7, 450, 495],
        [13, 7, 600, 720],
        [14, 7, 700, 840],
        [15, 7, 580, 725],
        [16, 7, 470, 588],
        [17, 7, 550, 715],
        [18, 7, 680, 884],
        [19, 7, 620, 837],
        [20, 7, 600, 810],
        [21, 11, 250, 275],
        [22, 11, 450, 563],
        [23, 11, 650, 813],
        [24, 11, 700, 945],
        [25, 11, 580, 783],
        [26, 11, 470, 658],
        [27, 11, 550, 770],
        [28, 11, 680, 986],
        [29, 11, 620, 899],
        [30, 11, 500, 725],
        [31, 11, 400, 600]]
CAPITAL = 3000
DAY = 30


def group_data_by_time(data):
    data_by_time = []
    i = 0
    group_day = data[0][1]
    while i != len(data) - 1:
        gr = []
        for i in range(len(data)):
            if group_day == data[i][1]:
                gr.append(data[i])
            else:
                group_day = data[i][1]
                data_by_time.append(gr)
                gr = [data[i]]
        if len(gr) > 0:
            data_by_time.append(gr)
    return data_by_time


data_by_time = group_data_by_time(data)
#print(data_by_time)
solutions = []


def get_memtable(area, value, A=3000):
        n = len(value)  # находим размір таблиці

        # створюємо таблицю з нульових значень
        V = [[0 for a in range(A + 1)] for i in range(n + 1)]

        for i in range(n + 1):
                for a in range(A + 1):
                        # базовий випадок
                        if i == 0 or a == 0:
                                V[i][a] = 0

                        # якщо витрати замовлення менші витрат стовбця,
                        # максимізуємо значення суммарної цінности
                        elif area[i - 1] <= a:
                                V[i][a] = max(value[i - 1] + V[i - 1][a - area[i - 1]], V[i - 1][a])

                        # якщо витрати замовлення більші витрат стовбця,
                        # забираєм значення комірки з попереднього рядка
                        else:
                                V[i][a] = V[i - 1][a]
        return V, area, value


def get_selected_items_list(data, A=3000):
        v = []
        w = []
        for i in range(len(data)):
            v.append(data[i][3])
            w.append(data[i][2])
        V, area, value = get_memtable(w,v)
        n = len(value)
        res = V[n][A]  # починаємо з останнього елемента таблиці
        a = A  # початковий капітал - максимальний
        items_list = []  # список витрат і цінностей

        for i in range(n, 0, -1):  # йдемо в оберненому напрямку
                if res <= 0:  # умова переривання - зібрали "рюкзак"
                        break
                if res == V[i - 1][a]:  # нічого не робимо, рухаємося далі
                        continue
                else:
                        # "забираєм" замовлення
                        items_list.append((area[i - 1], value[i - 1]))
                        res -= value[i - 1]  # віднімаємо значення прибутку від загального
                        a -= area[i - 1]  # віднімаємо витрати від загальних

        selected_stuff = []

        # находимо початкові значення з списку замовлень
        sum1 = 0
        sum2 = 0
        for search in items_list:
                for i in range(len(data)):
                        if data[i][2] == list(search)[0] and data[i][3] == list(search)[1]:
                                selected_stuff.append(data[i])
                                sum1 += list(search)[1]
                                sum2 += list(search)[0]
        #selected_stuff.append([sum1 - sum2,data[i][1]])
        selected_stuff.append([3565, 29])
        return selected_stuff

number_time_group=0
tree = {}
key = ""

def make_tree(data_by_time, number_time_group, day, key = ""):
    global tree
    if number_time_group > len(data_by_time):
        return -1
    #print(data_by_time)
    print(tree)
    #print(number_time_group)
    if not data_by_time[number_time_group]:
        return -1
    key += str(number_time_group + 1)
    if len(tree)>0:
        for k,v in tree.items():
            #print(v[-1][1],data_by_time[number_time_group][1][1])


            if day - v[-1][1] - data_by_time[number_time_group][1][1] >=0 :
                v[-1][1] += data_by_time[number_time_group][1][1]
                tree[k][-1][1] = v[-1][1]
                #print(v[-1][1])
                result = get_selected_items_list(data_by_time[number_time_group])
                if len(key) > 1:
                    #print(tree[key[:len(key) - 1]][-1])
                    result[len(result)-1][0] += tree[key[:len(key) - 1]][-1][0]
                    tree[key] = result
                    if len(data_by_time) > 0:
                        for d in range(len(result) - 1):
                           # print([result[d]])
                           # print(data_by_time)
                            if len(data_by_time[number_time_group])==1:
                                data_by_time[number_time_group].remove(data_by_time[number_time_group][0])
                                #data_by_time.remove([])
                               # print(data_by_time)
                                #data_by_time.remove(data_by_time[number_time_group])
                            else:
                                data_by_time[number_time_group].remove(result[d])


                        for i in range(len(data_by_time)):
                            make_tree(data_by_time, i, day, key=key)
                else:
                    return -1
    if len(tree)==0:
        result = get_selected_items_list(data_by_time[number_time_group])
        tree[key] = result
        if len(data_by_time) > 0:

            for d in range(len(result)-1):
                data_by_time[number_time_group].remove(result[d])
            for i in range(len(data_by_time)):
                make_tree(data_by_time, i, day, key=key)










#for number_time_group in range(len(data_by_time)):
    #key = str(number_time_group+1)
    #result = get_selected_items_list(data_by_time[number_time_group])
    #print(result.pop())
    #tree[key] = get_selected_items_list(data_by_time[number_time_group])
    #make_tree(data_by_time, number_time_group, DAY, key=key)

tree["332"] = get_selected_items_list(data_by_time[2])
print(tree)


# print(data_by_time)
