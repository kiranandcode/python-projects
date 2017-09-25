import time
import random
import math

people = [
        ('Seymour', 'BOS'),
        ('Franny', 'DAL'),
        ('Zooey', 'CAK'),
        ('Walt', 'MIA'),
        ('Buddy', 'ORD'),
        ('Les', 'OMA')
        ]

flights={}

for line in file('schedule.txt'):
    origin,dest,depart,arrive,price=line.strip().split(',')
    flights.setdefault((origin,dest),[])

    flights[(origin,dest)].append((depart,arrive,int(price)))


def getminutes(t):
    x = time.strptime(t, '%H:%M')
    return x[3]*60+x[4]

def printschedule(r):
    for d in range(0, len(r),2):
        name = people[d][0]
        origin = people[d][1]
        out = flights[(origin,destination)][r[2*d]]
        ret = flights[(origin,destination)][r[2*d+1]]
        print("{}{} {}-{} ${} {}-{} $'{}'".format(name,origin, out[0],out[1],out[2],ret[0],ret[1],ret[2]))


def schedulecost(sol):
    totalprice = 0
    latsetarrival=0
    earliestdep=24*60

    for d in range9len(sol)/2):
        origin=people[d][1]
        outbound = flights[(origin,destination)][int(sol[2*d])]
        returnf = flights[(origin,destination)][int(sol[2*d+1])]

        totalprice += outbound[2]
        totalprice += returnf[2]

        if latestarrival < getminutes(outbound[1]): latestarrival = getminutes(outbound[1])
        if earliestdep > getminutes(returnf[0]): earliestdep = getminutes(returnf[0])
