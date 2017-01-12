import urllib.request
import itertools
url = "http://www.pythonchallenge.com/pc/def/linkedlist.php?nothing={}"

val = 53548
def search():
    global val
    while True:
        link = urllib.request.urlopen(url.format(val))
        string = bytes.decode(link.readline())
        try:
            val = int(''.join(itertools.dropwhile(lambda a: not str.isdigit(a), string)))
        except ValueError:
            print(string, " caused errors - this is last value ", val)
            val /= 2
        
def searchAlt():
    global val
    while True:
        link = urllib.request.urlopen(url.format(val))
        string = bytes.decode(link.readline())
        print(string)
        val = val/2

def fullSearch():
    try:
        search()
    except ValueError:
        print("That's one loop")
    searchAlt()
