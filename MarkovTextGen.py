import random
def countOccurances(string):
    counter ={}
    for char in string:
            fchar = counter.get(char,1)
            fchar += 1
            counter[char] = fchar
    return counter

def convString(file):
    prostring = []
    for line in file:
        word = line.strip().split()
        prostring.append(word)
    return prostring

    
def buildMarkov(ls):
    mk = {}
    for line in ls:
        for index, word in enumerate(line):
            if(index < len(line)-2):
                if not tuple(word) in mk:
                    mk[tuple(word)] = []
                tmp = mk[tuple(word)]
                tmp.append(line[index+1])
                mk[tuple(word)] = tmp
    return mk


def buildSentence(mk, times):
    ks = list(mk.keys())
    srtwd = random.choice(ks)
    for i in range(times):
        if not isinstance(srtwd, tuple):
            print(str(srtwd), end=" ")
        else:
            print("".join(srtwd), end=" ")
        if len(mk.get(tuple(srtwd), [])) > 0:
            srtwd = random.choice(mk[tuple(srtwd)])
        else:
            print(" ")
            srtwd = random.choice(ks)

