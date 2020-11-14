## Web scraper for Journal of Machine Learning Research - https://www.jmlr.org/papers/
# Can get from an html file or a web page - This will pull from webpage
# Santosh Khadka santoshkhadka@my.unt.edu

from bs4 import BeautifulSoup
import requests
import re #regex
import csv
import unidecode #transliterates any unicode string into the closest possible representation in ascii text. ex) newTest = unidecode.unidecode(oldString)
## TO DO: What to do about special character with accents?? unidecode did NOT work

## CSV Column variables/lists
jmlr_title_list = []    # Turns into 2D list
jmlr_abstract_list = [] # Turns into 2D list
jmlr_abstract_URL_list = [] # Turns into 2D list
jmlr_authors_list = []  # Turns into 2D list
jmlr_keywords_list = [] # Turns into 2D list
jmlr_affiliations_list = [] # Turns into 2D list
jmlr_month_list = []    # Turns into 2D list
jmlr_volume_url_list = [] 
jmlr_journal_name = "Journal of Machine Learning Research"
jmlr_year_list = [] # Turns into 2D list
jmlr_volume_list = [] 
jmlr_issue_list = []    # Turns into 2D list

## Scraper Set Up - ALL Volumes 
source_volumes = requests.get('https://www.jmlr.org/papers/').text
soup_papers = BeautifulSoup(source_volumes, 'lxml')
#print(soup_papers.prettify()) # !Testing

## Find - volume titles - Method 2 - #NOTE: This <div id=content> works for most pages.
div_content = soup_papers.find("div", id="content").text
#print(div_content) # !Testing

## CSV Names Creator & Volume counter - Used to count number of volumes and to create .csv file names
jmlr = "JMLR "
fileEnd = ".csv"
counter_volumes = 0
for line in div_content.splitlines():
    if "Volume " in line:
        #print(line) # !Testing
        csvName = jmlr + line + fileEnd
        csvName = csvName.replace(" ", "_")
        jmlr_volume_list.append(csvName) #NOTE: jmlr_volume_list[0] contains newest volume NOT oldest. Use reverse 
        counter_volumes += 1
        #print(csvName)
jmlr_volume_list.reverse() # NEED to reverse order so everything else makes sense. Old to New. 
#print(counter_volumes) # !Testing
#print(jmlr_volume_list) # !Testing

# Setup 2D lists - Title, Abstract, Author, keywords, affiliation, month, link, jorunal name, year, volume, issue
# for n in range(counter_volumes):
#     jmlr_title_list.append([])


## Volume Link Creator - Creates urls for volumes - Example url: https://www.jmlr.org/papers/v20/
url_baseFront = "https://www.jmlr.org/papers/v" 
url_baseEnd = "/"
for n in range(1, counter_volumes+1):
    url_complete = url_baseFront + str(n) + url_baseEnd
    jmlr_volume_url_list.append(url_complete)
    #print(url_complete)
#print(jmlr_volume_url_list) #NOTE: jmlr_volume_url_list[20]) -> "https://www.jmlr.org/papers/v21/" # !Testing


