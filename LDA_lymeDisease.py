# -*- coding: utf-8 -*-
#LDA_lymeDisease.py postIDAndContent.csv col_number num_topics num_passes

import csv, sys
import random
import gensim
import string
import nltk
import logging
import math
import numpy as np
from nltk import word_tokenize          
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
from pprint import pprint  
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
#logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


filename = sys.argv[1]
data = filename.split("\\")
newname = data[1].split(".")[0]

columnNumber = int(input('Text column number:'))

# Globals
stemmer = PorterStemmer()
stop = set(stopwords.words('english'))
add_stop = set('br/ I ... -- n\'t \'s'.split())
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

#print out the topics in the model
def printTopics(ldamodel):
    topics_brief = ldamodel.show_topics(num_topics=num_topics, num_words=15, log=False, formatted=False)
    print('Printing Topics...\n\n')
    iter = 0
    for topic in topics_brief:
        print ("%d: %s" % (iter, " ".join([x for x,y in topic[1]])))
        iter += 1

#main
def __main__():
    try:
        corpus = gensim.corpora.MmCorpus('generatedFiles/corpora_'+newname+'.mm')
        dictionary = gensim.corpora.Dictionary.load('generatedFiles/corporaDictionary_'+newname+'.dict')
        print('Found corpus and dictionary for the input file')   
    except FileNotFoundError:
        print("Corpora or dictionary for the input file not found, creating one...")
        readFile(filename)
        texts = [text.lower() for text in postList]
        texts = [tokenize(text) for text in postList]
        dictionary = corpora.Dictionary(texts)
        dictionary.save('generatedFiles/corporaDictionary_'+newname+'.dict')
        print('new dictionary saved') 
        corpus = [dictionary.doc2bow(text) for text in texts]
        corpora.MmCorpus.serialize('generatedFiles/corpora_'+newname+'.mm', corpus)
        print('new corpora stored')
    finally:
        number_of_words = sum(cnt for document in corpus for _, cnt in document)
        parameter_list = range(5, 71, 5)
        for parameter_value in parameter_list:
            __getLDA__(corpus,dictionary,parameter_value,number_of_words)
        
#perform LDA
def __getLDA__(corpus,dictionary,num_topics,number_of_words):
    print('Running LDA on '+str(num_topics)+' topics, with '+str(10)+' run(s)')    
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=num_topics, id2word = dictionary, passes=2)
    #printTopics(ldamodel) 
    perplex = ldamodel.bound(corpus)
    print('Total Perplexity: '+str(perplex))   
    per_word_perplex = np.exp2(-perplex / number_of_words)   
    print('Per Word Perplexity: '+str(per_word_perplex))
    print('\n')

__main__()
