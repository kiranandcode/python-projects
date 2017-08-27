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

        # select w0.urlid, w0.location, w1.location... from wordlocation w0, wordlocation w1 where w0.wordid=### and w1.urlid=w0.urlid and w1.wordid=####
        fullquery = 'select {} from {} where {}'.format(fieldlist, tablelist, clauselist)
        cur = self.con.execute(fullquery)
        rows = [row for row in cur]

        # returns a list of tuples (urlid, wordlocation location...) where each word in the input string is found in the url
        return rows,wordids

    def inboundlinkscore(self,rows):
        # list of url ids
        uniqueurls=set([row[0] for row in rows])
        # { urlids: count of urls to the currenturl, ...}
        inboundcount=dict([(u,self.con.execute( \
                'select count(*) from link where toid={}'.format(u)).fetchone()[0]) for u in uniqueurls])
        return self.normalize(inboundcount)

    def getscoredlist(self, rows, wordids):
        ## mapping of urls (first entry in tuple to score values
        # totalscores = { urlid=1: 0, urlid=2: 0 }
        totalscores=dict([(row[0],0) for row in rows])

        
        # insert search code here
        weights = [(1.0, self.frequencyscore(rows)),
                   (1.5, self.locationscore(rows)),
                   (1.8, self.distancescore(rows)),
                   (1.9, self.inboundlinkscore(rows))]

        # allows for prioritizing different weights by different ammounts
        for(weight,scores) in weights:
            for url in totalscores:
                totalscores[url] += weight*scores[url]

        return totalscores

    def geturlname(self, id):
        # returns the name value of an urlid
        return self.con.execute(
                "select url from urllist where rowid={}".format(id)).fetchone()[0]
    
    def query(self,q):
        # rows = [(1,1,1,2), (1,2,3,2) ...]
        rows, wordids = self.getmatchrows(q)
        scores = self.getscoredlist(rows,wordids)
        rankedscores = sorted([(score,url) for (url,score) in scores.items()], reverse=1)
        for (score, urlid) in rankedscores[0:10]:
            print("{}\t{}".format(score,self.geturlname(urlid)))


    def normalize(self, scores, smallIsBetter=False):
        #scores = { urlid: score, ...}
        vsmall = 0.00001
        # normalizes all scores between 0, 1 - range is dependant on smallIsBetter
        if smallIsBetter:
            minscore = min(scores.values())
            return dict((u,float(minscore)/max(vsmall,l)) for (u,l) in scores.items())
        else:
            maxscore = max(scores.values())
            if maxscore == 0: maxscore = vsmall
            # returns {urlid: score (normalized between 0,1),...}
            return dict((u,float(c)/maxscore) for (u,c) in scores.items())

    def frequencyscore(self,rows):
        # rows = [(urlid, 1,2,3),...]
        counts=dict((row[0],0) for row in rows)
        # each time a url appears, add 1
        for row in rows: counts[row[0]]+=1
        return self.normalize(counts)

    def locationscore(self, rows):
        locations = dict([(row[0],10000000) for row in rows])
        for row in rows:
            loc = sum(row[1:])
            # sets loc to the earliest the word occurs in the document
            if loc < locations[row[0]]: locations[row[0]]=loc
        return self.normalize(locations, smallIsBetter=True)

    def distancescore(self, rows):
        if len(rows[0]) <= 2: return dict([(row[0],1.0) for row in rows])
        mindistance = dict([(row[0],10000000) for row in rows])
        for row in rows:
            # sums together the distances between consecutive words in the row
            dist=sum([abs(row[i]-row[i-1]) for i in range(2,len(row))])
            if dist<mindistance[row[0]]: mindistance[row[0]]=dist
        return self.normalize(mindistance,smallIsBetter=True)

    def calculatepagerank(self, iterations=20):
        self.con.execute('drop table if exists pagerank')
        self.con.execute('create table pagerank(urlid primary key, score)')

        self.con.execute('insert into pagerank select rowid, 1.0 from urllist')
        self.dbcommit()

