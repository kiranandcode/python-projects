from math import sqrt

def loadMovieLens(path='/home/gopiandcode/Downloads/temp/ml-100k'):

    movies = {}
    prefs = {}

    for line in open(path+'/u.item', encoding='latin-1'):
        try:
            (id,title)=line.split('|')[0:2]
            movies[id]=title
        except Exception:
            print("Error")
    try:
        for line in open(path+'/u.data'):
            (user,movieid,rating,ts)=line.split('\t')
            prefs.setdefault(user,{})
            prefs[user][movies[movieid]] = float(rating)
    except Exception:
        print("Error")
    return prefs


def pearson_simmilarity(entryA, entryB, dataset):
    """
    Given two entries into a data set, calculates the pearson correleation coefficient for the two entries.
    """

    values = {}

    # Generate a smaller data set of only values both have seen
    for value in dataset[entryA]:
        if value in dataset[entryB]:
            values.setdefault(value,{})
            values[value][entryA] = dataset[entryA][value]
            values[value][entryB] = dataset[entryB][value]

    # if no simmilar values, return 0
    if len(values) == 0:
        return 0

    n = len(values)

    sumEntryA = sum(values[i][entryA] for i in values.keys())
    sumEntryB = sum(values[i][entryB] for i in values.keys())

    sumSqEntryA = sum(pow(values[i][entryA],2) for i in values.keys())
    sumSqEntryB = sum(pow(values[i][entryB],2) for i in values.keys())
    sumEntryAEntryB = sum(values[i][entryA]*values[i][entryB] for i in values.keys())

    numerator = (n * sumEntryAEntryB) - (sumEntryA * sumEntryB)

    denomSq = (n*sumSqEntryA - pow(sumEntryA,2))*(n*sumSqEntryB - pow(sumEntryB,2))
    
    denom = sqrt(denomSq)

    # check for division by zero errors
    if denom == 0:
        return 0

    return (numerator / denom)*n




def getSimmilar(key_entry, dataset, simmilarity_function=pearson_simmilarity):
    """
    Given an entry into a data set, will return a list of tuples.
    Each tuple will be of the form
    (score, entry)
    where score is the simmilarity score given by the simmilarity_function.
    The list will also sorted with the highest scores at the top.
    """

    results = []

    for entry in dataset.keys():
        if entry != key_entry:
            score = simmilarity_function(key_entry, entry, dataset)
            results.append((score, entry))

    results.sort(key=lambda x: x[0], reverse=True)

    return results
    

def processDataset(dataset):
    processed = {}

    for key in dataset.keys():
        simmilar = getSimmilar(key, dataset)[0:5]
        processed[key] = simmilar

    return processed
