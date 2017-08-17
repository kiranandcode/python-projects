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
                wordid = wordrow[0]
                wordids.append(wordid)
                if tablenumber > 0:
                    tablelist += ','
                    clauselist += ' and '
                    clauselist += 'w{}.urlid=w{}.urlid and '.format(tablenumber-1, tablenumber)
                    fieldlist += ',w{}.location'.format(tablenumber)
                    tablelist += "wordlocation w{}".format(tablenumber)
                    clauselist += "w{}.wordid={}".format(tablenumber, wordid)
                    tablenumber += 1

        fullquery = 'select {} from {} where {}'.format(fieldlist, tablelist, clauselist)
        cur = self.con.execute(fullquery)
        rows = [row for row in cur]

        return rows,wordids
