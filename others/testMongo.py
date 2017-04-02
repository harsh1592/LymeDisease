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
from collections import defaultdict

def main ():
	threads = list()
	posts = list()
	threads_dict = dict()
	client = MongoClient('mongodb://localhost:27017/')
	db = client.test
	collection = db.posts
	for post in collection.find():
		if post['ReplyNum'] == 0:			
			threads.append(post)
			threads_dict[post['ThreadRef']] = set()	
	
	for post in collection.find():
		if post['ReplyNum'] != 0:	
			posts.append(post)
			threads_dict[post['ThreadRef']].add(post['PosterId'])

if __name__ == '__main__': 
	main()