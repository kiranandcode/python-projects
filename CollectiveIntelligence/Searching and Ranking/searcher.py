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

        return rows,wordids
