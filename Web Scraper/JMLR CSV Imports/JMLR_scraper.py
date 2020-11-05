## Web scraper for Journal of Machine Learning Research - https://www.jmlr.org/papers/
# Can get from an html file or a web page - This will pull from webpage

from bs4 import BeautifulSoup
import requests
import re #regex
import csv

## CSV Column variables/lists
jmlr_title_list = []
jmlr_abstract_list = []
jmlr_authors_list = []
jmlr_keywords_list = []
jmlr_affiliations_list = []
jmlr_month_list = []
jmlr_link_list = []
jmlr_journal_name = "Journal of Machine Learning Research"
jmlr_year_list = []
jmlr_volume_list = []
jmlr_issue_list = []

## Scraper Set Up - ALL Volumes 
source_volumes = requests.get('https://www.jmlr.org/papers/').text
soup_papers = BeautifulSoup(source_volumes, 'lxml')
#print(soup_papers.prettify())

## Find - volume titles - Method 1
volume_name = soup_papers.find("font", class_="volume").text
#print(volume_name)

## Find - volume titles - Method 2 - THIS WORKS
div_content = soup_papers.find("div", id="content").text
#print(div_content)

## CSV Names and Volume counter
jmlr = "JMLR "
fileEnd = ".csv"
counter_volumes = 0
for line in div_content.splitlines():
    if "Volume " in line:
        #print(line)
        csvName = jmlr + line + fileEnd
        csvName = csvName.replace(" ", "_")
        jmlr_volume_list.append(csvName) #NOTE: jmlr_volume_list[0] contains newest volume NOT oldest. Use reverse 
        counter_volumes += 1
        #print(csvName)
jmlr_volume_list.reverse() # NEED to reverse order so everything else makes sense. Old to New. 
#print(counter_volumes)
#print(jmlr_volume_list)

## Volume Link Creator - Creates urls for volumes - Example url: https://www.jmlr.org/papers/v20/
url_baseFront = "https://www.jmlr.org/papers/v" 
url_baseEnd = "/"
for n in range(1, counter_volumes+1):
    url_complete = url_baseFront + str(n) + url_baseEnd
    jmlr_link_list.append(url_complete)
    #print(url_complete)
#print(jmlr_link_list) #NOTE: jmlr_link_list[20]) -> "https://www.jmlr.org/papers/v21/"
## Volume[] Scraper

## Scraper Set Up - Volume[x]
# for n in range(counter_volumes): 
#     current_url = jmlr_link_list[n] 
#     print(current_url)
#     source_url_get = requests.get(current_url).text
#     soup_url = BeautifulSoup(source_url_get, 'lxml')
#     break
# #print(soup_url.prettify())

## CSV OUTPUT ##
# for n in range(counter_volumes):
    # current_volume = jmlr_volume_list[n]
    # current_title = jmlr_title_list[n]
    # current_abstract = jmlr_title_list[n]
    # current_authors = jmlr_authors_list[n]
    # current_keywords = jmlr_keywords_list[n]
    # current_affiliations = jmlr_affiliations_list[n]
    # current_month = jmlr_month_list[n]
    # current_link = jmlr_link_list[n]
    # current_journal_name = "Journal of Machine Learning Research"
    # current_year = jmlr_year_list[n]
    # current_volume = jmlr_volume_list[n]
    # current_issue = jmlr_issue_list[n]
    
#     with open(current_volume, 'w', newline='') as f:
        # csvWriter = csv.writer(f)
        # csvWriter.writerow(['title', 'abstract', 'authors', 'keywords', 'affiliations', 'month', 'link', 'journal_name', 'year', 'volume', 'issue'])
        # crvWriter.writerow([current_title, current_abstract, current_authors, current_keywords, current_affiliations, current_month, current_link, current_journal_name, current_year, current_volume, current_issue])  

## REGEX to find dates - NOT WORKING
# dateRegex = re.compile(r'January|February|March|April|May|June|July|August|September|October|November|December')
# dates = dateRegex.search(div_content)
# print(dates.group())
# for articles in soup_papers:
#      volume = soup_papers.find('volume')
#      print(volume)