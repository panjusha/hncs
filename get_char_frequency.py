# Date Created: 19-Apr-2017

import time
import os
from datetime import datetime
import re
import string

start_time = time.time()
print(datetime.now())
print()

# Split data into train and test

INPUT_FOLDER = '../data/body/nbt/processed/'

files = [f for f in os.listdir(INPUT_FOLDER) if os.path.isfile(os.path.join(INPUT_FOLDER, f))]

freq = {}
other = {}

for file in files:

    input_path = os.path.join(INPUT_FOLDER, file)

    # read
    print("Reading", input_path)
    with open(input_path, encoding='utf-8') as input_file:
        lines = input_file.readlines()
        lines = [x.strip() for x in lines]

    for line in lines:
        for ch in line:
            freq[ch] = freq.get(ch, 0) + 1
            if re.match(u'[\u20B9\u0900-\u097F]', ch) is None: # devnagri / hindi unicode range (u20B9 is ₹: INR)
                other[ch] = 1

for k, v in freq.items():
    print((k, v))

print('Non-hindi')
for k in other:
    print((k, 0))

print(datetime.now())
print("Total time: %s seconds" % (time.time() - start_time))
