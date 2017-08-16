import urllib
from bs4 import BeautifulSoup
from uritools import urijoin
import re

from sqlite3 import dbapi2 as sqlite

# words to ignore
ignorewords=set(['the','of','to','and','a','in','is','it'])

class crawler:
    # initialize the crawler with the dbname
    def __init__(self, dbname):
        self.con = sqlite.connect(dbname)

    # clear all records on end
    def __del__(self):
        self.con.close()

    
    def dbcommit(self):
        self.con.commit()

    def createindextables(self):
        self.con.execute('create table urllist(url)')
        self.con.execute('create table wordlist(word)')
        self.con.execute('create table wordlocation(urlid,wordid,location)')
        self.con.execute('create table link(fromid integer,toid integer)')
        self.con.execute('create table linkwords(wordid,linkid)')
        self.con.execute('create index wordidx on wordlist(word)')
        self.con.execute('create index urlidx on urllist(url)')
        self.con.execute('create index wordurlidx on wordlocation(wordid)')
        self.con.execute('create index urltoidx on link(toid)')
        self.con.execute('create index urlfromidx on link(fromid)')
        self.dbcommit()
    
    #  getting an entry id or adding it if not present
    def getentryid(self,table, field, value, createnew=True):
        return None

    # index a page
    def addtoindex(self, url, soup):
        if self.isindexed(url): return
        print('Indexing {}'.format(url))

        text = self.gettextonly(soup)
        words = self.separatewords(text)

        urlid = self.getentryid('urllist','url',url)

        for i in range(len(words)):
            word = words[i]
            if word in ignorewords: continue
            wordid = self.getentryid('wordlist', 'word', word)
            self.con.execute('insert into wordlocation(urlid,wordid,location) \
                    values ({},{},{})'.format(urlid,wordid,i))



    # extract a page only
    def gettextonly(self, soup):
        v = soup.string
        if v == None:
            c = soup.contents
            resulttext=''
            for t in c:
                # recurse to traverse the dom
                subtext = self.gettextonly(t)
                resulttext += subtext + '\n'
            return resulttext
        else:
            return v.strip()

    # separate words by any non-whitespace character
    def separatewords(self, text):
        splitter = re.compile('\\W*')
        return [s.lower() for s in splitter.split(text) if s != '']


    def isindexed(self, url):
        return False

    def addlinkref(self, urlFrom, urlTo, linkText):
        pass

    def crawl(self, pages, depth=2):
        # iterate for each depth
        for i in range(depth):
            # use a set to prevent repeats
            newpages = set()

            # for each page in pages list
            for page in pages:
                c = None
                try:
                    c = urllib2.urlopen(page)
                except:
                    print("Could not open {}".format(page))

                if not c:
                    continue


                # after retrieving the html
                soup = BeautifulSoup(c.read())

                # index page 
                self.addtoindex(page, soup)

                # iterate through all the links in the page
                links = soup('a')
                for link in links:
                    if('href' in dict(link.attrs)):
                        url = urijoin(page, link['href'])
                        
                        # check for quotes
                        if url.find("'")!= -1: continue

                        # remove location fragments
                        url = url.split('#')[0]

                        # is the result a valid url
                        if url[0:4] == 'http' and not self.isindexed(url):
                            newpages.add(url)
                        # create a link between the two pages
                        linkText = self.gettextonly(link)
                        self.addlinkref(page, url, linkText)
                
                # store the db
                self.dbcommit()

            # recurse
            pages =newpages

    def createindextables(self):
        pass
