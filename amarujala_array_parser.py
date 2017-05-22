# Date Created: 22-Mar-2017

import time
import json
from os import listdir
from os.path import isfile, join
from datetime import datetime

start_time = time.time()
print(datetime.now())
print()

# Array Parser for Amar Ujala

folder_list = ['education', 'fashion', 'astrology', 'spirituality']

BASE_URL_PATTERN = '../data/amarujala/new/{}/array/'
URL_FILE_PATTERN = '../data/amarujala/new/{}/urls.txt'

type_freq = {}

for folder in folder_list:
    print(folder)
    INPUT_DIR = BASE_URL_PATTERN.format(folder)
    files = [f for f in listdir(INPUT_DIR) if isfile(join(INPUT_DIR, f))]
    ulist = []
    for f in files:
        # print(f)
        path = join(INPUT_DIR, f)
        try:
            with open(path) as jsonfile:
                jsondata = json.load(jsonfile)
                news = jsondata['news']
                for i in range(len(news)):
                    news_type = str(news[i]['news_type']).strip()
                    ulist.append(str(news[i]['News_detail']).strip())
                    type_freq[news_type] = type_freq.get(news_type, 0) + 1
        except Exception as e:
            print(e)
    with open(URL_FILE_PATTERN.format(folder), 'w') as outfile:
        outfile.write('\n'.join(ulist))

total = 0
print()
print('{:<6} {}'.format('Count', 'News Type'))
for t in sorted(type_freq, key=type_freq.get, reverse=True):
    print('{:<6} {}'.format(type_freq[t], t))
    total += type_freq[t]

print()
print('Total', total)

print(datetime.now())
print("Total time: %s seconds" % (time.time() - start_time))
