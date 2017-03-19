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
	posts = list()
	comments = list()
	posts_dict = dict()
	db_meteor = MongoClient('localhost',27017).enable
	for post in db_meteor.Post.find():
		posts.append(post)
		posts_dict[post['url']] = set()	
	for comment in db_meteor.Comment.find():
		comments.append(comment)
		posts_dict[comment['postUrl']].add(comment['userId'])
	f = open("posts_list.pkl", "w")
	pickle.dump(posts, f)
	f.close()
	f = open("comments_list.pkl", "w")
	pickle.dump(comments, f)
	f.close()
	f = open("posts_dict.pkl", "w")
	pickle.dump(posts_dict, f)
	f.close()

	u = nx.Graph()
	d = nx.DiGraph()

	for post in posts:
		grp = set()
		done = set()
		grp.add(post['userId'])
		poster = post['userId']
		for comment in posts_dict[post['url']] - { poster }:
			d.add_edge(comment, poster)
			for x in grp:
				u.add_edge(comment, x)
			grp.add(comment)

        f = open("digraph.pkl", "w")
        pickle.dump(d, f)
        f.close()
        f = open("graph.pkl", "w")
        pickle.dump(u, f)
        f.close()

	nx.write_gexf(d, "digraph.gexf")
	nx.write_gexf(u, "graph.gexf")

		

		
	
if __name__ == '__main__': 
	main()
