import urllib
from bs4 import BeautifulSoup
from uritools import urijoin
import re

from sqlite3 import dbapi2 as sqlite

class Searcher:
    def __init__(self, dbname):
        self.con = sqlite.connect(dbname)

    def __del__(self):
        self.con.close()

    def getmatchrows(self,q):

        # strings that will eventually be used to build the query
        fieldlist = 'w0.urlid'
        tablelist=''
        clauselist=''
        wordids=[]

        words = q.split(' ')
        tablenumber = 0

        for word in words:
            wordrow = self.con.execute(
                    "select rowid from wordlist where word='{}'".format(word)).fetchone()
            if wordrow:
                # accumulate all the word items into a list 
                wordid = wordrow[0]
                wordids.append(wordid)
                if tablenumber > 0:
                    # if table number is > 0, add connecter phrases
                    tablelist += ','
                    clauselist += ' and '
                    clauselist += 'w{}.urlid=w{}.urlid and '.format(tablenumber-1, tablenumber)
                # field list = w0.urlid, w1.location, 
                fieldlist += ',w{}.location'.format(tablenumber)
                # table list = wordlocation w0, wordlocation w1, wordlocation w2
                tablelist += "wordlocation w{}".format(tablenumber)
                
                # clause list = w0.wordid=10 w0.urlid=w1.urlid and w1.wordid=23 
                # a query for all words with the same url
                clauselist += "w{}.wordid={}".format(tablenumber, wordid)
                tablenumber += 1

        fullquery = 'select {} from {} where {}'.format(fieldlist, tablelist, clauselist)
        cur = self.con.execute(fullquery)
        rows = [row for row in cur]

        # returns a list of tuples (urlid, wordlocation location...) where each word in the input string is found in the url
        return rows,wordids


    def getscoredlist(self, rows, wordids):
        ## mapping of urls (first entry in tuple to score values
        totalscores=dict([(row[0],0) for row in rows])


        weights = [(1.0, self.frequencyscore(rows))]
        # insert search code here

        for(weight,scores) in weights:
            for url in totalscores:
                totalscores[url] += weight*scores[url]

        return totalscores

    def geturlname(self, id):
        # returns the name value of an urlid
        return self.con.execute(
                "select url from urllist where rowid={}".format(id)).fetchone()[0]
    
    def query(self,q):
        rows, wordids = self.getmatchrows(q)
        scores = self.getscoredlist(rows,wordids)
        rankedscores = sorted([(score,url) for (url,score) in scores.items()], reverse=1)
        for (score, urlid) in rankedscores[0:10]:
            print("{}\t{}".format(score,self.geturlname(urlid)))


    def normalize(self, scores, smallIsBetter=False):
        vsmall = 0.00001
        # normalizes all scores between 0, 1 - range is dependant on smallIsBetter
        if smallIsBetter:
            minscore = min(scores.values())
            return dict((u,float(minscore)/max(vsmall,l)) for (u,l) in scores.items())
        else:
            maxscore = max(scores.values())
            if maxscore == 0: maxscore = vsmall
            return dict((u,float(c)/maxscore) for (u,c) in scores.items())

    def frequencyscore(self,rows):
        counts=dict((row[0],0) for row in rows)
        for row in rows: counts[row[0]]+=1
        return self.normalize(counts)
