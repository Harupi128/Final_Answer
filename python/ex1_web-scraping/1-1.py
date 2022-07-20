from unittest import result
import requests
from bs4 import BeautifulSoup
import re
import csv
import os
import unicodedata
import time

results = []
head = ['店舗名', '電話番号', 'メールアドレス', '都道府県', '市区町村', '番地', '建物名']

headers = {
    'User-Agent': 'PyQ Example Crawler/1.0.0 (http://pyq.jp)'
    }

url = 'https://r.gnavi.co.jp/area/aream2115/rs/'
time.sleep(3)
response = requests.get(url)
bs = BeautifulSoup(response.text, 'html.parser')
div_tags = bs.find_all('div', class_ = 'style_restaurant__SeIVn')
links = []
for div in div_tags:
    h2_tag = div.find('a')
    links.append(h2_tag.get('href'))
    if len(links) >= 50:
        break


url = 'https://r.gnavi.co.jp/area/aream2115/rs/?p=2'
time.sleep(3)
response = requests.get(url)
bs = BeautifulSoup(response.text, 'html.parser')
div_tags = bs.find_all('div', class_ = 'style_restaurant__SeIVn')
for div in div_tags:
    h2_tag = div.find('a')
    links.append(h2_tag.get('href'))
    if len(links) >= 50:
        break


url = 'https://r.gnavi.co.jp/area/aream2115/rs/?p=3'
time.sleep(3)
response = requests.get(url)
bs = BeautifulSoup(response.text, 'html.parser')
div_tags = bs.find_all('div', class_ = 'style_restaurant__SeIVn')
for div in div_tags:
    h2_tag = div.find('a')
    links.append(h2_tag.get('href'))
    if len(links) >= 50:
        break


for link in links:
    data = []
    time.sleep(3)
    response1 = requests.get(link)
    bs1 = BeautifulSoup(response1.content, 'html.parser')
    store_name_code = bs1.find('p', class_ = 'fn org summary')
    store_name = unicodedata.normalize("NFKD", store_name_code.get_text())
    tel = bs1.find('span', class_ = 'number')
    address = bs1.find('span', class_ = 'region')
    pattern = '''(...??[都道府県])([^0-9]+)(.+)'''
    res = re.match(pattern, address.get_text())
    locality = bs1.find('span', class_ = 'locality')

    if locality is None:
        locate = ''
    else:
        locate = locality.get_text()
    mailto = bs1.find('a',href=re.compile('mailto'))
    if mailto is not None:
        mail = re.sub("mailto:", '', mailto.get('href'))
    else:
        mail = ''
    data.append(store_name)
    data.append(tel.get_text())
    data.append(mail)
    if res:
        data.append(res.group(1))
        data.append(res.group(2))
        data.append(res.group(3))
    data.append(locate)
    results.append(data)

with open('1-1.csv', 'w', newline='', encoding='utf_8_sig') as f:
    writer = csv.writer(f)
    writer.writerow(head)
    writer.writerows(results)