#### Scraper for Volume[x] - Title, Authors, Month, Year
## TITLE Scraper
seperator = "(" # Used to remove "(Kernel Machines Section)" &  "(Special Topic on Learning Theory)"
for n in range(counter_volumes):
# NOTE HOW STORAGE WORKS: JMLR Journal -> Volume[x] -> Volume[x].title[n]. 2D List - Volume[x] is the first list(row) and the titles[x] in the volumes are the 2nd list.  
    current_url = jmlr_volume_url_list[n] 
    #print("################# ", current_url) # !Testing
    source_url_get = requests.get(current_url).text
    soup_url = BeautifulSoup(source_url_get, 'lxml')
    current_volume_titles_list = []
    current_volume_authors_list = []
    
    # TITLE get: Volumes 1-4: Get everything in <tables> tag then everything in <dt> tag -> Paper titles. 
    if (n < 4): # HTML changes in Volumes 5 and up - no <table> tag just <dt>
        current_volume_table = soup_url.find("table", cellspacing="0")
        #print(current_volume_table) # !Testing
        current_volume_titles = current_volume_table.find_all("dt")
    else:   # Volumes >= 5 have different html setup
        current_volume_content = soup_url.find("div", id="content")
        #print(current_volume_content) # !Testing
        current_volume_titles = current_volume_content.find_all("dt")
    
    # TITLE get: Title of paper in Volume[x]
    for x in range(len(current_volume_titles)):
        current_volume_titles[x] = current_volume_titles[x].text.strip().replace('\n', '').replace("  ", ' ')
        string1 = str(current_volume_titles[x])
        #print(string1) # !Testing
        if ("(Kernel" in string1) or ("(Special" in string1):
            current_volume_titles[x] = string1.split(seperator, 1)[0]
        current_volume_titles[x] = str(current_volume_titles[x]).strip()
        current_volume_titles_list.append(current_volume_titles[x]) # current_volume_titles_list gets reset because of the parent loop
        #print(current_volume_titles[x]) # !Testing
    # print(len(jmlr_title_list)) # !Testing
    jmlr_title_list.append(current_volume_titles_list)
    #break # !Testing - To check if it works at least once. Leave commented to run through all volumes
#print(jmlr_title_list[0]) # !Testing
#print(jmlr_title_list[0][1]) # !Testing

## AUTHOR Scraper 
for n in range(counter_volumes):
    # NOTE HOW STORAGE WORKS: JMLR Journal -> Volume[x] -> Volume[x].author[n]. 2D List - Volume[x] is the first list(row) and the author[x] in the volumes are the 2nd list.
    current_url = jmlr_volume_url_list[n]
    #print("################# ", current_url) # !Testing 
    source_url_get = requests.get(current_url).text
    soup_url = BeautifulSoup(source_url_get, 'lxml')
    current_volume_authors_list = []   
    
    # AUTHOR get: Get evertyhing in <table> -> <div id=content> -> <b> : Author names   
    if (n < 4):
        current_volume_table = soup_url.find("table", cellspacing="0")
        current_volume_bTag = current_volume_table.find_all("b")
    else:
        current_volume_table = soup_url.find("div", id="content")
        current_volume_bTag = current_volume_table.find_all("b")
    
    # AUTHOR get: Author of paper in Volume[x]
    for x in range(len(current_volume_bTag)):
        current_volume_bTag[x] = current_volume_bTag[x].text.strip().replace('\n', '').replace("  ", ' ')
        string1 = str(current_volume_bTag[x].strip())
        #print(string1) # !Testing
        current_volume_authors_list.append(string1) # current_volume_titles_list gets reset because of the parent loop
       #print(current_volume_authors_list[x]) # !Testing
    #print(len(current_volume_authors_list)) # !Testing
    jmlr_authors_list.append(current_volume_authors_list)
    #break # !Testing - To check if it works at least once. Leave commented to run through all volumes
#print(jmlr_authors_list) # !Testing

## ABSTRACT URL Scraper 
for n in range(counter_volumes):
    # NOTE HOW STORAGE WORKS:   
    current_url = jmlr_volume_url_list[n]
    #print("################# ", current_url) # !Testing 
    source_url_get = requests.get(current_url).text
    soup_url = BeautifulSoup(source_url_get, 'lxml')
    abstractURL_list = []   
    
    # ABSTRACT URL get: Get evertyhing in <table> -> <a> -> "[abs]" : Abstract urls
    current_volume_table = soup_url.find("div", id="content")
    current_volume_aTag = current_volume_table.find_all("a")
    for i in range(len(current_volume_aTag)):
        if ("[abs]" in str(current_volume_aTag[i])) or (">abs<" in str(current_volume_aTag[i])):
            string1 = str(current_volume_aTag[i])
            string1 = string1.split('"')
            if (n < 3):
                string1 = (current_url+string1[1]).replace(" ", '')
                print(string1)
            elif((n==3) or (n==4)):
                string1 = (string1[1]).replace(" ", '')
                print(string1)
            else:
                string1 = "http://www.jmlr.org"+((string1[1]).replace(" ", ''))
                print(string1)    
            abstractURL_list.append(string1)
    jmlr_abstract_URL_list.append(abstractURL_list)
    #print(len(jmlr_abstract_URL_list[n])) # !Testing
