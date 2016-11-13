inputArray = [1677, 1018, 1816, 572, 912, 1944, 1843, 369, 1591, 1231, 1354, 1429, 110, 1000, 1144, 791, 667, 1092, 1495, 1878, 1020, 1607, 674, 231, 985, 530, 1378, 1664, 246, 850, 1732, 504, 247, 491, 1466, 529, 799, 1422, 981, 1599, 636, 811, 23, 133, 1964, 1679, 643, 550, 48, 910]




def quickSort(inputArr = list):

    if len(inputArr) <= 1:
        return inputArr
    pivot = inputArr.pop()
    counter = 0;

    for i in range(len(inputArr)):

        if inputArr[i] < pivot:

            temp = inputArr[counter]
            inputArr[counter] = inputArr[i]
            inputArr[i] = temp
            counter += 1

    if counter != len(inputArr):
        temp = inputArr[counter]
        inputArr.append(temp)
        inputArr[counter] = pivot

        inputArr[:counter] = quickSort(inputArr[:counter])
        inputArr[counter:] = quickSort(inputArr[counter:])
    else:
        inputArr.append(pivot)
        inputArr[:counter] = quickSort(inputArr[:counter])
    return inputArr


print(quickSort(inputArray))