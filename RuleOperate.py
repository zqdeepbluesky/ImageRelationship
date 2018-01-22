# -*-coding:utf-8-*-

'''
This script was created for processing the rule txt file
'''


def ReadRules(rulename='rules.txt'):
    rules = []
    with open(rulename, 'r') as f:
        title = f.readline().strip().split(',')
        ruletxt = f.readlines()
        for rule in ruletxt:
            rules.append(rule.strip().split(','))
    return title, rules


def WriteRules(title, rules, rulename='rules.txt'):
    with open(rulename, 'w') as f:
        f.write(",".join(title) + "\n")
        for rule in rules:
            f.write(",".join(rule) + "\n")


def Compare(contents, rules):
    relation = contents[0]
    personset = contents[1]
    defaultAction = 'Accept'
    defaultLevel = 0
    for rule in rules:
        Action = rule[0]
        Object1 = rule[1]
        Object2 = rule[2]
        Relationship = rule[3]
        Level = rule[4]
        if (Object1 in personset and Object2 in personset) \
                or (Object1 in personset and '*' == Object2) \
                or (Object2 in personset and '*' == Object1):
            if relation == Relationship:
                print rule
                return Action, Level
    return defaultAction, defaultLevel


if __name__ == "__main__":
    contents = ['hands', set(['Alice', 'Bob'])]
    title, rules = ReadRules()
    print Compare(contents, rules)
