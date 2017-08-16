import urllib
from bs4 import BeautifulSoup
from uritools import urijoin

# words to ignore
ignorewords=set(['the','of','to','and','a','in','is','it'])

class crawler:
    # initialize the crawler with the dbname
    def __init__(self, dbname):
        pass

    # clear all records on end
    def __del__(self):
        pass

    
    def dbcommit(self):
        pass

    
    #  getting an entry id or adding it if not present
    def getentryid(self,table, field, value, createnew=True):
        return None

    # index a page
    def addtoindex(self, url, soup):
        print('Indexing {}'.format(url))

    # extract a page only
    def gettextonly(self, soup):
        return None

    # separate words by any non-whitespace character
    def separatewords(self, text):
        return None


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
