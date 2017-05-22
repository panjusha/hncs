# Date Created: 19-Apr-2017

import time
import os
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
import heapq

start_time = time.time()
print(datetime.now())
print()

# Data preprocessor: calculate tfidf

INPUT_TRAIN_FOLDER = '../data/body/nbt/train/'
INPUT_TEST_FOLDER = '../data/body/nbt/test/'
OUTPUT_TRAIN_FOLDER = 'cnn/data/train/'
OUTPUT_TEST_FOLDER = 'cnn/data/test/'

files = [f for f in os.listdir(INPUT_TRAIN_FOLDER) if os.path.isfile(os.path.join(INPUT_TRAIN_FOLDER, f))]

doc = {}
max_document_length = 100

# read
for file in files:
    input_path = os.path.join(INPUT_TRAIN_FOLDER, file)
    print("Reading", input_path)
    with open(input_path, encoding='utf-8') as input_file:
        doc[file] = input_file.read()


def tokenize(text):
    return text.split()


print('Calculating TFIDF')
tfidf_start_time = time.time()
tfidf_vectorizer = TfidfVectorizer(tokenizer=tokenize)
tfs = tfidf_vectorizer.fit(doc.values())
print("Tfidf time: %s seconds" % (time.time() - tfidf_start_time))

feature_names = tfidf_vectorizer.get_feature_names()
print('Num features:', len(feature_names))
word_idx = {}
for i in range(len(feature_names)):
    word_idx[feature_names[i]] = i


def process(filename, filedata, output_folder):
    output_path = os.path.join(output_folder, filename)
    lines = filedata.splitlines()
    res = []
    for line in lines:
        tfidf = tfidf_vectorizer.transform([line])
        words = tokenize(line)

        if len(words) == 0:
            print('Empty line in file:', file)

        # find top max_document_length words
        heap = []
        for word in words:
            if word in word_idx:
                col = word_idx[word]
                heap.append((-tfidf[0, col], word))
            else:
                print('Missing in word_idx:', word)

        if len(heap) == 0:
            print('Empty heap in file:', file, 'line:', line)

        heapq.heapify(heap)

        # extract ltr words with tfidf > min_val (and min_count words with tfidf == min_val)
        important_words = []
        while len(heap) > 0 and len(important_words) < max_document_length:
            t = heapq.heappop(heap)
            important_words.append(t[1])
        res.append(' '.join(important_words))

    print("Writing", output_path)
    with open(output_path, mode='w', encoding='utf-8') as out_file:
        out_file.write('\n'.join(res))


# process train data
for file, data in doc.items():
    process(file, data, OUTPUT_TRAIN_FOLDER)

# process test data
files = [f for f in os.listdir(INPUT_TEST_FOLDER) if os.path.isfile(os.path.join(INPUT_TEST_FOLDER, f))]
for file in files:
    input_path = os.path.join(INPUT_TEST_FOLDER, file)
    print("Reading", input_path)
    with open(input_path, encoding='utf-8') as input_file:
        process(file, input_file.read(), OUTPUT_TEST_FOLDER)

print(datetime.now())
print("Total time: %s seconds" % (time.time() - start_time))
