# python create_utility_files_mod.py year
#eg, python create_utility_files_mod.py 2006

import matplotlib.pyplot as plt
import pickle
import collections
import pymongo
import copy
import sys
import datetime
import networkx as nx
import math
from sklearn import preprocessing
import sklearn
import sklearn.cluster
import numpy as np
from pymongo import MongoClient
from pymongo.cursor import _QUERY_OPTIONS
from pymongo.errors import AutoReconnect
from bson.timestamp import Timestamp
from collections import defaultdict
import re
import pdb

def read_date(date):
    try:
        output = datetime.datetime.strptime(date, "%Y/%m/%d %H:%M")
    except ValueError as e:
        print("Bad date: %s" % date)
        temp = list(date)
        temp.pop(8)
        temp.insert(9, temp[10])
        temp.pop(13)
        temp.pop(11)
        temp.insert(13, ':')
        temp.insert(15, '0')
        dateTemp = ''.join(temp)
        output = datetime.datetime.strptime(dateTemp, "%Y/%m/%d %H:%M")
    return output

def main():

    threads = list()
    posts = list()
    all_posts = list()
    # threads_dict = dict()
    client = MongoClient('mongodb://localhost:27017/')
    db = client.db
    post_collection = db.posts
    thread_collection = db.threads
    
    year = sys.argv[1]
    board = sys.argv[2]

    b = datetime.datetime.strptime(year+"-01-01", "%Y-%m-%d")
    tSet = set()

    threadDict = defaultdict()
    for thread in thread_collection.find():
        threadDict[thread['ThreadRef']] = thread['Board']

    for post in post_collection.find():
        if threadDict[post['ThreadRef']] == board:
            count = len(re.findall(r'\w+', post['Content']))
            date = read_date(post['PostedOn'])
            if post['ReplyNum'] == '0':
                if date > b:
                    if count >= 6500:
                        post['Content'] = " "
                        tSet.add(post['ThreadRef'])
                        threads.append(post)
                    else:
                        tSet.add(post['ThreadRef'])
                        threads.append(post)
            else:
                if (date > b) & (post['ThreadRef'] in tSet):
                    if count >= 6500:
                        post['Content'] = " " # for debugging replace with ' File size too large or spam 
                        posts.append(post)
                    # if any(d['ThreadRef'] == post['ThreadRef'] for d in threads):
                    else:    
                        posts.append(post)

    f = open("LIWC_DATA/threads_list.pkl", "w")
    pickle.dump(threads, f)
    f.close()

    f = open("LIWC_DATA/posts_list.pkl", "w")
    pickle.dump(posts, f)
    f.close()

if __name__ == '__main__':
    main()
