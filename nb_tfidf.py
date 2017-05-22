# Date Created: 22-Mar-2017

import time
from datetime import datetime
import math
from sklearn import metrics
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2, mutual_info_classif



start_time = time.time()
print(datetime.now())
print()

# Naive Bayes train

class_list = ['automobile', 'business', 'editorial', 'education', 'jokes', 'lifestyle', 'movies', 'sports',
              'technology', 'world']

TRAIN_FILE_PATTERN = 'cnn/data/train/{}.txt'
TEST_FILE_PATTERN = 'cnn/data/test/{}.txt'

train_data = []
train_target = []

test_data = []
test_target = []

def tokenizer(text):
    return text.strip().split()

for i in range(len(class_list)):
    cls = class_list[i]
    print("Loading", cls)
    with open(TRAIN_FILE_PATTERN.format(cls), mode='r', encoding='utf-8') as file:
        lines = file.readlines()
        train_data += lines
        train_target += ([i] * len(lines))

text_clf = Pipeline([('vect', CountVectorizer(tokenizer=tokenizer)),
                     # ('feature_selection', SelectKBest(mutual_info_classif, k=15000)),
                     # ('tfidf', TfidfTransformer()),
                     ('clf', MultinomialNB()),
                     ])

print('Training')
text_clf = text_clf.fit(train_data, train_target)

print(datetime.now())
print("Train time: %s seconds" % (time.time() - start_time))
print()

# test
start_time = time.time()
for i in range(len(class_list)):
    cls = class_list[i]
    print("Loading", cls)
    with open(TEST_FILE_PATTERN.format(cls), mode='r', encoding='utf-8') as file:
        lines = file.readlines()
        test_data += lines
        test_target += ([i] * len(lines))


all_predictions = text_clf.predict(test_data)
correct_lines = 0
total_lines = len(test_target)

confusion = [[0 for x in range(len(class_list))] for y in range(len(class_list))]

for i in range(len(all_predictions)):
    if all_predictions[i] == test_target[i]:
        correct_lines += 1
    confusion[test_target[i]][all_predictions[i]] += 1


# print()
# print("Out of Vocabulary:", oov, "/", tot, "=", oov/tot)
# print()

print(datetime.now())
print("Test time: %s seconds" % (time.time() - start_time))
print()
print("Accuracy", correct_lines, "/", total_lines, "=", correct_lines / total_lines)

# calc precision, recall and f1-avg (macro)
tp = [0 for x in range(len(class_list))]
tn = [0 for x in range(len(class_list))]
fp = [0 for x in range(len(class_list))]
fn = [0 for x in range(len(class_list))]

pre = [0 for x in range(len(class_list))]
rec = [0 for x in range(len(class_list))]
f1 = [0 for x in range(len(class_list))]

f1_avg = 0

row_sum = [0 for x in range(len(class_list))]
col_sum = [0 for x in range(len(class_list))]

print('\nConfusion:')
for i in range(len(class_list)):
    print('{:<10}'.format(class_list[i]), confusion[i])
    for j in range(len(class_list)):
        row_sum[i] += confusion[i][j]
        col_sum[j] += confusion[i][j]

print()
print('{:<10} {:<24} {:<24} {:<24}'.format('Class', 'Precision', 'Recall', 'F1'))
for i in range(len(class_list)):
    tp[i] = confusion[i][i]
    fp[i] = col_sum[i] - tp[i]
    fn[i] = row_sum[i] - tp[i]
    # tn[i] = total_lines - tp[i]
    if tp[i] == 0:
        pre[i] = 0
        rec[i] = 0
        f1[i] = 0
    else:
        pre[i] = tp[i] / (tp[i] + fp[i])
        rec[i] = tp[i] / (tp[i] + fn[i])
        f1[i] = (2 * pre[i] * rec[i]) / (pre[i] + rec[i])

    print('{:<10} {:<24} {:<24} {:<24}'.format(class_list[i], pre[i], rec[i], f1[i]))

print()
f1_avg = sum(f1) / len(class_list)
print("F1 avg. (macro):", f1_avg)

print()
print('sklearn: confusion_matrix')
print(metrics.confusion_matrix(test_target, all_predictions))
print()
print('sklearn: classification_report')
print(metrics.classification_report(test_target, all_predictions, target_names=class_list))