import requests
import os
from bs4 import BeautifulSoup
import urllib
import sys
import random
from pprint import pprint as pp
import json
import pandas as pd
import hashlib

sys.setrecursionlimit(200000)

desktop_agents = [
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0']

file_dir = 'pages/'


def random_headers():
    return {'User-Agent': random.choice(desktop_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}


def get_file(name):
    try:
        return open(file_dir + name, 'r', encoding='utf-8').read()
    except FileNotFoundError:
        return False


def save_file(name, data):
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    file = open(file_dir + name, 'wb')
    file.write(data.encode("utf-8"))
    file.close()


def get_page(url):
    name = hashlib.md5(url.encode('utf-8')).hexdigest()
    plain_text = get_file(name)
    if plain_text:
        return BeautifulSoup(plain_text, "html.parser")
    while True:
        try:
            plain_text = requests.get(url, headers=random_headers()).text
            save_file(name, plain_text)
            return BeautifulSoup(plain_text, "html.parser")
        except requests.exceptions.RequestException as e:
            print('RequestException')
            return False


def get_json_request(url):
    print(url)
    return requests.get(url, headers=random_headers()).content


def get_paper_info(paper):
    result = dict(
            title=paper.find('span', class_='title-text').text,
            abstract=None,
            authors=[],
            keywords=[],
            affiliations=[],
    )
    if paper.find('div', class_='Abstracts'):
        result['abstract'] = paper.find('div', class_='Abstracts').find('p').text

    authors = paper.find('div', class_='author-group')
    if authors:
        for author in authors.find_all('span', class_='content'):
            result['authors'].append(
                    author.find(class_='given-name').text + ' ' + author.find(class_='surname').text
            )
    keywords_sections = paper.find_all('div', class_='keywords-section')
    for keywords_section in keywords_sections:
        if not keywords_section.find('h2'):
            continue
        if 'Keywords' != keywords_section.find('h2').text:
            continue
        keywords = keywords_section.find_all('div', class_='keyword')
        for keyword in keywords:
            result['keywords'].append(keyword.find('span').text)

    affiliations = paper.find_all('dl', class_='affiliation')
    # TODO: check this part
    for affiliation in affiliations:
        result['affiliations'].append(affiliation.find('dd').text)

    publication = paper.find('div', class_='publication-volume u-text-center').find('div', class_='text-xs')
    result['month'] = publication.text.split(', ')[2].split(' ')[0]

    return result


if __name__ == '__main__':
    journal_name = 'Journal of Financial Economics'
    main_domain = 'https://www.sciencedirect.com/'
    main_path = 'https://www.sciencedirect.com/journal/0304405X/year/{}/issues'
    issue_path = 'https://www.sciencedirect.com/journal/journal-of-financial-economics/vol/{}/issue/{}'

    # for year in range(2020, 1974, -1):
    for year in [2020, 2019]:
        data = []
        print('year', year)
        year_issues = json.loads(get_json_request(main_path.format(year)))['data']
        print('total issues', len(year_issues))
        for year_issue in year_issues:
            issue = get_page(issue_path.format(year_issue['volumeFirst'], year_issue['issueFirst']))
            paper_links = issue.find_all('a', class_='anchor article-content-title u-margin-xs-top u-margin-s-bottom')
            print('total papers', len(paper_links))
            for i, paper_link in enumerate(paper_links):
                print(i, paper_link['href'])
                paper = get_page(main_domain + paper_link['href'])
                data_tmp = get_paper_info(paper)
                data_tmp['link'] = main_domain + paper_link['href']
                data_tmp['journal_name'] = journal_name
                data_tmp['year'] = year
                data_tmp['volume'] = year_issue['volumeFirst']
                data_tmp['issue'] = year_issue['issueFirst']
                data.append(data_tmp)
        df = pd.DataFrame(data)
        df.to_csv(journal_name.replace(' ', '_') + '_' + str(year) + '.csv', index=False)

        pp(df.head())
