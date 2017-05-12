import time
import networkx as nx
import pickle
import sys
import os
import operator
import pdb
import nltk
import ntpath
import pandas as pd
import numpy as np
import matplotlib
import csv
import sys
import json
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import spacy
nlp = spacy.load('en')

nlp.vocab[u'lyme'].is_stop = True
nlp.vocab[u'Borrelia'].is_stop = True

year = []
def getLocation(g,window):
    post_location = []
    comment_location = []
    for x in g:
        doc5 = nlp(g.node[x]['text'])
        for ent in doc5.ents:
            if ent.label_=="GPE":         
                year.append({'year':window,'post_location':str(ent), 'comment_location':''})           
                    
    for x, y in g.edges():
        doc5 = nlp(g.edge[x][y]['text'])
        for ent in doc5.ents:
            if ent.label_=="GPE" or ent.label_=="LOC":
                year.append({'year':window,'post_location':'', 'comment_location':str(ent)})   

def WriteDictToCSV(csv_file,csv_columns,dict_data):
    try:
        with open(csv_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in dict_data:
                writer.writerow(data)
    except IOError as (errno, strerror):
        print("I/O error({0}): {1}".format(errno, strerror))    
    return 

if __name__ == '__main__':
    for filename in os.listdir("LIWC_DATA/utility_graphs8/"):
        if not filename.startswith("%s_di" % sys.argv[1]):
            continue
        print filename
        g = nx.read_gexf("LIWC_DATA/utility_graphs8/"+filename) 
        file = str(ntpath.basename(filename)).split('.')[0]
        windowyear = file[len(file)-21:len(file)-11]
        getLocation(g,windowyear)
    with open('LIWC_DATA/LOCATION_FILES/onlyLocation.txt', 'w') as outfile:
        json.dump(year, outfile)

        
        