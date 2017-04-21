import matplotlib.pyplot as plt
import pickle
import collections
import pymongo
import copy
import sys
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
import re
import pdb


def main():

    threads = list()
    posts = list()
    all_posts = list()
    # threads_dict = dict()
    client = MongoClient('mongodb://localhost:27017/')
    db = client.test
    collection = db.posts
    for post in collection.find():
        count = len(re.findall(r'\w+', post['Content']))
        if post['ReplyNum'] == '0':
            if count >= 6500:
                post['Content'] = " "
                threads.append(post)
            else:
                threads.append(post)
                # threads_dict[post['ThreadRef']] = set()
        else:
            #if not any(d['_id'] == post['_id'] for d in threads): # this is to remove self edges but commented since we handle it later
            if count >= 6500:
                post['Content'] = " " # for debugging replace with ' File size too large or spam 
                posts.append(post)
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
