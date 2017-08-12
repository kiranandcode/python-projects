import feedparser
import re

def getwordcounts(url):
    d = feedparser.parse(url)
    wc = {}


    # process each RSS entry
    for e in d.entries:
        if 'summary' in e: 
            summary = e.summary
        else:
            summary =  e.description

        # extract a list of words
        words = getwords(e.title+' '+summary)
        for word in words:
            wc.setdefault(word, 0)
            wc[word]+=1

    title = None

    if d.feed:
        return d.feed.title,wc
    else:
        raise Exception("Empty feed")


def getwords(html):
    txt = re.compile(r'<[^>]+>').sub('',html)

    words = re.compile(r'[^A-Z^a-z]+').split(txt)

    return [word.lower() for word in words if word != '']




apcount = {}
wordcounts={}
feedlist=[]

for feedurl in open('feedlist.txt'):
    feedlist.append(feedurl)
    try:
        title,wc=getwordcounts(feedurl)
        wordcounts[title]=wc
        for word, count in wc.items():
            apcount.setdefault(word, 0)
            if count > 1:
                apcount[word]+=1
    except Exception:
        continue


# generate a list of words
wordlist = []

for w,bc in apcount.items():
    frac = float(bc)/len(feedlist)
    if frac > 0.1 and frac < 0.5:
        wordlist.append(w)

with open('blogdata.txt', 'w', encoding="UTF-8") as out:
    out.write('Blog')
    # write a line containing every word
    for word in wordlist:
        out.write("\t{}".format(word))
    out.write('\n')

    # for each blog, construct a vector with elements corresponding to the number of occurances of each value
    for blog,wc in wordcounts.items():
        out.write(blog)
        for word in wordlist:
            if word in wc:
                out.write("\t{}".format(wc[word]))
            else:
                out.write("\t0")
        out.write("\n")
