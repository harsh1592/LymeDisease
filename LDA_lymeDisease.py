# -*- coding: utf-8 -*-
#LDA_lymeDisease.py postIDAndContent.csv col_number num_topics num_passes

import csv, sys
import random
import gensim
import string
import nltk
import logging
import math
import time
import numpy as np
import matplotlib.pyplot as plt
from nltk import word_tokenize          
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
from pprint import pprint  
from nltk.corpus import stopwords
from collections import defaultdict
#logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


filename = sys.argv[1]
data = filename.split("/")
newname = data[1].split(".")[0]

#columnNumber = int(input('Text column number:'))
columnNumber = 0
# Globals
grid = {}
stemmer = PorterStemmer()
stop = set(stopwords.words('english'))
add_stop = set('br/ I ... -- n\'t \'s'.split())
postList = []
parameter_list=[5, 10, 15]

#parse the file into a list
def readFile(filename):
    f = open(filename, 'rt', encoding='utf8')
    try:
        reader = csv.reader(f)
        for row in reader:
            if len(row) > 0:
                postList.append(row[columnNumber])
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
def printTopics(ldamodel,parameter_value):
    topics_brief = ldamodel.show_topics(num_topics=parameter_value, num_words=15, log=False, formatted=False)
    print('Printing Topics...\n\n')
    iter = 0
    for topic in topics_brief:
        print ("%d: %s" % (iter, " ".join([x for x,y in topic[1]])))
        iter += 1

#save text to file
def writeToFile(texts):
    thefile = open('generatedFiles/frequentWords.txt', 'w')
    for text in texts:    
        thefile.write(" ".join(text)+"\n")

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

        # remove words that appear only once
        frequency = defaultdict(int)
        for text in texts:
            for token in text:
                frequency[token] += 1
        texts = [[token for token in text if frequency[token] > 1] for text in texts]        
        writeToFile(texts)

        dictionary = corpora.Dictionary(texts)
        dictionary.save('generatedFiles/corporaDictionary_'+newname+'.dict')
        print('new dictionary saved') 
        corpus = [dictionary.doc2bow(text) for text in texts]
        corpora.MmCorpus.serialize('generatedFiles/corpora_'+newname+'.mm', corpus)
        print('new corpora stored')
    finally:
        cp = random.sample(list(corpus),100000)
        #cp=corpus
        # split into 70% training and 20% test sets
        p = int(len(cp) * .7)
        cp_train = cp[0:p]
        cp_test = cp[p:]
        number_of_words = sum(cnt for document in cp_test for _, cnt in document)
        for parameter_value in parameter_list:
            __getLDA__(cp_train,cp_test,dictionary,parameter_value,number_of_words)
        
#perform LDA
def __getLDA__(cp_train,cp_test,dictionary,parameter_value,number_of_words):
    # print "starting pass for num_topic = %d" % num_topics_value
    print("starting pass for parameter_value = %.3f" % parameter_value)
    start_time = time.time()

    ldamodel = models.LdaMulticore(corpus=cp_train, id2word=dictionary, num_topics=parameter_value,chunksize=3000,
                                    passes=2,  eta=None, workers=3)
    printTopics(ldamodel,parameter_value)
    # show elapsed time for model
    elapsed = time.time() - start_time
    print("Elapsed time: %s" % elapsed)

    perplex = ldamodel.bound(cp_test)
    #print("Perplexity: %s" % perplex)
    #grid[parameter_value].append(perplex)

    per_word_perplex = np.exp2(-perplex / number_of_words)
    print("Per-word Perplexity: %s" % per_word_perplex)
    grid[parameter_value] = per_word_perplex
    

__main__()
print(grid)
with open('LDA_perplexity_'+newname+"_.csv", 'w') as csv_file:
    writer = csv.writer(csv_file)
    for key, value in grid.items():
       writer.writerow([key, value])

#pyplot.subplot(2,1,1)
yaxis = []
for key, value in grid.items():
    yaxis.append(grid[key])
plt.plot(parameter_list, yaxis, color='blue', lw=2)
plt.show()
