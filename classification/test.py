import sns as sns
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
tfidf_vec = TfidfVectorizer()
documents = [
    'this is the bayes document',
    'this is the second second document',
    'and the third one',
    'is this the document'
]
tfidf_matrix = tfidf_vec.fit_transform(documents)
print('每个单词的 tfidf 值:', tfidf_matrix.toarray())

label_dict = {
'Autos & Vehicles' : 1, 'Comedy':2, 'Education':3, 'Entertainment':4, 'Film & Animation':5, 'Gaming':6, 'Howto & Style':7, 'Music':8, 'News & Politics':9, 'Nonprofits & Activism':10, 'Pets & Animals':11, 'Science & Technology':12, 'Sports':13, 'Travel & Events':14
}

f = open('train.txt', 'r')
train = f.readlines()
f.close()
label_list = []
content = []
punctuations = "!\"%&'()*+,-./:;<=>?[\\]^_`{|}~…"
bad_words = ['http']
trantab = str.maketrans(dict.fromkeys(punctuations, ''))
for line in train:
    pos = line.rfind('\t')
    label = line[pos+1:].strip()
    label_list.append(label_dict[label])
    content_line = line[0:pos].translate(trantab)
    content.append(content_line)
train_tf = TfidfVectorizer(max_df=0.5)
train_features = train_tf.fit_transform(content)


from sklearn.naive_bayes import MultinomialNB
clf = MultinomialNB(alpha=0.001).fit(train_features, label_list)


f = open('test.txt', 'r')
test = f.readlines()
f.close()
test_label_list = []
test_content = []
for line in test:
    pos = line.find('\t')
    label = line[pos+1:].strip()
    test_label_list.append(label_dict[label])
    content_line = line[0:pos].translate(trantab)
    test_content.append(content_line)
train_vocabulary = train_tf.vocabulary_
test_tf = TfidfVectorizer(max_df=0.5, vocabulary=train_vocabulary)
test_features = test_tf.fit_transform(test_content)

predicted_labels = clf.predict(test_features)
from sklearn import metrics
test_precession = metrics.accuracy_score(test_label_list, predicted_labels)





train_content = train.split('\n')
word_list = nltk.word_tokenize(train)
word_list_tag = nltk.pos_tag(word_list)

f = open('englishST.txt', 'r')
stopwords = f.read()
f.close()
stops = stopwords.split()
tf = TfidfVectorizer(stop_words=stops, max_df=0.5)
features = tf.fit_transform(train_content)

aaa = tf.vocabulary_['furniture']
a_features = features.toarray()
aab = a_features[0][3509]