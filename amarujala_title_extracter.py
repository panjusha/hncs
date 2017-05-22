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

folder_list = ['automobiles', 'business', 'crime', 'education', 'entertainment', 'fashion', 'jobs', 'lifestyle',
               'sports', 'technology']

BASE_URL_PATTERN = '../data/amarujala/{}/array/'
TRAIN_FILE_PATTERN = '../data/title/amarujala/train/{}.txt'
TEST_FILE_PATTERN = '../data/title/amarujala/test/{}.txt'
TRAIN_SPLIT = 0.2

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
                    ulist.append(str(news[i]['News-Synopsis']).strip().replace('\r', ' ').replace('\n', ' '))
        except Exception as e:
            print(e)
    split_loc = int(TRAIN_SPLIT * len(ulist))
    with open(TRAIN_FILE_PATTERN.format(folder), mode='w', encoding='utf-8') as outfile:
        outfile.write('\n'.join(ulist[:split_loc]))
    with open(TEST_FILE_PATTERN.format(folder), mode='w', encoding='utf-8') as outfile:
        outfile.write('\n'.join(ulist[split_loc:]))


print(datetime.now())
print("Total time: %s seconds" % (time.time() - start_time))
