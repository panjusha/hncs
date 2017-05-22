# Date Created: 22-Mar-2017

import time
from datetime import datetime
from os import listdir
from os.path import isfile, join
import json
from collections import defaultdict

start_time = time.time()
print(datetime.now())

# Data Parser for navbharattimes : Hindi News Archive

INPUT_DIR = '../data/json/'

files = [f for f in listdir(INPUT_DIR) if isfile(join(INPUT_DIR, f))]
print('Processing {} files'.format(len(files)))

category_set = defaultdict(int)

err = 0

for f in files:
    # print(f)
    path = join(INPUT_DIR, f)
    with open(path, encoding='utf-8') as data_file:
        try:
            article = json.load(data_file)
            category = article['category']
            category_set[category] += 1
        except Exception as e:
            err += 1
            print('File: {}, Error {}: {}'.format(f, err, e))

print('{:<5} {}'.format('Count', 'Category'))
for cat in sorted(category_set, key=category_set.get, reverse=True):
    print('{:<5} {}'.format(category_set[cat], cat))

print("Total time: %s seconds" % (time.time() - start_time))
