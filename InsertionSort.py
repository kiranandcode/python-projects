#array to be sorted
inputArray = [1677, 1018, 1816, 572, 912, 1944, 1843, 369, 1591, 1231, 1354, 1429, 110, 1000, 1144, 791, 667, 1092, 1495, 1878, 1020, 1607, 674, 231, 985, 530, 1378, 1664, 246, 850, 1732, 504, 247, 491, 1466, 529, 799, 1422, 981, 1599, 636, 811, 23, 133, 1964, 1679, 643, 550, 48, 910];
outputArray = list;

def createSorted():
    global inputArray;
    output = []
    if len(inputArray) > 1:
        if inputArray[0] < inputArray[1]:
            output.append(inputArray[0])
            output.append(inputArray[1])
            inputArray = inputArray[3:]
        else:
            output.append(inputArray[1])
            output.append(inputArray[0])
            inputArray = inputArray[3:]
    else:
        output.append(inputArray[0])
        inputArray = inputArray[2:]
    print("INPUT ARRAY",inputArray)
    return output

def insertSorted(a = int):
    global outputArray
    for i in range(len(outputArray)):
        if outputArray[i] > a:
            outputArray.insert(i, a)
            print("INDEX, VALUE:",i, a)
            print("OUTPUT", outputArray)
            return

    outputArray.append(a)
    print("VALUE", a)
    print("OUTPUT:", outputArray)
    return

def insertionSort():
    global inputArray
    global outputArray

    outputArray = createSorted()

    while len(inputArray) > 0:
        insertSorted(inputArray.pop())

    print(outputArray)







def betterSort(arr):
    input = arr
    i = 1;

    #starting at index 1.
    while i < len(input):
        a = input[i]

        j = i
        while j > 0: #check every index before it

            if input[j-1] > a: #check if index below is less than current value

                input[j] = input[j-1] #if so shift it forwards
                j -= 1
            else:   #otherwise end
                break
            print(input)
        input[j] = a #after moving backwards through the list, replace the inital value

        i += 1
    return input


print(betterSort(inputArray))