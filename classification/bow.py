import string
import json
import chardet
from collections import defaultdict
from stemming.porter2 import stem
import re


f = open('Tweets.14cat.train', 'rt', encoding="windows-1252")
lines_f = f.readlines()
f.close()
stopwords = open('englishST.txt')
stops = stopwords.read()
stops = stops.split()
tweets_list = []
tweets_list_label = []
punctuations = r"\"%&'()*+,-./;<=>?[\\]^_`{|}~…1234567890"
trantab = str.maketrans(dict.fromkeys(punctuations, ''))
trantab1 = str.maketrans(dict.fromkeys(string.punctuation, ''))
# bad_words = ['http', 'RT', 'twitter']
bad_words = ['http']
emoji_list = [':)', ';-)', ':-)', ';)', ':D', ';D', '=)',
              'lol', 'Lol', 'LOL', '(:', '(-:', ':-D', 'XD',
              'X-D', 'xD', '<3', ';-D', '(;', '(-;', ':-(',
              ':(']

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

tweet_nltk = []
for line in lines_f:
    line = line.strip()
    pos1 = line.find('\t')
    pos2 = line.rfind('\t')
    len_label = len(line) - pos2 - 1  # Get the tweet's label length
    if pos1 > 0:
        label = line[0 - len_label:]  # Get the tweet's label
        tweets_string = line[pos1+1:pos2]  # Get the tweet's content
        # discount = tweets_string.find('% off')  # change '50% OFF' to 'discount'
        # if discount != 0:
        #     tweets_newstr.append('discount')
        tweets_split = tweets_string.split()  # string to list
        tweets_newstr = []  # new a temp list
        for term in tweets_split:
            # term = stem(term)  # Stemming
            if (not any(bad_word in term for bad_word in bad_words)) and (term not in stops):  # delete stopwords, badwords
            # if not any(bad_word in term for bad_word in bad_words):
                tweets_newstr.append(term)
            # term = re.sub(r'(.)\1{2,}', r'\1\1\1', term)  # simplify repeated letters
            if ':' in term and '@' not in term:  # Duplicate colon process
                tweets_newstr.append(':')
            # tweets_newstr.append(term)  # do nothing on text
            if '@' in term:  # Duplicating @surname's @
                pos_1 = term.find('@')
                tweets_newstr.append(term[pos_1 + 1:])
            if '#' in term:  # Duplicate hushtag
                pos_ = term.find('#')
                tweets_newstr.append(term[pos_ + 1:])
            if '$' in term:
                tweets_newstr.append('$')
            # if any(emoji in term for emoji in emoji_list):  # change emoji to 'emoji'
            #     tweets_newstr.append('emoji')
            if 'http' in term:  # change link to 'http'
                tweets_newstr.append('http')
        tweets_string = " ".join(tweets_newstr)
        # tweets_content = tweets_string.strip()  # Do nothing
        # tweets_content = tweets_string.strip().lower()  # Lowercase
        tweets_content = tweets_string.strip().lower().translate(trantab)  # Delete punctuation
        tweets_list.append(tweets_content)
        tweets_label = tweets_content + '\t' + label
        tweets_list_label.append(tweets_label)


# f_temp = open('train.txt', 'w')
# for content in tweets_list_label:
#     f_temp.write(content)
#     f_temp.write('\n')
# f_temp.close()


tweets_dict = {}
unique_id = 1
# tfidf_list = []
term_dict = {}
for line in tweets_list:
    # line = line.translate(trantab)  # delete punctuation
    line = line.split()
    # tfidf_list.append(line)
    for item in line:
        if not tweets_dict.__contains__(item):  # do nothing
        # if not tweets_dict.__contains__(item) and item not in stops:
            # term_dict[item] = 0
            tweets_dict[item] = unique_id
            unique_id += 1

f_temp = open('tweets_dict.txt', 'w')
for content in tweets_dict:
    f_temp.write(content + ' ')
    f_temp.write('\n')
f_temp.close()




feats_train = []
for line in tweets_list_label:
    pos = line.find('\t')
    label = line[pos+1:]
    content = line[0:pos]
    # content = content.translate(trantab)
    content = content.split()
    temp = []
    temp.append(label_dict[label])
    for item in content:
        if item in tweets_dict.keys():
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

ftest = open('Tweets.14cat.test', 'rt', encoding="windows-1252")
lines_test = ftest.readlines()
tweets_test_list_label = []
for line in lines_test:
    line = line.strip()
    pos1 = line.find('\t')
    pos2 = line.rfind('\t')
    len_label = len(line) - pos2 - 1
    if pos1 > 0:
        label = line[0 - len_label:]
        tweets_string = line[pos1 + 1:pos2]
        # discount = tweets_string.find('% off')
        tweets_split = tweets_string.split()
        tweets_newstr = []
        # if discount != 0:
        #     tweets_newstr.append('discount')
        for term in tweets_split: # delete link
            # term = stem(term)
            if (not any(bad_word in term for bad_word in bad_words)) and (term not in stops):
            # if not any(bad_word in term for bad_word in bad_words):
                tweets_newstr.append(term)
            # term = re.sub(r'(.)\1{2,}', r'\1\1\1', term)
            # tweets_newstr.append(term)
            if '@' in term:  # Duplicating @surname's @
                pos_1 = term.find('@')
                tweets_newstr.append(term[pos_1 + 1:])
            if ':' in term and '@' not in term:
                tweets_newstr.append(':')
            # if any(emoji in term for emoji in emoji_list):
            #     tweets_newstr.append('emoji')
            if '#' in term:
                pos_ = term.find('#')
                tweets_newstr.append(term[pos_+1:])
            if '$' in term:
                tweets_newstr.append('$')
            if 'http' in term:
                tweets_newstr.append('http')
        tweets_string = " ".join(tweets_newstr)
        # tweets_content = tweets_string.strip()  # Do nothing
        # tweets_content = tweets_string.strip().lower()  # Lowercase
        tweets_content = tweets_string.strip().lower().translate(trantab)
        tweets_label = tweets_content + '\t' + label
        tweets_test_list_label.append(tweets_label)

# f_temp = open('test.txt', 'w')
# for content in tweets_test_list_label:
#     f_temp.write(content)
#     f_temp.write('\n')
# f_temp.close()

feats_test = []
for line in tweets_test_list_label:
    pos = line.find('\t')
    label = line[pos+1:]
    # content = line[0:pos].translate(trantab).split()
    content = line[0:pos].split()
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
