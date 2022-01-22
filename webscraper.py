import requests

import string

import os

from bs4 import BeautifulSoup

url = 'https://www.nature.com/nature/articles?sort=PubDate&year=2020&page=1'

parent_directory = os.getcwd()
page_number = int(input())
type_of_articles = input()

links = []
full_links = []
article_names = []

def find_article():
    url_content = requests.get(url).content
    soup = BeautifulSoup(url_content, 'html.parser')
    soup_articles = soup.find_all('article')
    for article in soup_articles:
        article_type = article.find('span', "c-meta__type").text
        if article_type == type_of_articles:
            links.append(article.find('a').get('href'))

#find_article()


def convert_link():
    for link in links:
        full_link = 'https://nature.com' + link
        full_links.append(full_link)


#convert_link()

def access_contents():
    for name in full_links:
        link_content = requests.get(name).content
        content_soup = BeautifulSoup(link_content, 'html.parser')
        soup_title = content_soup.find('title').text
        modified_title = soup_title.translate(str.maketrans('','',string.punctuation))
        modified_title1 = modified_title.replace(' ','_')
        file_name = modified_title1 + '.txt'
        article_names.append(file_name)

        file = open(file_name, 'w', encoding='utf-8')
        soup_body = content_soup.find('div', {'class': "c-article-body u-clearfix"}).text
        body = soup_body.strip()
        body = body.replace("\n", "")
        file.write(body)
        file.close()

#access_contents()


#print(article_names)

for i in range(1, page_number+1):
    directory_name = 'Page_' + str(i)
    path = os.path.join(parent_directory, directory_name)
    os.mkdir(path)
    os.chdir(path)
    print(os.getcwd())
    find_article()
    convert_link()
    access_contents()

print('Saved all articles.')
