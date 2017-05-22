# Date Created: 22-Mar-2017

import requests
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
from urllib.parse import urljoin
import time

start_time = time.time()

# Crawler for navbharattimes : Hindi News Archive

# requirements:
# 1. requests : pip install requests
# 2. pip install beautifulsoup4

# Crawl from id 37257 (Jan 1, 2002) to 42735 (Dec 31, 2016) : total 5478 days
PATH_PATTERN = 'http://navbharattimes.indiatimes.com/archivelist/starttime-{}.cms'
START_TIME_MIN = 42675  # (Nov 1, 2016)
START_TIME_MAX = 42704  # (Nov 30, 2016)

URLS_FILE = '../data/urls.txt'

total_number_of_urls_extracted = 0

only_div_tags_with_class_normtxt = SoupStrainer("div", class_="normtxt")

hs = {}


def extract_urls(list_url):
    print(list_url)
    u = []
    r = requests.get(list_url)
    if r.status_code == requests.codes.ok:
        div = BeautifulSoup(r.text, 'html.parser', parse_only=only_div_tags_with_class_normtxt)
        if div is not None:
            a = div.find_all('a')
            for i in range(len(a)):
                u.append(urljoin(list_url, a[i].get('href')))
                # print(len(u), a[i].get_text())
    else:
        print(r.status_code, r.url)
    return u


with open(URLS_FILE, mode='w', encoding='utf-8') as urlsfile:
    for start_time in range(START_TIME_MIN, START_TIME_MAX + 1):
        list_url = PATH_PATTERN.format(start_time)
        urls = extract_urls(list_url)
        total_number_of_urls_extracted += len(urls)
        uniq = []
        for url in urls:
            if url in hs:
                print('duplicate', url)
            else:
                uniq.append(url)
                hs.setdefault(url, 0)
        if len(uniq) > 0:
            urlsfile.write('\n'.join(uniq) + '\n')
        print('number_of_urls_extracted:', total_number_of_urls_extracted)

print('total_number_of_urls_extracted:', total_number_of_urls_extracted)
print('unique:', len(hs))

print("Total time: %s seconds" % (time.time() - start_time))
