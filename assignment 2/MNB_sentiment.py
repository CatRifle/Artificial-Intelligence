import pandas as pd
import csv
import numpy as np
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import sys

# receive files
f_train, f_test = sys.argv[1], sys.argv[2]

# read files
g_train = pd.read_csv(f_train, header=None, sep='\t')
g_test = pd.read_csv(f_test, header=None,sep='\t')

# receive sentences
sen_train, coord_y_train = np.array(g_train[1]), np.array(g_train[2])
id_test, sen_test = np.array(g_test[0]), np.array(g_test[1])

# modify sentences
def modify_sentence(sentences):
    # specified redundant characters
    junk_url = re.compile(r'http[s]?://(?:[0-9]|[a-zA-Z]|[!*\(\),]|[$-_@.&+]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    junk_char = re.compile(r'[^#@_$%\s\w\d]')
    expect_sentence = []
    for line in sentences:
        # delete url
        de_url = re.sub(junk_url, ' ', line)
        # remove illegal char
        de_char = re.sub(junk_char, '', de_url)
        # connect words
        expect_sentence.append(de_char)
    return expect_sentence


# get modified sentences
modified_train, modified_test = np.array(modify_sentence(sen_train)), np.array(modify_sentence(sen_test))

# create training model
Vcount = CountVectorizer(lowercase=False, token_pattern='[#@_$%\w\d]{2,}')
X_train = Vcount.fit_transform(modified_train)
X_test = Vcount.transform(modified_test)


# train the MNB model
classifier = MultinomialNB()
model = classifier.fit(X_train, coord_y_train)
pred_y = model.predict(X_test)
length = len(sen_test)

# write down data
for j in range(length):
    print(id_test[j], pred_y[j])
