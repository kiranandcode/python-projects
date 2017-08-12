from math import sqrt

def readfile(filename, encoding=None):
    """
        Parses generated data, which should have the following format:
        1st Line: List of tab separated words.
        nth Line: Feedname, number for each word in 1st line
        
        returns the rows, the columns and the data"""
    lines = [line for line in open(filename, encoding=encoding)]

    colnames = lines[0].strip().split('\t')[1:]
    rownames=[]
    data=[]
    for line in lines[1:]:
        p = line.strip().split('\t')[0:]
        name = p[0].encode('ascii','ignore').decode(encoding='ascii', errors='ignore')
        
        print(name)
        rownames.append(name)
        data.append([float(x) for x in p[1:]])
    return rownames, colnames, data




def pearson(v1, v2):
    """

    Calculates a modifiedpearson correlation coefficient for 2 datasets for the clustering algorithm.

    
    The pearson correleation coefficient is modified to return a smaller value the closer two values are - to simulate the euclidean distance measure.
    """

    sum1 = sum(v1)
    sum2 = sum(v2)

    sum1Sq = sum(pow(i,2) for i in v1)
    sum2Sq = sum(pow(i,2) for i in v2)

    if len(v1) != len(v2):
        while len(v1) < len(v2):
            v1.append(0)
        while len(v2) < len(v1):
            v2.append(0)


    pSum = sum(v1[i]*v2[i] for i in range(len(v1)))

    n = len(v1)

    num = pSum - (sum1*sum2/n)
    den = sqrt((sum1Sq-pow(sum1,2)/n)*(sum2Sq - pow(sum2,2)/n))

    if den == 0: return 0

    return 1.0 - (num/den)

    

    
class bicluster:
    """
    A class designed to represent the clusters made in the clustering
    algorithm.

    good stuff

    """
    def __init__(self, vec, left=None, right=None, distance=0.0,id=None):
        self.left = left
        self.right = right
        self.vec = vec
        self.id = id
        self.distance = distance

    def print(clust, labels=None, n=0):
        for i in range(n): print(' ',end='')

        if clust.id < 0:
            print('-', end='\n')
        else:
            if labels==None:
                print(clust.id)
            else:
                print(labels[clust.id])

        if clust.left!=None: clust.left.print(labels=labels,n=n+1)
        if clust.right!=None: clust.right.print(labels=labels,n=n+1)

def hcluster(rows, distance=pearson):
    distances = {}
    currentclustid=-1

    clust=[bicluster(rows[i],id=i) for i in range(len(rows))]

    while len(clust) > 1:
        lowestpair = (0,1)
        closest = distance(clust[lowestpair[0]].vec, clust[lowestpair[1]].vec)

        for i in range(len(clust)):
            for j in range(i+1, len(clust)):
                # O(n^2) Baby! I just don't care!! Whooo!
                if(clust[i].id, clust[j].id) not in distances:
                    # sweet memoization ftw!
                    distances[(clust[i].id, clust[j].id)]=distance(clust[i].vec, clust[j].vec)
                d = distances[clust[i].id, clust[j].id]
                if d < closest:
                    closest = d
                    lowestpair=(i,j)

        mergevec = [
                (clust[lowestpair[0]].vec[i]+clust[lowestpair[1]].vec[i])/2.0 for i in range(len(clust[0].vec))]

        newcluster = bicluster(mergevec,left=clust[lowestpair[0]],
                right=clust[lowestpair[1]], distance=closest,id=currentclustid)

        currentclustid -= 1

        # remove from list
        del clust[lowestpair[1]]
        del clust[lowestpair[0]]
        clust.append(newcluster)

    return clust[0]


