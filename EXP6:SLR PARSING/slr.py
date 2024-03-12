import copy

# Perform grammar augmentation
def grammarAugmentation(rules, nonterm_userdef, start_symbol):
    newRules = []
    newChar = start_symbol + "'"
    while newChar in nonterm_userdef:
        newChar += "'"

    newRules.append([newChar, ['.', start_symbol]])

    for rule in rules:
        k = rule.split("->")
        lhs = k[0].strip()
        rhs = k[1].strip()
        multirhs = rhs.split('|')
        for rhs1 in multirhs:
            rhs1 = rhs1.strip().split()
            rhs1.insert(0, '.')
            newRules.append([lhs, rhs1])
    return newRules

# Find closure
def findClosure(input_state, dotSymbol):
    global start_symbol, separatedRulesList, statesDict
    closureSet = []

    if dotSymbol == start_symbol:
        for rule in separatedRulesList:
            if rule[0] == dotSymbol:
                closureSet.append(rule)
    else:
        closureSet = input_state

    prevLen = -1
    while prevLen != len(closureSet):
        prevLen = len(closureSet)
        tempClosureSet = []
        for rule in closureSet:
            indexOfDot = rule[1].index('.')
            if rule[1][-1] != '.':
                dotPointsHere = rule[1][indexOfDot + 1]
                for in_rule in separatedRulesList:
                    if dotPointsHere == in_rule[0] and in_rule not in tempClosureSet:
                        tempClosureSet.append(in_rule)
        for rule in tempClosureSet:
            if rule not in closureSet:
                closureSet.append(rule)
    return closureSet

# Compute GOTO
def compute_GOTO(state):
    global statesDict, stateCount
    generateStatesFor = []
    for rule in statesDict[state]:
        if rule[1][-1] != '.':
            indexOfDot = rule[1].index('.')
            dotPointsHere = rule[1][indexOfDot + 1]
            if dotPointsHere not in generateStatesFor:
                generateStatesFor.append(dotPointsHere)
    if len(generateStatesFor) != 0:
        for symbol in generateStatesFor:
            GOTO(state, symbol)

# GOTO
def GOTO(state, charNextToDot):
    global statesDict, stateCount, stateMap
    newState = []
    for rule in statesDict[state]:
        indexOfDot = rule[1].index('.')
        if rule[1][-1] != '.':
            if rule[1][indexOfDot + 1] == charNextToDot:
                shiftedRule = copy.deepcopy(rule)
                shiftedRule[1][indexOfDot] = shiftedRule[1][indexOfDot + 1]
                shiftedRule[1][indexOfDot + 1] = '.'
                newState.append(shiftedRule)
    addClosureRules = []
    for rule in newState:
        indexDot = rule[1].index('.')
        if rule[1][-1] != '.':
            closureRes = findClosure(newState, rule[1][indexDot + 1])
            for rule in closureRes:
                if rule not in addClosureRules and rule not in newState:
                    addClosureRules.append(rule)
    for rule in addClosureRules:
        newState.append(rule)
    stateExists = -1
    for state_num in statesDict:
        if statesDict[state_num] == newState:
            stateExists = state_num
            break
    if stateExists == -1:
        stateCount += 1
        statesDict[stateCount] = newState
        stateMap[(state, charNextToDot)] = stateCount
    else:
        stateMap[(state, charNextToDot)] = stateExists

# Generate states
def generateStates(statesDict):
    prev_len = -1
    called_GOTO_on = []
    while len(statesDict) != prev_len:
        prev_len = len(statesDict)
        keys = list(statesDict.keys())
        for key in keys:
            if key not in called_GOTO_on:
                called_GOTO_on.append(key)
                compute_GOTO(key)

# Calculation of FIRST
def first(rule):
    global diction
    if len(rule) != 0 and (rule is not None):
        if rule[0] in term_userdef:
            return rule[0]
        elif rule[0] == '#':
            return '#'
    if len(rule) != 0:
        if rule[0] in list(diction.keys()):
            fres = []
            rhs_rules = diction[rule[0]]
            for itr in rhs_rules:
                indivRes = first(itr)
                if type(indivRes) is list:
                    for i in indivRes:
                        fres.append(i)
                else:
                    fres.append(indivRes)
            if '#' not in fres:
                return fres
            else:
                fres.remove('#')
                if len(rule) > 1:
                    ansNew = first(rule[1:])
                    if ansNew is not None:
                        if type(ansNew) is list:
                            return fres + ansNew
                        else:
                            return fres + [ansNew]
                    else:
                        return fres
            fres.append('#')
            return fres

# Calculation of FOLLOW
def follow(nt):
    global diction
    solset = set()
    if nt == start_symbol:
        solset.add('$')
    for curNT in diction:
        rhs = diction[curNT]
        for subrule in rhs:
            if nt in subrule:
                while nt in subrule:
                    index_nt = subrule.index(nt)
                    subrule = subrule[index_nt + 1:]
                if len(subrule) != 0:
                    res = first(subrule)
                    if '#' in res:
                        res.remove('#')
                        ansNew = follow(curNT)
                        if ansNew is not None:
                            if type(ansNew) is list:
                                newList = res + ansNew
                            else:
                                newList = res + [ansNew]
                            res = newList
                    else:
                        if nt != curNT:
                            res = follow(curNT)
                if res is not None:
                    if type(res) is list:
                        for g in res:
                            solset.add(g)
                    else:
                        solset.add(res)
    return list(solset)

# Create parsing table
def createParseTable(statesDict, stateMap, T, NT):
    global separatedRulesList, diction
    rows = list(statesDict.keys())
    cols = T + ['$'] + NT
    Table = []
    tempRow = [''] * len(cols)
    for _ in range(len(rows)):
        Table.append(copy.deepcopy(tempRow))
