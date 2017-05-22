# Date Created: 22-Mar-2017

import time
import json
from os import listdir
from os.path import isfile, join
from datetime import datetime
import re
import string

start_time = time.time()
print(datetime.now())
print()

# Array Parser for NBT

folder_list = ['automobile', 'business', 'editorial', 'education', 'jokes', 'lifestyle', 'movies', 'sports',
               'technology', 'world']

BASE_URL_PATTERN = '../data/nbt/{}/data/'
FILE_PATTERN = '../data/body/nbt/raw/{}.txt'
MAX_SIZE = 2500

tag = 'Story'

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
                news = jsondata['it']
                if tag in news:
                    content = ' '.join(news[tag].split())  # turn article into single line

                    # check sentences with little (< 5 words) or no hindi contents
                    tmp = re.sub(u'[^\u20B9\u0900-\u097F]', ' ', content)
                    tmp = ' '.join(tmp.split())
                    tmp = tmp.strip()

                    content = tmp
                    if tmp and tmp != "" and len(tmp.split()) > 5:
                        ulist.append(content)
                    else:
                        print("Empty: ", tag, 'tag in file', f)
                else:
                    print('Error:', tag, 'not found in file', f)
        except Exception as e:
            print(e, f)
    with open(FILE_PATTERN.format(folder), mode='w', encoding='utf-8') as outfile:
        outfile.write('\n'.join(ulist[:MAX_SIZE]))

print(datetime.now())
print("Total time: %s seconds" % (time.time() - start_time))
