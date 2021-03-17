import requests

from bs4 import BeautifulSoup
word = input()
i = input()

r = requests.get(i)
soup = BeautifulSoup(r.content, 'html.parser')

target = soup.find_all('p')
for items in target:
    check = items.text
    if word in check:
        print(items.text)
