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


newname = sys.argv[1]
corpus = gensim.corpora.MmCorpus('generatedFiles/corpora_'+newname+'.mm')
dictionary = gensim.corpora.Dictionary.load('generatedFiles/corporaDictionary_'+newname+'.dict')

pprint(corpus)