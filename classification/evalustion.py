import string
from collections import defaultdict

# 制作qrels, 也就是feats.test里面的内容
# ID：class，feats.test和pred.out的ID同位置相同
f_test = open('feats.test', 'r')
line_test = f_test.readlines()
f_test.close()
tweet_id = 1
feats_test = []
for line in line_test:
    line = line.split()
    temp = []
    temp.append(int(line[0]))
    temp.append(tweet_id)
    feats_test.append(temp)
    tweet_id += 1

# 制作retrieved，也就是pred.out里面的内容
# 格式和feats_test相同
f_pred = open('pred.out', 'r')
line_pred = f_pred.readlines()
f_pred.close()
tweet_id = 1
pred = []
for line in line_pred:
    line = line.split()
    temp = []
    temp.append(int(line[0]))
    temp.append(tweet_id)
    pred.append(temp)
    tweet_id += 1

# tweet_test = sorted(feats_test, key=lambda x: x[0])
# tweet_pred = sorted(pred, key=lambda x:x[0])

tweet_test = {
    1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: [], 11: [], 12: [], 13: [], 14: []
}
tweet_pred = {
    1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: [], 11: [], 12: [], 13: [], 14: []
}
for item in feats_test:
    tweet_test[item[0]].append(item[1])
for item in pred:
    tweet_pred[item[0]].append(item[1])
tp_all = 0
f1_sum = 0
p_all = []
r_all = []
f_all = []
for i in range(1, 15):
    tp = set(tweet_test[i]).intersection(set(tweet_pred[i]))
    fn = set(tweet_test[i]).difference(set(tweet_pred[i]))
    fp = set(tweet_pred[i]).difference(set(tweet_test[i]))
    tp_all += len(tp)
    p = len(tp) / (len(tp) + len(fp))
    p_all.append(round(p, 3))
    r = len(tp) / (len(tp) + len(fn))
    r_all.append(round(r, 3))
    f = 2 * p * r / (p + r)
    f_all.append(round(f, 3))
    f1_sum += f

f_eval = open('Eval0.txt', 'w')
accu = tp_all/(tweet_id - 1)
f_eval.write('Accuracy = ' + str(round(accu, 3)) + '\n')
macrof1 = f1_sum/14
f_eval.write('Macro-F1 = ' + str(round(macrof1, 3)) + '\n')
f_eval.write('Results per class:\n')
for i in range(1, 15):
    f_eval.write(str(i) + ': P=' + str(p_all[i-1]) + ' R=' + str(r_all[i-1]) + ' F=' + str(f_all[i-1]) + '\n')
f_eval.close()
