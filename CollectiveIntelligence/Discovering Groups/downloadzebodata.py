from bs4 import BeautifulSoup
import urllib2
import re

chare = re.compile(r'[!-\.&]')
itemowners = {}
dropwords = ['a','new','some','more','my','own'



soup = BeautifulSoup(html_doc, 'html.parser')
