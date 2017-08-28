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
        cur = self.con.execute(
                "select rowid from {} where {}='{}'".format(table,field,value))
        res = cur.fetchone()
        if(res == None):
            if createnew:
                cur = self.con.execute(
                        "insert into {}({}) values ('{}')".format(table,field,value))
                return cur.lastrowid
            else:
                return None
        else:
            return res[0]

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
        cur = self.con.execute("select rowid from urllist where url={}".format(url))
        res = cur.fetchone()
        if res:
            # check whether the urlid has been indexed, we could have a link that's in urlist, but hasn't actually been trawled
            v = self.con.execute("select * from wordlocation where urlid={}".format(res[0])).fetchone()
            if v:
                return True
        return False

    def addlinkref(self, urlFrom, urlTo, linkText):
        words = self.separatewords(linkText)
        fromid = self.getentryid('urllist','url',urlfrom)
        toid = self.getentryid('urllist','url', urlTo)

        if fromid == toid:
            return
        cur = self.con.execute("insert into link(fromid,toid) values({},{})".format(fromid,toid))
        linkid = cur.lastrowid
        for word in words:
            if word in ignorewords: continue
            wordid = self.getentryid('wordlist','word',word)
            self.con.execute("insert into linkwords(linkid,wordid) values({},{})".format(linkid,wordid))

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

                # index page (as in add all the words into the words table)
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

    def calculatepagerank(self, iterations=20):
        self.con.execute('drop table if exists pagerank')
        self.con.execute('create table pagerank(urlid primary key, score)')

        # initialize pagerank as (urls, 1.0) for each url in urllist
        self.con.execute('insert into pagerank select rowid, 1.0 from urllist')
        self.dbcommit()

        for i in range(iterations):
            print("Iteration {}".format(i))
            # for each url in pagerank
            for (urlid,) in self.con.execute('select rowid from urllist'):
                pr=0.15

                # select all unique urls pointing to the url
                for (linker,) in self.con.execute( \
                        'select distinct fromid from link where toid={}'.format(urlid)):
                    # get the score for the fromurl
                    linkingpr=self.con.execute(
                            'select score from pagerank where urlid={}'.format(linker)).fetchone()[0]

                    # count all the links from the fromurl
                    linkingcount=self.con.execute( \
                            'select count(*) from link where fromid={}'.format(linker)).fetchone()[0]
                    pr += 0.85*(linkingpr/linkingcount)
                self.con.execute(
                        'update pagerank set score={} where urlid={}'.format(pr,urlid))
                self.dbcommit()
