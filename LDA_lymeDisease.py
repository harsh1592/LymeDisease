# -*- coding: utf-8 -*-
#LDA_lymeDisease.py postIDAndContent.csv

import csv, sys
import random
import gensim
import string
import nltk
import logging
from nltk import word_tokenize          
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
from pprint import pprint  
from nltk.corpus import stopwords

#logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
stemmer = PorterStemmer()
stop = set(stopwords.words('english'))
add_stop = set('br/ I ... -- n\'t \'s'.split())

filename = sys.argv[1]
columnNumber = int(sys.argv[2])
postList = []

#parse the file into a list
def readFile(filename):
    #f = open(filename, 'rt', encoding='utf8')
    f = open(filename, 'rt')
    try:
        reader = csv.reader(f)
        for row in reader:
            postList.append(row[columnNumber])# row[1] for the file postIDAndContent.csv
    finally:
        print('Reading Complete')
        f.close()

#stem the tokens using porterStemmer    
def stem(tokens,stemmer):
    stemmed = []
    for item in tokens:
        if not item in stop and item not in add_stop:            
            stemmed.append(stemmer.stem(item))
    return stemmed

#tokenize a post    
def tokenize(post):
    tokens = nltk.word_tokenize(post)
    tokens = [i for i in tokens if i not in string.punctuation]
    stems = stem(tokens, stemmer)
    return stems

readFile(filename);
texts = [text.lower() for text in postList]
texts = [tokenize(text) for text in postList]

print('Tokenized text')
dictionary = corpora.Dictionary(texts)
print('saving')
dictionary.save('corporaDictionary.dict')
print('saved')
corpus = [dictionary.doc2bow(text) for text in texts]
ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=15, id2word = dictionary, passes=1)
topics_brief = ldamodel.show_topics(num_topics=15, num_words=15, log=False, formatted=False)
iter = 0
for topic in topics_brief:
    print ("%d: %s" % (iter, " ".join([x for x,y in topic[1]])))
    iter += 1
