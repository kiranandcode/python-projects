from math import sqrt
from recommendations import critics
from itertools import combinations

def sim_distance(prefs, person1, person2):
    si = {}
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item] = 1
    if len(si) == 0:
        return 0
    sum_of_squares = sum(pow(prefs[person1][item]-prefs[person2][item],2) for item in si)
    # we want a higher score for people who are simmilar.
    # the euclidian distance, sqrt(sum_of_squares) would be
    # smaller for simmilar people.
    # hence we invert and (add 1 to prevent division by 0
    return 1/(1+sqrt(sum_of_squares))


min = 10000
best =[] 

for criticA, criticB in combinations(critics.keys(), 2): 
        print(criticA, " != ", criticB)
        score = sim_distance(critics, criticA, criticB)
        if score < min:
            min = score
            best = [criticA,criticB]

print(min, " by ", criticA, " and ", criticB)
        
