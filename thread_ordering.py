threadA_commands = [
    "global x; x = 4",
    "global x; temp = x",
    "global x; x = 2 * temp"
    ]
threadB_commands = [
    "global x; x = 1",
    "global x; temp2 = x",
    "global x; x = temp2 - 1"
    ]

threadA = [(i, "threadA") for i in range(len(threadA_commands))]
threadB = [(i, "threadB") for i in range(len(threadB_commands))]

def findAllInterleavings(listA, listB):
    if not listA and listB:
        return [listB]
    if not listB and listA:
        return [listA]
    if not listA and not listB:
        return []
    headA, *tailA = listA
    headB, *tailB = listB
    finalresult = findAllInterleavings(tailA, tailB)
    removingAResult = findAllInterleavings(tailA, listB)
    removingBResult = findAllInterleavings(listA,tailB)


    removingB  = [[headB] + permutation for permutation in removingBResult]
    removingA  = [[headA] + permutation for permutation in removingAResult]
    removingBA = [[headB,headA] + permutation for permutation in finalresult]
    removingAB = [[headA,headB] + permutation for permutation in finalresult]

    result = removingB + removingA + removingAB + removingBA

    return result

x = 0
def getOutcome(commandList):
    path = []
    for command in commandList:
        statement = eval(command[1] + "_commands[{}]".format(command[0]))
        path.append(statement)
        exec(statement)
    return (x, path)


def printAllInterleavings():
    results = {}
    for interleaving in findAllInterleavings(threadA, threadB):
        result, statements = getOutcome(interleaving)
        results[result] = statements
    return sorted(list(results.items()),key=lambda x: x[0])

for result, value in printAllInterleavings():
	print("{} was produced by".format(result))
	for command in value:
		print("\t{}".format(command.split(';')[1]))


