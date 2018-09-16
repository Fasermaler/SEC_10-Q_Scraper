# -*- coding: utf-8 -*-
"""
Created on Mon Sep 17 00:17:56 2018

@author: Fasermaler
"""

from pprint import pprint
import requests
import csv
from bs4 import BeautifulSoup

links_list = ['MMM','ABT']

e = 0
for i in range(len(links_list)) :
    url = "https://www.sec.gov/cgi-bin/browse-edgar?CIK=" + str(links_list[i]) + "&owner=exclude&action=getcompany&Find=Search"

    session = requests.session()
    user_agent_header = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
    
    page_source = session.get(url, allow_redirects = True, headers = user_agent_header, verify = False).text
    
    soup = BeautifulSoup(page_source, "lxml")
    current_tag = links_list[i]
    table_data = []
    table_data.append(current_tag)
    
    #with open("rawpage2.html", "w", encoding="UTF-8") as file:
    #    file.write(str(soup))
    
    full_table = soup.find("div", {"id": "seriesDiv"}).find("table").find_all("td")
    div_table = soup.find("div", {"id": "seriesDiv"}).find("table").find("td")#.find("tbody")]
    div_links = soup.find("div", {"id": "seriesDiv"}).find("table").find("a")['href']
    #pprint(div_table)
    #pprint(div_links)
    #pprint(div_table)
    document_link = []
    e = 0
    for i in full_table:
        try:
            tr_iterable = div_table.text#[x.text.strip() for x in div_table]
            #pprint(tr_iterable)
            if "10-Q" == tr_iterable:
                document_link.append(div_table.find_next_sibling().find("a")['href'])
            else:
                pass
        except:
            pass
        div_table = div_table.next_element
    pprint(document_link)
    full_doc_url = "https://www.sec.gov" + document_link[0]
    pprint(full_doc_url)
    
    session = requests.session()
    user_agent_header = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
    
    page_source = session.get(full_doc_url, allow_redirects = True, headers = user_agent_header, verify = False).text
    
    soup = BeautifulSoup(page_source, "lxml")
    
    with open("rawpage3.html", "w", encoding="UTF-8") as file:
        file.write(str(soup))
    
    doc_table = soup.find("table", {"class": "tableFile"}).find("tr").find_next_sibling()
    pprint(doc_table)
    dochtm_link = "https://www.sec.gov" + str(doc_table.find("a")['href'])
    pprint(dochtm_link)
    
    table_data.append(dochtm_link)
    e += 1
    
    
    
    with open("report_links.csv", "a", encoding="UTF-8", newline = "") as f:
                writer = csv.writer(f, delimiter = ",")
                writer.writerow(table_data)