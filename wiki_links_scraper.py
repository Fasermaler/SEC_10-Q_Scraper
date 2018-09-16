# -*- coding: utf-8 -*-
"""
Created on Sun Sep 16 01:01:23 2018

@author: Fasermaler
"""


from pprint import pprint
import requests
from bs4 import BeautifulSoup
import csv


url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

session = requests.session()
user_agent_header = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}

page_source = session.get(url, allow_redirects = True, headers = user_agent_header, verify = False).text

soup = BeautifulSoup(page_source, "lxml")

#with open("rawpage.html", "w", encoding="UTF-8") as file:
#    file.write(str(soup))

links_table = soup.find("div", {"class": "mw-parser-output"}).find("table").find("tbody")
totallinks = links_table.find_all("tr")
links_tr = links_table.find("tr").find_next_sibling()

links_list = []

for i in totallinks:
    try:
        tr_iterable = links_tr.find("a", {"class": "external text"}).text
        #ticker_label = [x.text.strip() for x in tr_iterable]
        #pprint(tr_iterable)
        links_list.append(str(tr_iterable))
        links_tr = links_tr.find_next_sibling()
    except:
        break

links_list = [link.replace(".", "") for link in links_list]
print(links_list)


