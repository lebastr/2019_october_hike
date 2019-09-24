from members import *

import numpy as np
import pandas as pd
import datetime
from collections import Counter


def food_planning(food, NBreakfast, NDinner, NLunch, NSnack, WomanFoodMaxWeight):
    names_counter = Counter()
    total_weight = 0.0

    for m in Members.values():
        m.food = []

    tbl = []

    for row in food:
        one_portion_weight = float(row[1])
        portion_weight = one_portion_weight * NMembers
        times = float(row[2])
        weight = portion_weight * times

        total_weight += weight

        assert len(row) == 3 or len(row) == 4
        names_counter[row[0]] += 1
        assert names_counter[row[0]] <= 1



        if len(row) == 3:
            tbl.append({'name': row[0],
                    'portion': portion_weight,
                    'times': times,
                    'weight': weight})

        else:
            if isinstance(row[3], Member):
                member = row[3]
                assert member.name in MembersList
                member.food.append({'kind' : 'food', 'packing_weight': portion_weight,
                                    'weight' : weight, 'name' : row[0]})

                tbl.append({'name': row[0],
                    'portion': portion_weight,
                    'times': times,
                    'weight': weight, 'Кто несет': member.name})
            else:
                members, ks = row[3]
                assert np.sum(ks) - times < 1e-9, print(np.sum(ks), times)
                assert len(members) == len(ks)
                assert len(members) > 1

                for member, k in zip(members, ks):
                    assert member.name in MembersList
                    member.food.append({'kind' : 'food', 'packing_weight': portion_weight,
                                        'weight' : portion_weight * k, 'name' : row[0]})

                    tbl.append({'name': row[0],
                                'portion': portion_weight,
                                'times': k,
                                'weight': portion_weight * k, 'Кто несет': member.name})

                if np.sum(ks) < times - 1e-9:
                    # Есть нераспределенное снаряжение
                    tbl.append({'name': row[0],
                                'portion': portion_weight,
                                'times': times - np.sum(ks),
                                'weight': portion_weight * (times - np.sum(ks))})


    print("Общий вес: {}".format(total_weight))

    avg = (total_weight - WomanFoodMaxWeight * NWomans) / (NMembers - NWomans)
    print("Средний вес на мужчину: {}".format(avg))
    print("Средний вес на женщину: {}".format(WomanFoodMaxWeight))
    print("Вес на человека в день: {}\n".format(total_weight / NMembers / ((NBreakfast + NDinner + NSnack + NLunch) / 4)))

    cur_weight = 0.0
    for name, member in sorted(Members.items()):
        w = np.sum([r['weight'] for r in member.food])
        cur_weight += w
        if name in Womans:
            d = WomanFoodMaxWeight - w
        else:
            d = avg - w

        print("{}: {}".format(name, d))

    print("\nОстаток: {}".format(total_weight - cur_weight))

    table = pd.DataFrame(data=tbl)
    return table


def group_by_members(table, fname=None):
    for a, b in table.groupby(['Кто несет']):
            print("Участник: {}, несет: {}".format(a, b['weight'].sum()))
            print(str(b))
            print("\n\n")

    if fname is not None:
        with open("food.txt", 'w') as f:
            f.write("Дата создания: {}\n\n".format(datetime.datetime.now()))
            for a, b in table.groupby(['Кто несет']):
                f.write("Участник: {}, несет: {}\n".format(a, b['weight'].sum()))
                f.write(str(b))
                f.write("\n\n")

            f.write("\nСводная таблица\n")
            f.write(str(table))