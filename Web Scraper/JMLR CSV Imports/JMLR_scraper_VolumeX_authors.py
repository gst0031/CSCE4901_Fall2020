### TESTING SPECIFIC VOLUMES
## Web scraper for Journal of Machine Learning Research - https://www.jmlr.org/papers/
# Can get from an html file or a web page - This will pull from webpage

from bs4 import BeautifulSoup
import requests
import csv

## VOLUME 5 ##
current_url = "https://www.jmlr.org/papers/v1/"
print("################# ", current_url) # !Testing
source_url_get = requests.get(current_url).text
soup_url = BeautifulSoup(source_url_get, 'lxml')
#print(soup_url) # !Testing

# AUTHOR get: Get evertyhing in <dd> tags
current_volume_table = soup_url.find("table", cellspacing="0")
current_volume_bTag = current_volume_table.find_all("b")
#print(current_volume_bTag) # !Testing
#current_volume_authors = current_volume_bTag.find_all("i")
for i in range(len(current_volume_bTag)):
    print(current_volume_bTag[i].text)
# print(current_volume_authors[2].text.rstrip().replace('\n', ''))
# print(current_volume_authors[20].text.strip().rep)
# print(current_volume_authors[2].text.rstrip())
# print(current_volume_authors[3].text.rstrip())

# seperator = "("
# seperator2 = " "
# for x in range(len(current_volume_authors)):
#     current_volume_authors[x] = current_volume_authors[x].text.rstrip().replace('\n', '').replace("  ", ' ')
#     string1 = str(current_volume_authors[x])
#     #print(string1) # !Testing
#     current_volume_authors[x] = string1.split(seperator, 1)[0]
#     current_volume_authors[x] = str(current_volume_authors[x]).rstrip()
#     #jmlr_title_list.append(current_volume_titles[x]) 
#     print(current_volume_authors[x]) # !Testing

##2D list append test
# volume_titles = []

# for n in range(21):
#     volume_titles.append([n, n+1])
    
# print(volume_titles)