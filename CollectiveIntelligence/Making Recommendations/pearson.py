from recommendations import critics
from math import sqrt
from itertools import combinations

def pearson_distance(prefs, p1, p2):
    si = {}
    for item in prefs[p1]:
        if item in prefs[p2]:
            si[item] = 1

    n = len(si)

    if n==0:
        return 0.0

    sum1 = sum(prefs[p1][item] for item in si)
  #  print("Sum for ", p1, " is ", sum1)
    sum2 = sum(prefs[p2][item] for item in si)
  #  print("Sum for ", p2, " is ", sum2)

    sum1Sq = sum(pow(prefs[p1][item],2) for item in si)
  #  print("Sum of squares for ", p1, " is ", sum1Sq)
    sum2Sq = sum(pow(prefs[p2][item],2) for item in si)
  #  print("Sum of squares for ", p2, " is ", sum2Sq)

    pSum = sum(prefs[p1][item] * prefs[p2][item] for item in si)
  #  print("Sum of multiplication is ", pSum)

    num = pSum - (sum1 * sum2/n)
  #  print("Num is ", num)
    den = sqrt((sum1Sq - pow(sum1,2)/n)*(sum2Sq - pow(sum2, 2)/n))
  #  print("Den is ", den)
    if den == 0:
        return 0.0
    r = num/den
  #  print("Num(", num, ")/den(", den, ") = ", r)
    return r


min = 0 
best = [] 

for criticA, criticB in combinations(critics, 2):
    score = pearson_distance(critics, criticA, criticB)
    if score > min :
        print("Best Score is ",score)
        min = score
        best = [criticA, criticB]
        print("Best is ", best, " with ", min)
    
if len(best) > 0:
    print(min, " from ", best[0]," and ", best[1])

for item in critics[best[0]]:
    if item in critics[best[1]]:
        print(item, " got a score of ", critics[best[0]][item], " from ", best[0], " and a score of ", critics[best[1]][item], " from ", best[1])



def topMatches(prefs, person, n=5, simmilarity=pearson_distance):
    scores = [(simmilarity(prefs, person, other), other) for other in prefs if other != person]
    scores.sort()
    scores.reverse()
    return scores[0:n]

for person in critics:
    print("Top matches for ", person, " was ", topMatches(critics, person))
