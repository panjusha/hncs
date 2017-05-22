# Date Created: 22-Mar-2017

import time
import json
from os import listdir
from os.path import isfile, join
from datetime import datetime

start_time = time.time()
print(datetime.now())
print()

# ERR for Navbharattimes
loc = 'automobile'
data_dir = '../data/nbt/{}/data/'.format(loc)
URL_FILE = '../data/nbt/{}/urls.txt'.format(loc)
ERR_FILE = '../data/nbt/{}/err.txt'.format(loc)

cnt = 0

files = [f for f in listdir(data_dir) if isfile(join(data_dir, f))]
fset = {}
for f in files:
    fset.setdefault(f, 0)
with open(URL_FILE) as ufile:
    lines = ufile.readlines()
with open(ERR_FILE, 'w') as outfile:
    for i in range(0, len(lines), 2):
        fname = lines[i + 1].strip().split('=')[1].strip()
        if fname not in fset:
            outfile.write(lines[i])
            outfile.write(lines[i + 1])
            cnt += 1

print("Count", cnt)
print(datetime.now())
print("Total time: %s seconds" % (time.time() - start_time))
