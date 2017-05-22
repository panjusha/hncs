# Date Created: 22-Mar-2017

import time
from datetime import datetime
import math
from sklearn import metrics

start_time = time.time()
print(datetime.now())
print()

# Naive Bayes train

class_list = ['automobile', 'business', 'editorial', 'education', 'jokes', 'lifestyle', 'movies', 'sports',
              'technology', 'world']

TRAIN_FILE_PATTERN = 'cnn/data/train/{}.txt'
TEST_FILE_PATTERN = 'cnn/data/test/{}.txt'

token_list = {}
token_given_class = {}
total_tokens = 0
num_cls_tokens = {}
prior = {}

class_doc = {}
total_doc = 0

for cls in class_list:
    print("Training", cls)
    with open(TRAIN_FILE_PATTERN.format(cls), mode='r', encoding='utf-8') as file:
        lines = file.readlines()
        tokens = []
        num_tokens = 0
        given_cls = {}
        for line in lines:
            if line:
                t = line.strip().split()
                for token in t:
                    if token:
                        token_list[token] = token_list.get(token, 0) + 1
                        given_cls[token] = given_cls.get(token, 0) + 1
                        num_tokens += 1
        total_tokens += num_tokens
        num_cls_tokens[cls] = num_tokens
        token_given_class[cls] = given_cls
        class_doc[cls] = len(lines)
        total_doc += len(lines)

# calc prior
for cls in class_list:
    prior[cls] = math.log(class_doc[cls] / total_doc)

# calc conditional prob with add 1 smoothing
log_prob_token_given_class = {}
v = len(token_list)
for cls in class_list:
    given_cls = token_given_class[cls]
    c_tokens = num_cls_tokens[cls]
    log_prob = {}
    for token in token_list:
        log_prob[token] = math.log((given_cls.get(token, 0) + 1) / (c_tokens + v))
    log_prob_token_given_class[cls] = log_prob

print(datetime.now())
print("Train time: %s seconds" % (time.time() - start_time))
print()
print("Vocabulary size: ", v)
print()

# test
start_time = time.time()
total_lines = 0
correct_lines = 0
oov = 0
tot = 0


y_test = []
all_predictions = []
confusion = [[0 for x in range(len(class_list))] for y in range(len(class_list))]

for actual_class in range(len(class_list)):
    cls = class_list[actual_class]
    print("Testing", cls)
    with open(TEST_FILE_PATTERN.format(cls), mode='r', encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            prob_line = []
            if line:
                total_lines += 1
                t = line.strip().split()
                predict_class = 0
                predict_prob = float('-infinity')
                for i in range(len(class_list)):
                    log_prob = prior[class_list[i]]
                    log_prob_token = log_prob_token_given_class[class_list[i]]
                    for token in t:
                        if token not in token_list:
                            oov += 1
                        tot += 1
                        log_prob += log_prob_token.get(token, 0)
                    if predict_prob < log_prob:
                        predict_prob = log_prob
                        predict_class = i
                confusion[actual_class][predict_class] += 1
                if actual_class == predict_class:
                    correct_lines += 1
                y_test.append(actual_class)
                all_predictions.append(predict_class)


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
print(metrics.confusion_matrix(y_test, all_predictions))
print()
print('sklearn: classification_report')
print(metrics.classification_report(y_test, all_predictions, target_names=class_list))