class Member(object):
    def __init__(self, name):
        self.name = name
        self.equipment = []
        self.food = []
        
    def __repr__(self):
        return "<Person: name: {}>".format(self.name)

Womans = set(['Бубнова',
             'Виноградова',
             'Ткачева'])
Males = set(['Авраменко',
             'Герасимов',
             'Дятлов',
             'Еналеев',
             'Лебедев',
             'Малышев'])

assert len(Womans.intersection(Males)) == 0

MembersList = Womans.union(Males)

NMembers = len(MembersList)
NWomans = len(Womans)

Members = {}
for m in MembersList:
    s = "{} = Member('{}'); Members['{}'] = {}".format(m, m, m, m)
    exec(s)

print(MembersList)
    
print("Количество участников: {}".format(NMembers))
print("Количество женщин: {}".format(NWomans))
