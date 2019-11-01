import string
import json
import chardet
from collections import defaultdict



# f= open('Tweets.14cat.train', mode='rb')
# data=f.read()
# f.close()
# result=chardet.detect(open('Tweets.14cat.train', mode='rb').read())
# print(result)

f = open('Tweets.14cat.train', 'rt', encoding="windows-1252")
lines_f = f.readlines()
f.close()
tweets_list = []
tweets_list_label = []
punctuations = "!\"%&'()*+,-./:;<=>?[\\]^_`{|}~…"
bad_words = ['htt']
trantab = str.maketrans(dict.fromkeys(punctuations, ''))
for line in lines_f:
    line = line.strip()
    pos1 = line.find('\t')
    pos2 = line.rfind('\t')
    len_label = len(line) - pos2 - 1
    if pos1 > 0:
        tweets_string = line[pos1+1:]
        # tweets_label = line[pos1+1:]
        tweets_split = tweets_string.split()
        tweets_newstr = []
        for term in tweets_split: # delete link
            if not any(bad_word in term for bad_word in bad_words):
                tweets_newstr.append(term)
        tweets_string = " ".join(tweets_newstr)
        label = tweets_string[0-len_label:]
        tweets_content = tweets_string[0:0-len_label].strip()
        # tweets_content = tweets_content.translate(trantab)
        tweets_list.append(tweets_content)
        tweets_label = tweets_content + '\t' + label
        tweets_list_label.append(tweets_label)

tweets_dict = {}
unique_id = 1
for line in tweets_list:
    line = line.translate(trantab)
    line = line.split()
    for item in line:
        if not tweets_dict.__contains__(item):
            tweets_dict[item] = unique_id
            unique_id += 1

label_dict = {
'Autos & Vehicles' : 1,
'Comedy':2,
'Education':3,
'Entertainment':4,
'Film & Animation':5,
'Gaming':6,
'Howto & Style':7,
'Music':8,
'News & Politics':9,
'Nonprofits & Activism':10,
'Pets & Animals':11,
'Science & Technology':12,
'Sports':13,
'Travel & Events':14
}
feats_train = []
for line in tweets_list_label:
    pos = line.find('\t')
    label = line[pos+1:]
    content = line[0:pos]
    content = content.translate(trantab)
    content = content.split()
    temp = []
    temp.append(label_dict[label])
    for item in content:
        item_id = tweets_dict[item]
        if item_id not in temp:
            temp.append(item_id)
    temp_part_sorted = sorted(temp[1:])
    temp[1:] = temp_part_sorted
    feats_train.append(temp)

ft_ = open('feats.train', 'w')
for line in feats_train:
    ft_.write(str(line[0]))
    for i in range(1,len(line)):
        ft_.write(' ' + str(line[i]) + ':1')
    ft_.write('\n')
ft_.close()

# for i in range(1, 15):
#     ft_.write(str(i))
#     for value in feats_train[i]:
#         ft_.write(' ' + str(value) + ':1')
#     ft_.write('\n')
# ft_.close()

ftest = open('Tweets.14cat.test', 'rt', encoding="windows-1252")
lines_test = ftest.readlines()
# tweets_test_list = []
tweets_test_list_label = []
for line in lines_test:
    line = line.strip()
    pos1 = line.find('\t')
    pos2 = line.rfind('\t')
    len_label = len(line) - pos2 - 1
    if pos1 > 0:
        tweets_string = line[pos1+1:]
        tweets_split = tweets_string.split()
        tweets_newstr = []
        for term in tweets_split: # delete link
            if not any(bad_word in term for bad_word in bad_words):
                tweets_newstr.append(term)
        tweets_string = " ".join(tweets_newstr)
        label = tweets_string[0 - len_label:]
        tweets_content = tweets_string[0:0 - len_label].strip()
        tweets_label = tweets_content + '\t' + label
        tweets_test_list_label.append(tweets_label)

feats_test = []
for line in tweets_test_list_label:
    pos = line.find('\t')
    label = line[pos+1:]
    content = line[0:pos].translate(trantab).split()
    temp = []
    temp.append(label_dict[label])
    for item in content:
        if item in tweets_dict.keys():
            item_id = tweets_dict[item]
            if item_id not in temp:
                temp.append(item_id)
    temp_part_sorted = sorted(temp[1:])
    temp[1:] = temp_part_sorted
    feats_test.append(temp)

ft_ = open('feats.test', 'w')
for line in feats_test:
    ft_.write(str(line[0]))
    for i in range(1, len(line)):
        ft_.write(' ' + str(line[i]) + ':1')
    ft_.write('\n')
ft_.close()

