import random
from clusters import pearson

def kcluster(rows, distance=pearson,k=4):

    ranges=[(min(row[i] for row in rows), max(row[i] for row in rows)) for i in range(len(rows[0]))]

    clusters=[
            [
                random.random()*(ranges[i][1]-ranges[i][0])+ranges[i][0] for i in range(len(rows[0]))] for j in range(k)]

    lastmatches = None

    for t in range(100):
        print('Iteration {}'.format(t))

        # construct k lists, each of which will be filled by the closest matches
        bestmatches = [[] for i in range(k)]


        for j in range(len(rows)):
            row = rows[j]
            bestmatch = 0
            bestdist  = distance(clusters[bestmatch],row)

            for i in range(k):
                d = distance(clusters[i],row)
                if d < bestdist:
                    bestmatch,bestdist = i, d

            bestmatches[bestmatch].append(j)

        if bestmatches == lastmatches:
            break
        lastmatches = bestmatches


        for i in range(k):
            avgs = [0.0]*len(rows[0])
            if len(bestmatches[i]) > 0:
                for rowid in bestmatches[i]:
                    for m in range(len(rows[rowid])):
                        avgs[m] += rows[rowid][m]
                for j in range(len(avgs)):
                    avgs[j] /= len(bestmatches[i])
                clusters[i] = avgs
    return bestmatches
