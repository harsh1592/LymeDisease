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
matplotlib.use('Agg')
import matplotlib.pyplot as plt


countDict = []

def getLIWC(g):
    postCount = 0
    commentCount = 0
    for x in g:
        if len(g.node[x]['text'])>0: 
            postCount += 1 
    for x, y in g.edges():
        if len(g.edge[x][y]['text'])>0:
            commentCount += 1
    return (postCount, commentCount)


def getCounts(filepath): 
    file = ntpath.basename(filepath)
    if not file.startswith("%s_di" % sys.argv[1]):
        return
    print "Processing %s" % file
    g = nx.read_gexf('LIWC_DATA/utility_graphs/'+filepath)  # HACK for top dir
    (postCount, commentCount) = getLIWC(g)
    countDict.append({'filename':filepath,'postCount':postCount,'commentCount':commentCount})


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
    fileList = []
    count = 0
    for filename in os.listdir("LIWC_DATA/utility_graphs/"):
        print filename
        if not filename.startswith("%s_di" % sys.argv[1]):
            continue
        fileList.append(filename) 

    # multithreading to speed the processing time
    fileList = sorted(fileList)
    for filename in fileList:
        getCounts(filename)

    csv_columns = ['filename','postCount','commentCount']
    WriteDictToCSV('LIWC_DATA/counts.csv',csv_columns,countDict)