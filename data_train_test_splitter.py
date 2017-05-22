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
TRAIN_FOLDER = '../data/body/nbt/train/'
TEST_FOLDER = '../data/body/nbt/test/'

TRAIN_SIZE = 2000
MAX_SIZE = 2500

files = [f for f in os.listdir(INPUT_FOLDER) if os.path.isfile(os.path.join(INPUT_FOLDER, f))]

for file in files:

    input_path = os.path.join(INPUT_FOLDER, file)

    # read
    print("Reading", input_path)
    with open(input_path, encoding='utf-8') as input_file:
        lines = input_file.readlines()
        lines = [x.strip() for x in lines]

    # write
    train_path = os.path.join(TRAIN_FOLDER, file)
    test_path = os.path.join(TEST_FOLDER, file)

    with open(train_path, mode='w', encoding='utf-8') as outfile:
        print('train_path', train_path)
        outfile.write('\n'.join(lines[:TRAIN_SIZE]))
    with open(test_path, mode='w', encoding='utf-8') as outfile:
        print('test_path', test_path)
        outfile.write('\n'.join(lines[TRAIN_SIZE:MAX_SIZE]))

    print()

print(datetime.now())
print("Total time: %s seconds" % (time.time() - start_time))
