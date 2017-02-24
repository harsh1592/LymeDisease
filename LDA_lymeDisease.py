# -*- coding: utf-8 -*-

import csv
import random
import gensim
import string
import nltk
from nltk import word_tokenize          
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
from pprint import pprint  
from nltk.corpus import stopwords

stemmer = PorterStemmer()
stop = set(stopwords.words('english'))
add_stop = set('br/ I ... -- n\'t \'s'.split())

def stem(tokens,stemmer):
    stemmed = []
    for item in tokens:
        if not item in stop and item not in add_stop and not string.punctuation in item:
            stemmed.append(stemmer.stem(item))
    return stemmed
    
def tokenize(text):
    tokens = nltk.word_tokenize(text)
    tokens = [i for i in tokens if i not in string.punctuation]
    stems = stem(tokens, stemmer)
    return stems

postList = []
f = open('D:\Capstone\CSV Files from Database\PostLevel\HLBatch4WithBinariesNoUselessColumns.csv', 'rt')

try:
    reader = csv.reader(f)
    for row in reader:
        postList.append(row[9])
finally:
    f.close()

texts = [text.lower() for text in postList]
texts = [tokenize(text) for text in postList]

dictionary = corpora.Dictionary(texts)
corpus = [dictionary.doc2bow(text) for text in texts]
ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=20, id2word = dictionary, passes=50)
topics_brief = ldamodel.show_topics(num_topics=20, num_words=15, log=False, formatted=False)
iter = 0
for topic in topics_brief:
    print ("%d: %s" % (iter, " ".join([x for x,y in topic[1]])))
    iter += 1

