### TESTING SPECIFIC VOLUMES
## Web scraper for Journal of Machine Learning Research - https://www.jmlr.org/papers/
# Can get from an html file or a web page - This will pull from webpage

from bs4 import BeautifulSoup
import requests
import csv

## VOLUME X - Abstract URL Scraper ##
for n in range(0, 1):
    current_url = "https://www.jmlr.org/papers/v21/"   
    print("################# ", current_url) # !Testing 
    source_url_get = requests.get(current_url).text
    soup_url = BeautifulSoup(source_url_get, 'lxml')
    current_volume_abstract_list = []
    abstractURL_list = []
    jmlr_abstract_URL_list = []
    
    current_volume_table = soup_url.find("div", id="content")
    current_volume_aTag = current_volume_table.find_all("a")
    #print(current_volume_aTag) # !Testing
    for i in range(len(current_volume_aTag)):
        if ("[abs]" in str(current_volume_aTag[i])) or (">abs<" in str(current_volume_aTag[i])):
            string1 = str(current_volume_aTag[i])
            string1 = string1.split('"')
            string1 = (current_url+string1[1]).replace(" ", '')
            #print(string1) # !Testing
            abstractURL_list.append(string1)
    jmlr_abstract_URL_list.append(abstractURL_list)   
print(len(jmlr_abstract_URL_list[0]))
    
# txt = "apple#banana#cherry#orange"

# # setting the maxsplit parameter to 1, will return a list with 2 elements!
# x = txt.split("#", 1)

# print(x)