### TESTING SPECIFIC VOLUMES
## Web scraper for Journal of Machine Learning Research - https://www.jmlr.org/papers/
# Can get from an html file or a web page - This will pull from webpage

from bs4 import BeautifulSoup
import requests
import csv

## VOLUME 5 ##
current_url = "https://www.jmlr.org/papers/v5/"
print("################# ", current_url) # !Testing
source_url_get = requests.get(current_url).text
soup_url = BeautifulSoup(source_url_get, 'lxml')
#print(soup_url) # !Testing

current_volume_content = soup_url.find("div", id="content")
#print(current_volume_content) # !Testing
current_volume_titles = current_volume_content.find_all("dt")
# print(current_volume_titles[0].text.rstrip())
# print(current_volume_titles[2].text.rstrip().replace('\n', ''))
# print(current_volume_titles[20].text.strip().rep)
# print(current_volume_titles[2].text.rstrip())
# print(current_volume_titles[3].text.rstrip())

seperator = "("
seperator2 = " "
for x in range(len(current_volume_titles)):
    current_volume_titles[x] = current_volume_titles[x].text.rstrip().replace('\n', '').replace("  ", ' ')
    string1 = str(current_volume_titles[x])
    #print(string1) # !Testing
    current_volume_titles[x] = string1.split(seperator, 1)[0]
    current_volume_titles[x] = str(current_volume_titles[x]).rstrip()
    #jmlr_title_list.append(current_volume_titles[x]) 
    print(current_volume_titles[x]) # !Testing

##2D list append test
# volume_titles = []

# for n in range(21):
#     volume_titles.append([n, n+1])
    
# print(volume_titles)