import copy

# perform grammar augmentation
def grammarAugmentation(rules, nonterm_userdef, start_symbol):
    # newRules stores processed output rules
    newRules = []

    # create unique 'symbol' to represent new start symbol
    newChar = start_symbol + "'"
    while (newChar in nonterm_userdef):
        newChar += "'"

    # adding rule to bring start symbol to RHS
    newRules.append([newChar, ['.', start_symbol]])

    # new format => [LHS,[.RHS]], can't use dictionary since duplicate keys can be there
    for rule in rules:
        # split LHS from RHS
        k = rule.split("->")
        lhs = k[0].strip()
        rhs = k[1].strip()

        # split all rule at '|', keep single derivation in one rule
        multirhs = rhs.split('|')
        for rhs1 in multirhs:
            rhs1 = rhs1.strip().split()
            # ADD dot pointer at start of RHS
            rhs1.insert(0, '.')
            newRules.append([lhs, rhs1])
    return newRules

# find closure
def findClosure(input_state, dotSymbol):
    global start_symbol, separatedRulesList, statesDict

    # closureSet stores processed output
    closureSet = []

    # if findClosure is called for 1st time i.e. for I0, then LHS is received in "dotSymbol",
    # add all rules starting with LHS symbol to closureSet
    if dotSymbol == start_symbol:
        for rule in separatedRulesList:
            if rule[0] == dotSymbol:
                closureSet.append(rule)
    else:
        # for any higher state than I0, set initial state as received input_state
        closureSet = input_state

    # iterate till new states are getting added in closureSet
    prevLen = -1
    while prevLen != len(closureSet):
        prevLen = len(closureSet)
        # "tempClosureSet" - used to eliminate concurrent modification error
        tempClosureSet = []
        # if dot pointing at new symbol, add corresponding rules to tempClosure
        for rule in closureSet:
            indexOfDot = rule[1].index('.')
            if rule[1][-1] != '.':
                dotPointsHere = rule[1][indexOfDot + 1]
                for in_rule in separatedRulesList:
                    if dotPointsHere == in_rule[0] and in_rule not in tempClosureSet:
                        tempClosureSet.append(in_rule)

        # add new closure rules to closureSet
        for rule in tempClosureSet:
            if rule not in closureSet:
                closureSet.append(rule)
    return closureSet

# Other functions will go here

# *** MAIN *** - Driver Code
# example sample set 01
rules = ["E -> E + T | T",
         "T -> T * F | F",
         "F -> ( E ) | id"
         ]
nonterm_userdef = ['E', 'T', 'F']
term_userdef = ['id', '+', '*', '(', ')']
start_symbol = nonterm_userdef[0]

print("\nOriginal grammar input:\n")
for y in rules:
    print(y)

# print processed rules
print("\nGrammar after Augmentation: \n")
separatedRulesList = grammarAugmentation(rules, nonterm_userdef, start_symbol)
for rule in separatedRulesList:
    print(rule)

# find closure
start_symbol = separatedRulesList[0][0]
print("\nCalculated closure: I0\n")
I0 = findClosure(0, start_symbol)
for rule in I0:
    print(rule)

# Rest of the code will go here
