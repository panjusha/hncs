# Date Created: 22-Mar-2017

import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
import json

start_time = time.time()
print(datetime.now())

# Crawler for navbharattimes : Hindi News Archive

cnt = 0
success = 0
MAX_SUCCESS = -1
DATA_DIR = '../data/json/'
URLS_FILE = '../data/urls.txt'
START = 201

print('{:<7} {:<7} {:<7} {:<10} {}'.format('S.No.', 'Success', 'Status', 'News ID', 'URL'))
with open(URLS_FILE) as urls:
    with requests.Session() as s:
        for url in urls:
            if url:
                cnt += 1
                if cnt < START:
                    continue
                id = url.split('/')[-1].strip().split('.')[0]
                try:
                    r = s.get(url.strip())
                    if r.status_code == requests.codes.ok:
                        article = {}
                        soup = BeautifulSoup(r.text, 'html.parser')
                        article['category'] = soup.find('h2', class_='section_name').text.strip()
                        article['title'] = soup.find('h1').text.strip()
                        article['date'] = soup.find('div', class_='article_datetime').text.split(':')[-1].strip()
                        body = BeautifulSoup(str(soup.find('arttextxml')).replace('<br>', '\n').replace('</br>', ''),
                                             'html.parser').text.strip()
                        # remove extra white spaces
                        article['body'] = '\n'.join([x.strip() for x in body.split('\n')])
                        json.dump(article, open('{}{}.json'.format(DATA_DIR, id), 'w', encoding='utf-8'),
                                  ensure_ascii=False)
                        success += 1
                    print('{:<7} {:<7} {:<7} {:<10} {}'.format(cnt, success, r.status_code, id, r.url))
                except Exception as e:
                    print('{:<7} {:<7} {:<7} {:<10} {}'.format(cnt, success, -1, id, url))
                    print(e)
                    pass
                if success == MAX_SUCCESS:
                    break

print("Total time: %s seconds" % (time.time() - start_time))
