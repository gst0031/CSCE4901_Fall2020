## Web scraper for Journal of Machine Learning Research - https://www.jmlr.org/papers/
# Can get from an html file or a web page - This will pull from webpage

from bs4 import BeautifulSoup
import requests
import re #regex
import csv

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
list_volumes = []
counter_volumes = 0
for lines in div_content.splitlines():
    if "Volume " in lines:
        csvName = jmlr + lines + fileEnd
        csvName = csvName.replace(" ", "_")
        list_volumes.append(csvName)
        counter_volumes += 1
        #print(csvName)
#print(counter_volumes)
#print(list_volumes)

## CSV OUTPUT ##
for n in range(counter_volumes):
    current_volume_name = list_volumes[n]
    with open(current_volume_name, 'w', newline='') as f:
        csvWriter = csv.writer(f)
        csvWriter.writerow(['title', 'abstract', 'authors', 'keywords', 'affiliations', 'month', 'link', 'journal_name', 'year', 'volume', 'issue'])


# # REGEX to find dates
# dateRegex = re.compile(r'January|February|March|April|May|June|July|August|September|October|November|December')
# dates = dateRegex.search(div_content)
# print(dates.group())
# for articles in soup_papers:
#      volume = soup_papers.find('volume')
#      print(volume)