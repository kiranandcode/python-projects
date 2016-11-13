import math
inputArray = [1677, 1018, 1816, 572, 912, 1944, 1843, 369, 1591, 1231, 1354, 1429, 110, 1000, 1144, 791, 667, 1092, 1495, 1878, 1020, 1607, 674, 231, 985, 530, 1378, 1664, 246, 850, 1732, 504, 247, 491, 1466, 529, 799, 1422, 981, 1599, 636, 811, 23, 133, 1964, 1679, 643, 550, 48, 910]

def merge(a, b):
    result = []
    A = False
    B = False
    counter = 0
    while True:
        counter += 1
        if len(a) > 0 and not A:
            aVal = a.pop(0)
            A = True
        if len(b) > 0 and not B:
            bVal = b.pop(0)
            B = True
        if not A and not B :
            break
        if A and B:
            if aVal < bVal:
                result.append(aVal)
                A = False
            else:
                result.append(bVal)
                B = False
        elif A:
            result.append(aVal)
            A = False
        elif B:
            result.append(bVal)
            B = False
    return result

def mergeSort(input = list):
    counter = 0
    if len(input) == 1:
        return input
    else:
        lowHalf = int(len(input)/2)
        counter += 1
        a = mergeSort(input[:lowHalf])
        b = mergeSort(input[lowHalf:])
        return merge(a, b)



print(mergeSort(inputArray))