#print(jmlr_abstract_URL_list[20]) # !Testing - Prints All URLs for Volume 21
#print(jmlr_abstract_URL_list[20][0]) # !Testing - Prints First URL for Volume 21

## ABSTRACT Scraper
# for x in range(len(jmlr_abstract_URL_list)):
#     for y in range(len(jmlr_abstract_URL_list[x])):
#         # NOTE HOW STORAGE WORKS: jmlr_abstract_URL_list[x][y] : x is volume[x] and y is url[y] in volume[x]
#         current_url = jmlr_abstract_URL_list[x][y]
#         #print("################# ", current_url) # !Testing 
#         source_url_get = requests.get(current_url).text
#         soup_url = BeautifulSoup(source_url_get, 'lxml')
#         current_volume_abstract_list = []      

        # ABSTRACT get: Get evertyhing in <table> -> <a> -> "[abs]" : Abstract urls
        #current_volume_table = soup_url.find("div", id="content")
        #current_volume_aTag = current_volume_table.find_all("h3")
        #print()
        # for i in range(len(current_volume_aTag)):
        #     if ("[abs]" in str(current_volume_aTag[i])) or (">abs<" in str(current_volume_aTag[i])):
        #         string1 = str(current_volume_aTag[i])
        #         string1 = string1.split('"')
        #         string1 = (current_url+string1[1]).replace(" ", '')
        #     abstractURL_list.append(string1)
        # jmlr_abstract_URL_list.append(abstractURL_list)
        #print(len(jmlr_abstract_URL_list[n])) # !Testing
    #break
#print(jmlr_abstract_URL_list) # !Testing


## CSV OUTPUT ##
# for n in range(counter_volumes):
#     current_volume = jmlr_volume_list[n]
#     current_title = jmlr_title_list[n]
#     # current_abstract = jmlr_title_list[n]
#     # current_authors = jmlr_authors_list[n]
#     # current_keywords = jmlr_keywords_list[n]
#     # current_affiliations = jmlr_affiliations_list[n]
#     # current_month = jmlr_month_list[n]
#     current_link = jmlr_volume_url_list[n]
#     current_journal_name = "Journal of Machine Learning Research"
#     # current_year = jmlr_year_list[n]
#     # current_volume = jmlr_volume_list[n]
#     # current_issue = jmlr_issue_list[n]
    
#     with open(current_volume, 'w', newline='') as f:
#         csvWriter = csv.writer(f)
#         csvWriter.writerow(['title', 'abstract', 'authors', 'keywords', 'affiliations', 'month', 'link', 'journal_name', 'year', 'volume', 'issue'])
#         # csvWriter.writerow([current_title, 'abs', 'auth', 'key', 'aff', 'month', current_link, current_journal_name, 'year', 'vol', 'issue'])
#     #     # csvWriter.writerow([current_title, current_abstract, current_authors, current_keywords, current_affiliations, current_month, current_link, current_journal_name, current_year, current_volume, current_issue])  

## REGEX to find dates - NOT WORKING
# dateRegex = re.compile(r'January|February|March|April|May|June|July|August|September|October|November|December')
# dates = dateRegex.search(div_content)
# print(dates.group())
# for articles in soup_papers:
#      volume = soup_papers.find('volume')
#      print(volume)