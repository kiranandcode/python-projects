def indexes(a, val):
    output = []
    try:
        runs = a.count(val)
        if runs > 1 :
            index = a.index(val)
            output.append(index)
            for i in range(a.count(val)):
                if(a[index+1:].count(val) == 0):
                    break
                index = a[index+1:].index(val)+index+1
                output.append(index)

            return output
        else:
            return a.index(val)
    except (e):
        print(e)



