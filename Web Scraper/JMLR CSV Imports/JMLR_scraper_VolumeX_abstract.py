### TESTING SPECIFIC VOLUMES
## Web scraper for Journal of Machine Learning Research - https://www.jmlr.org/papers/
# Can get from an html file or a web page - This will pull from webpage
# Santosh Khadka santoshkhadka@my.unt.edu

from bs4 import BeautifulSoup
import requests
import csv

## VOLUME X - Abstract URL Scraper ##
for n in range(0, 1):
    current_url = "https://www.jmlr.org/papers/v2/"   
    #print("################# ", current_url) # !Testing 
    source_url_get = requests.get(current_url).text
    soup_url = BeautifulSoup(source_url_get, 'lxml')
    abstractURL_list = []
    jmlr_abstract_URL_list = []
    
    current_volume_table = soup_url.find("div", id="content")
    current_volume_aTag = current_volume_table.find_all("a")
    #print(current_volume_aTag) # !Testing
    for i in range(len(current_volume_aTag)):
        if ("[abs]" in str(current_volume_aTag[i])) or (">abs<" in str(current_volume_aTag[i])):
            string1 = str(current_volume_aTag[i])
            string1 = string1.split('"')
            if ("v1/" in current_url) or ("v2/" in current_url) or ("v3/" in current_url):
                string1 = (current_url+string1[1]).replace(" ", '')
                #print(string1) # !Testing
            elif("v4/" in current_url) or ("v5/" in current_url):
                string1 = (string1[1]).replace(" ", '')
                #print(string1)
            else:
                string1 = "http://www.jmlr.org"+((string1[1]).replace(" ", ''))
                #print(string1)
            abstractURL_list.append(string1)
    jmlr_abstract_URL_list.append(abstractURL_list)   
# print(len(jmlr_abstract_URL_list[0]))
    
for x in range(len(jmlr_abstract_URL_list)):
    for y in range(len(jmlr_abstract_URL_list[x])):
        # NOTE HOW STORAGE WORKS: jmlr_abstract_URL_list[x][y] : x is volume[x] and y is url[y] in volume[x]
        current_url = jmlr_abstract_URL_list[x][y]
        #print("################# ", current_url) # !Testing 
        source_url_get = requests.get(current_url).text
        soup_url = BeautifulSoup(source_url_get, 'lxml')
        current_volume_abstract_list = []   

        # ABSTRACT get: Get evertyhing in <table> -> <a> -> "[abs]" : Abstract urls
        current_volume_table = soup_url.find("div", id="content")
        current_volume_aTag = current_volume_table.find_all("h3")
        #print(current_volume_table) # !Testing
        string1 = str(current_volume_table).split("</h3>")
        string1 = str(string1[1]).split("<p>")
        print(string1[0].strip(), '\n') # !Testing
        #print(current_volume_aTag)
        for i in range(len(current_volume_aTag)):
            if ("[abs]" in str(current_volume_aTag[i])) or (">abs<" in str(current_volume_aTag[i])):
                string1 = str(current_volume_aTag[i])
                string1 = string1.split('"')
                string1 = (current_url+string1[1]).replace(" ", '')
            abstractURL_list.append(string1)
        jmlr_abstract_URL_list.append(abstractURL_list)
        #print(len(jmlr_abstract_URL_list[n])) # !Testing
        
#print(jmlr_abstract_URL_list) # !Testing