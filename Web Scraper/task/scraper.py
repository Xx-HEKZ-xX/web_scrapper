import sys

import requests
from bs4 import BeautifulSoup
import os
import re


def main():
    page = int(input())
    type_a = input()
    filename_list = []
    base_dir = os.getcwd()
    for i in range(0, page):
        news_links = search_links(i, type_a)
        dir_name = f"page_{i + 1}"
        os.mkdir(dir_name)

        os.chdir(base_dir + r"\\" + dir_name)

        for x in news_links:
            soup = setup(x)
            title = soup.find('h1', class_='article-item__title').text.strip()

            regex = re.compile(".*body.*")
            pseudo_body = soup.find('div', attrs={'class': regex}).find_all(['p', 'h2'])
            body = ''
            for n in pseudo_body:
                body += n.text
            print(title)
            convert = str.maketrans({' ': '_', '?': '', ':': '', '-': ''})
            title_for_filename = title.translate(convert)
            filename = f'{title_for_filename}.txt'
            filename_list.append(filename)

            with open(filename, 'wb') as f:
                f.write(body.encode('utf-8'))

        os.chdir(base_dir)
    print('Saved all articles')
    return 0


def search_links(page_no, types):
    soup = setup(
        'https://www.nature.com/nature/articles?searchType=journalSearch&sort=PubDate&page=' + str(page_no + 1))
    articles = soup.find_all('article')
    news_resources = []
    for x in articles:
        resource = x.find('div', class_="c-card__body u-display-flex u-flex-direction-column")
        article_type = resource.find('div', class_='u-mt-auto').div.span.span.text
        article_link = resource.h3.a.get('href')
        if article_type != types:
            continue
        else:
            news_resources.append('https://www.nature.com' + article_link)
    return news_resources


def check(data):
    if data.status_code != 200:
        print(data.status_code)
        print('Invalid url!')
        sys.exit()
    else:
        return None


def setup(url):
    input_pseudo_data = requests.get(url)
    check(input_pseudo_data)
    input_data = input_pseudo_data.content
    soup = BeautifulSoup(input_data, 'html.parser')
    return soup


if __name__ == '__main__':
    main()
