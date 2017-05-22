# Date Created: 22-Mar-2017

import time
import json
from os import listdir
from os.path import isfile, join
from datetime import datetime

start_time = time.time()
print(datetime.now())
print()

# Array Parser for Navbharattimes

folder_list = ['automobile', 'business', 'editorial', 'education', 'jokes', 'lifestyle', 'movies', 'sports', 'technology', 'world']

BASE_URL_PATTERN = '../data/nbt/{}/array/'
URL_FILE_PATTERN = '../data/nbt/{}/urls.txt'

DOWNLOAD_URL_PATTERN = 'http://navbharattimes.indiatimes.com/feeds/appnavigationshowv3next.cms?feedtype=sjson&version=v4&tag=news&msid={}&isnative=true'
OUT_NAME = ' out={}.json'

idset = {}
dup = 0
limit = 2500
total = 0

for folder in folder_list:
    print(folder)
    INPUT_DIR = BASE_URL_PATTERN.format(folder)
    files = [f for f in listdir(INPUT_DIR) if isfile(join(INPUT_DIR, f))]
    ulist = []
    for f in files:
        # print(f)
        path = join(INPUT_DIR, f)
        try:
            with open(path, encoding='utf-8') as jsonfile:
                jsondata = json.load(jsonfile)
                news = jsondata['items']
                for i in range(len(news)):
                    if 'id' in news[i]:
                        idx = str(news[i]['id']).strip()
                        if idx in idset:
                            print("Duplicate", idx)
                            dup += 1
                        else:
                            ulist.append(DOWNLOAD_URL_PATTERN.format(idx))
                            ulist.append(OUT_NAME.format(idx))
                            idset.setdefault(idx, 0)
        except Exception as e:
            print(e)
    print("Count", len(ulist)/2)
    total += len(ulist)/2
    with open(URL_FILE_PATTERN.format(folder), 'w') as outfile:
        outfile.write('\n'.join(ulist))

print("\nNumber of duplicates", dup)
print("total", total)
print(datetime.now())
print("Total time: %s seconds" % (time.time() - start_time))
