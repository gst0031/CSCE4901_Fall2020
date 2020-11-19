list1 = []

for n in range(5):
    list1.append([])

#print(list1)

for n in range(len(list1)):
    #list1[n].append(n)
    list1[n].append([1, 2, 3])
#print(list1)

from bs4 import BeautifulSoup
import requests
import csv

## VOLUME X - Abstract URL Scraper ##
for n in range(0, 1):
    current_url = "https://www.jmlr.org/papers/v1/meila00a.html"   
    #print("################# ", current_url) # !Testing 
    source_url_get = requests.get(current_url).text
    soup_url = BeautifulSoup(source_url_get, 'lxml')
    abstractURL_list = []
    jmlr_abstract_URL_list = []
    
    current_volume_table = soup_url.find("div", id="content")
    print(current_volume_table)
    #current_volume_aTag = current_volume_table.find_all("a")