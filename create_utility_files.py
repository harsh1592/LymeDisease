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

def main ():

	threads = list()
	posts = list()
	threads_dict = dict()
	client = MongoClient('mongodb://localhost:27017/')
	db = client.test
	collection = db.posts

	for post in collection.find():
		if post['ReplyNum'] == '0':
			threads.append(post)
			threads_dict[post['ThreadRef']] = set()	
	
	for post in collection.find():
		posts.append(post)
		threads_dict[post['ThreadRef']].add(post['PosterID'])
	
	f = open("LIWC_DATA/threads_list.pkl", "w")
	pickle.dump(threads, f)
	f.close()
	
	f = open("LIWC_DATA/posts_list.pkl", "w")
	pickle.dump(posts, f)
	f.close()

	f = open("LIWC_DATA/threads_dict.pkl", "w")
	pickle.dump(threads_dict, f)
	f.close()

	# u = nx.Graph()
	# d = nx.DiGraph()

	# for post in threads:
	# 	grp = set()
	# 	done = set()
	# 	grp.add(post['PosterID'])
	# 	poster = post['PosterID']
	# 	for comment in threads_dict[post['ThreadRef']] - { poster }:
	# 		d.add_edge(comment, poster)
	# 		for x in grp:
	# 			u.add_edge(comment, x)
	# 		grp.add(comment)
	# 	f = open("LIWC_DATA/digraph.pkl", "w")
	# 	pickle.dump(d, f)
	# 	f.close()
	# 	f = open("LIWC_DATA/graph.pkl", "w")
	# 	pickle.dump(u, f)
	# 	f.close()
	# nx.write_gexf(d, "digraph.gexf")
	# nx.write_gexf(u, "graph.gexf")

if __name__ == '__main__': 
	main()	
