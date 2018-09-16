# -*- coding: utf-8 -*-
"""
Created on Sun Sep 16 01:01:23 2018

@author: Fasermaler
"""


from pprint import pprint
import requests
from bs4 import BeautifulSoup
import csv
import time

total_success_count = 0
total_failed_count = 0
start_time = time.time()
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
# Removes any periods to deal with persky tickers like Berkshire Hathaway (BRK.B)
links_list = [link.replace(".", "") for link in links_list]
# Prints the list of tickers
print(links_list)
total_reports_count = len(links_list)
e = 0

report_links_list = []
for i in range(len(links_list)) :
    url = "https://www.sec.gov/cgi-bin/browse-edgar?CIK=" + str(links_list[i]) + "&owner=exclude&action=getcompany&Find=Search"

    session = requests.session()
    user_agent_header = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
    
    page_source = session.get(url, allow_redirects = True, headers = user_agent_header, verify = False).text
    
    soup = BeautifulSoup(page_source, "lxml")
    current_tag = links_list[i]
    table_data = []
    table_data.append(current_tag)
    
    print("Currently Processing: " + str(links_list[i]))
    
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
    try:
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
                    
        reports_links_list.append(dochtm_link)
        total_success_count += 1
    except:
        print("ERROR! 10-Q not found!")
        total_failed_count += 1
        pass
end_time = time.time()
elapsed_time = end_time - start_time
# converts the elapsed time to hours, minutes and seconds
minutes, seconds = divmod(elapsed_time, 60)
hours, minutes = divmod(minutes, 60)
# Completion output
print("COMPLETE!")
print("Total Reports: %d, Successful: %d, Failed: %d" % (total_reports_count, total_success_count, total_failed_count))
print("Total time taken: %d hours, %02d minutes, %02d seconds" % (hours, minutes, seconds))