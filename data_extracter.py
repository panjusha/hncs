# Date Created: 22-Mar-2017

import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
from os import listdir
from os.path import isfile, join
import json

start_time = time.time()
print(datetime.now())

# Data Extracter for navbharattimes : Hindi News Archive

cnt = 0
success = 0
MAX_SUCCESS = -1
INPUT_DIR = '../data/navbharattimes/'
DATA_DIR = '../data/json/'

files = [f for f in listdir(INPUT_DIR) if isfile(join(INPUT_DIR, f))]
print('Processing {} files'.format(len(files)))

category_set = {}

print('{:<5} {:<10} {:<30} {:<20} {}'.format('S.No.', 'File ID', 'Date', 'Category', 'Title'))
for f in files:
    cnt += 1
    path = join(INPUT_DIR, f)
    idx = f[:-4]
    try:
        article = {}
        soup = BeautifulSoup(open(path, encoding='utf-8'), 'html.parser')
        category = soup.find('h2', class_='section_name').text.strip()
        title = soup.find('h1').text.strip()
        date_time = soup.find('div', class_='article_datetime').text.split(':')[-1].strip()
        article['category'] = category
        article['title'] = title
        article['date'] = date_time
        body = BeautifulSoup(str(soup.find('arttextxml')).replace('<br>', '\n').replace('</br>', ''),
                             'html.parser').text.strip()
        # remove extra white spaces
        article['body'] = '\n'.join([x.strip() for x in body.split('\n')])
        json.dump(article, open('{}{}.json'.format(DATA_DIR, idx), 'w', encoding='utf-8'),
                  ensure_ascii=False)
        category_set[category] = category_set.get(category, 0) + 1
        success += 1
        print('{:<5} {:<10} {:<30} {:<20} {}'.format(cnt, idx, date_time, category, title))
    except Exception as e:
        print('{:<5} {:<10} {}'.format(cnt, idx, e))
        print(e)
        pass
    if success == MAX_SUCCESS:
        break

print('{:<5} {}'.format('Count', 'Category'))
for cat, num in category_set.items():
    print('{:<5} {}'.format(num, cat))

print('Success: {}'.format(success))
print('Failed: {}'.format(cnt - success))

print("Total time: %s seconds" % (time.time() - start_time))
