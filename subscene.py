#!/usr/bin/env python3

import json
import requests
from pprint import pprint
from tqdm import tqdm
from bs4 import BeautifulSoup as bs4
from os.path import expanduser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import re
import time
import sys

url = 'https://subscene.com/'

testing_mode = False

if not testing_mode:
    args = sys.argv
    if len(args) < 2:
        print('Please enter a movie name')
        exit()

    name = ' '.join(args[1:])

    name = re.split(r'[ \.]', name)

    max_top = len(name)
    for i,x in enumerate(name):
        if re.search('S\d+|Season.*|\(.*|((19|20)\d{2})', x):
            max_top = i
    name = ' '.join(name[:max_top])
    print(f'Searching subscene for "{name}"')

    chromedriver = '/usr/local/bin/chromedriver'
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1200x600')
    options.add_argument('chromever="73.0.3683.68"')

    browser = webdriver.Chrome(chromedriver, options=options)
    browser.get(url)

    login = browser.find_element_by_id('query')
    login.send_keys(f"{name}\n")

    d = dict()
    soup = bs4(browser.page_source, 'html.parser')
    browser.quit()

    idx = 0
    for x in soup.find_all('div', {'class':'title'}):
        for a in x.find_all('a'):
            if len(d) == 0:
                d[idx] = {'url':f"{url}{a['href']}", 'name':a.contents[0]}
                idx += 1
            elif not any(v['name'] == a.contents[0] for v in d.values()):
                d[idx] = {'url':f"{url}{a['href']}", 'name':a.contents[0]}
                idx += 1
                # print(i, f"{url}{a['href']}", a.contents[0])

    print()
    print('\n'.join(f'{str(k).rjust(len(str(idx)), " ")}: {v["name"]}' for k,v in d.items()))
    print('Chose a number')
    try:
        user_in = int(input())
    except Exception as e:
        user_in = -1
    while user_in not in d.keys():
        print('Please enter a valid number')
        print('\n'.join(f'{str(k).rjust(len(str(idx)), " ")}: {v["name"]}' for k,v in d.items()))
        try:
            user_in = int(input())
        except Exception as e:
            user_in = -1
    # pprint(d)
    # time.sleep(3)

if testing_mode:
    tester = 'https://subscene.com/subtitles/men-in-black-international'
    html = requests.get(tester).text
else:
    html = requests.get(d[user_in]['url']).text

soup = bs4(html, 'html.parser')
l = []
for x in soup.find_all('a', {'href':True}):
    for y in x.find_all('span'):
        if 'English' == y.contents[0].strip():
            l.append(x)
d = {}
idx = 0
for x in l:
    # print(x.previous_element.previous_element.previous_element.previous_element.prettify())
    # print('\n\n\n\n\n')

    parent = x.previous_element.previous_element.previous_element.previous_element
    # print(parent.prettify())
    file = parent.find_all('span')[1].contents[0].rstrip().strip().replace('/', '')
    try:
        author = parent.find_all('td', {'class':'a5'})[0].find_all('a')[0].contents[0].rstrip().strip()
    except Exception as e:
        author = 'Anonymous'
    desc = parent.find_all('div')[0].contents[0].rstrip().strip().replace('\n', ' ')
    link = url+parent.find('a')['href']
    # print(link, any(link == v['url'] for v in d.values()))
    if len(d) == 0:
        d[idx] = {'file':file[:50], 'author':author[:20], 'desc': '\n\t' + desc[:80], 'url':link}
        idx += 1
    elif not any(link == v['url'] for v in d.values()):
        d[idx] = {'file':file[:50], 'author':author[:20], 'desc': '\n\t' + desc[:80], 'url':link}
        idx += 1
# exit()
files = [len(x['file']) for x in d.values()]
authors = [len(x['author']) for x in d.values()]
descs = [len(x['desc']) for x in d.values()]

maxf = max(files) + 4
maxa = max(authors) + 4
maxa = 0
maxd = max(descs) + 4
maxd = 0

def format_line(v):
    p1 = f"{v['file']}{' '*(maxf - len(v['file']))}"
    p2 = f"{v['author']}{' '*(maxa - len(v['author']))}"
    p3 = f"{v['desc']}{' '*(maxd - len(v['desc']))}"
    return p1+p2+p3+('\n' * (len(v['desc'].strip()) != 0))

print()
print('\n'.join(f"{str(k).rjust(len(str(idx)), ' ')}: {format_line(v)}" for k,v in d.items()))
print('Chose a number')
user_in = int(input())
while user_in not in d.keys():
    print('Please enter a valid number')
    print('\n'.join(f"{str(k).rjust(len(str(idx)), ' ')}: {format_line(v)}" for k,v in d.items()))
    user_in = int(input())

html = requests.get(d[user_in]['url']).text
soup = bs4(html, 'html.parser')
dl = soup.find('div', {'class':'download'})
dl = dl.find('a', {'onclick':'DownloadSubtitle(this)'})
r = requests.get(url+dl['href'])
open(f'{d[user_in]["file"]}.zip', 'wb').write(r.content)
