from members import *
from collections import Counter
import pandas as pd
import datetime
import numpy as np


def equipment_planning(SharedEquipment):
    names_counter = Counter()
    undistributed = []
    total_weight = 0.0

    for m in Members.values():
        m.equipment = []

    tbl = []

    for row in SharedEquipment:
        weight = float(row[2])
        total_weight += weight

        assert len(row) == 3 or len(row) == 4
        names_counter[row[0]] += 1
        assert names_counter[row[0]] <= 1

        if len(row) == 3:
            undistributed.append(row)

        else:
            member = row[3]
            assert member.name in MembersList
            member.equipment.append({'kind': 'equipment', 'weight': weight, 'name': row[0], 'owner': row[1]})
            tbl.append({'name': row[0], 'weight': weight, 'Кто несет': member.name})

    print("Общий вес: {}".format(total_weight))

    avg = (total_weight - WomanShareEqMaxWeight * NWomans) / (NMembers - NWomans)
    print("Средний вес на мужчину: {}".format(avg))
    print("Средний вес на женщину: {}\n".format(WomanShareEqMaxWeight))

    rest = 0
    for name, member in sorted(Members.items()):
        w = np.sum([r['weight'] for r in member.equipment])
        if name in Womans:
            d = WomanShareEqMaxWeight - w
        else:
            d = avg - w

        rest += d
        print("{}: {}".format(name, d))

    print("\nОстаток: {}\n".format(rest))
    table = pd.DataFrame(data=tbl)
    return table


def group_by_members(table):
    for a, b in table.groupby(['Кто несет']):
            print("Участник: {}, несет: {}".format(a, b['weight'].sum()))
            print(str(b))
            print("\n\n")

    with open("equipment.txt", 'w') as f:
        f.write("Дата создания: {}\n\n".format(datetime.datetime.now()))
        for a, b in table.groupby(['Кто несет']):
            f.write("Участник: {}, несет: {}\n".format(a, b['weight'].sum()))
            f.write(str(b))
            f.write("\n\n")

        f.write("\nСводная таблица")
        f.write(str(table))