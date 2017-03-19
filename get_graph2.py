# python test_graph_from_scratch.py labels_users.csv menstions_all.csv
#
import matplotlib.pyplot as plt
import pickle
import collections
import pymongo
import traceback
import copy
import pdb
import sys
import time
import string
import datetime
import networkx as nx
import math
from sklearn import preprocessing
import sklearn
import sklearn.cluster
import nltk
import operator
import numpy as np
from pymongo import MongoClient
from pymongo.cursor import _QUERY_OPTIONS
from pymongo.errors import AutoReconnect
from bson.timestamp import Timestamp
import re

db = MongoClient('localhost',27017).enable

def get_in_node(bi, node):
	return bi.in_edges({node})[0][0]

def collapse_di (poster, comment, commenter):
	global db
	nu_di = nx.MultiDiGraph()
	for x,y in comment.edges():
		#try:
		#	t = nu_di.edge[x][y]['text']
		#except:
		t = ''
		
		
		try:
			poster_y = get_in_node(poster,y)
			commenter_x = get_in_node(commenter,x)
			commenter_text = comment.node[x]['text']
			if len(sys.argv) > 1:
				tokens = nltk.word_tokenize(commenter_text)

				i = 0
				last = -1
				last_user = ""
				while i < len(tokens):
					token = tokens[i]
					if token.find("+") == 0:
						name_part = token[1:]
						while i < len(tokens):
							try:
								reg = "^" + name_part
								regx = re.compile(reg, re.IGNORECASE)
							except:
								i += 1
								break
							users = db.users.find({"name": regx})
							users = list(users)
							#pdb.set_trace()
							if len(users) == 0: 
								i = i + 1
								if last > -1:
									nu_di.add_edge(commenter_x, last_user['uid'])
									print ("added ambiguous edge: " + commenter_x + ", " + last_user['uid'] + " (" + last_user['name'].encode('ascii', 'ignore') + ")")
								else:
									print "Cannot find: " + name_part.encode('ascii', 'ignore')
								break
							elif len(users) == 1:
								user = users[0]
								nu_di.add_edge(commenter_x, user['uid'])
								i = i + 1
								#print ("Found " + user["name"])
								print ("added edge: " + commenter_x + ", " + user['uid'] + " (" + user['name'].encode('ascii', 'ignore') + ")")
								break
							else:
								i += 1
								#print ("Yo")
								if i < len(tokens) and tokens[i].find("+") != 0:
									name_part += " " + tokens[i]
									last = len(users)
									last_user = users[0]
								else:
									break
					else:
						i += 1

			try:
				nu_di.add_edge(commenter_x, poster_y, text = commenter_text)
				#print comment.node[x]['text']
				if not 'text' in nu_di.node[poster_y]:
					nu_di.node[poster_y]['text'] = set()
				nu_di.node[poster_y]['text'].add(comment.node[y]['text']) 
			except Exception as e:
				print "EXCEPTION"
				print e
				#pdb.set_trace()
				nu_di.add_edge(commenter_x, poster_y, text = t)
				if not 'text' in nu_di.node[poster_y]:
					nu_di.node[poster_y]['text'] = set()
				nu_di.node[poster_y]['text'].add(comment.node[y]['text']) 

				#print "boogah"
		except Exception as e:
			print e
			traceback.print_exc()
			#pdb.set_trace()
			pass
	for n in nu_di:
		t = ''
		if 'text' in nu_di.node[n]:
			for x in nu_di.node[n]['text']:
				t += " " + x
		nu_di.node[n]['text'] = t
	# now collapse
	nd = nx.DiGraph()
	for x,y,z in nu_di.edges_iter(data=True):
		if not nd.has_edge(x,y):
			nd.add_edge(x,y, text = list())
		nd.edge[x][y]["text"].append(z["text"])
	for x,y,z in nd.edges_iter(data=True):
		z["width"] = len(z["text"])
		z["text"] = " ".join(z["text"])
	return nd

def clique_me (g, s):
	ns = set()
	for x in s:
		for y in ns:
			g.add_edge(x,y)
		ns.add(x)
	return g

def collapse_un (poster, comment, commenter):

	nu_un = nx.Graph()
	legal_nodes = set(comment.nodes()) - set(commenter.nodes())
	for y in legal_nodes:
		neighbs = set()
		neighbs.add(y)
		for x,z in comment.in_edges(y):
			neighbs.add(x)
		nu_un = clique_me(nu_un, neighbs)
	return nu_un

def read_date(date):
	try:
		output = datetime.datetime.strptime(date, "%b %d, %Y")
	except ValueError as e:
		try:
			output = datetime.datetime.strptime(date, "%d %b %Y")
		except ValueError as e:
			try:
				output = datetime.datetime.strptime(date, "%b %d, %Y, %I:%M:%S %p")
			except ValueError as e:
				try:
					output = datetime.datetime.strptime(date, "%d %b %Y, %H:%M:%S")
				except ValueError as e:
					try:
						output = datetime.datetime.strptime(date, "%Y-%m-%d")
					except ValueError as e:
						print "Bad date: %s" % date
						output = datetime.datetime.strptime("Jul 1, 1969", "%b %d, %Y")
	except TypeError as e:
		print "No date" 
		output = datetime.datetime.strptime("Jul 1, 1969", "%b %d, %Y")

	return output







def main ():

	f = open ("posts_list.pkl")
	posts = pickle.load(f)
	f.close()

	f = open ("comments_list.pkl")
	comments = pickle.load(f)
	f.close() 
	
	poster_graph = nx.DiGraph()
	posts_graph = nx.DiGraph()
	commenter_graph = nx.DiGraph()

    # here we construct three graph.
    # posts_graph is a bipartite graph matching comments to posts
    # 
	for post in posts:
		#pdb.set_trace()
		poster_graph.add_edge(post['userId'], post['url'])
		poster_graph.node[post['url']]['date'] = read_date(post['date'])
		posts_graph.add_node(post['url'])
		posts_graph.node[post['url']]['text'] = post["content"]
		#pdb.set_trac
		posts_graph.node[post['url']]['date'] = poster_graph.node[post['url']]['date']
 	for comment in comments:
		commenter_graph.add_edge(comment['userId'],comment['_id'])
		posts_graph.add_edge(comment['_id'], comment['postUrl'])
		posts_graph.node[comment['_id']]['text'] = comment['comment']
		posts_graph.node[comment['_id']]['date'] = read_date(comment["date"])

	print ("created utility graphs")
	f = open("utility_graph_list.pkl", "w")
	pickle.dump([poster_graph,posts_graph,commenter_graph], f)
	f.close()
	print ("dumped utility graphs")
	comments = posts_graph.edges()
	#pdb.set_trace()
	comments = [(posts_graph.node[x]["date"], x, y, posts_graph.node[x]['text'], posts_graph.node[y]['text']) for x,y in comments]
	comments = sorted(comments, key=operator.itemgetter(0))

	min_date = comments[0][0] # lower bound of interval
	max_date = comments[-1][0] # upper bound of interval
	end_date = comments[-1][0] # stopping condition
	span = len(comments)
	#pdb.set_trace()
	diff = max_date - min_date
	#diff = datetime.timedelta(days=14)
	max_date = min_date + diff
	print "max: %s, min: %s, diff: %d" % (datetime.datetime.strftime(max_date, "%Y-%m-%d"),datetime.datetime.strftime(min_date, "%Y-%m-%d"), diff.days/7)
	while diff.days/7 >= 2:
		
		lower = 0
		upper = len(comments)-1
		while comments[upper][0] > max_date:
			upper -= 1
		upper += 1
		min_date = comments[lower][0]
		
		
		while max_date <= end_date:
			#pdb.set_trace()

			nu_comments = [(u,v) for k,u,v, t, w in comments[lower:upper]]
			nu_un = nx.DiGraph()
			nu_un.add_edges_from(nu_comments)
			for k,u,v,t,w in comments[lower:upper]:
				nu_un.node[u]["text"]  = t
				nu_un.node[v]["text"]  = w
				nu_un.node[u]["type"] = "comment"
				nu_un.node[v]["type"] = "post"
				#print t


			d = collapse_di(poster_graph,nu_un,commenter_graph)
			#pdb.set_trace()
			nx.write_gexf(d, "graphs/%d_digraph_%s_%s.gexf" % (diff.days/7, datetime.datetime.strftime(min_date, "%Y-%m-%d"), datetime.datetime.strftime(max_date, "%Y-%m-%d")))
			
			f = open("graphs/%d_posts_%s_%s.pkl" % (diff.days/7, datetime.datetime.strftime(min_date, "%Y-%m-%d"), datetime.datetime.strftime(max_date, "%Y-%m-%d")), "w")
			pickle.dump(nu_un,f)
			f.close()
			#pdb.set_trace()


			g = collapse_un(poster_graph,nu_un,commenter_graph)
			nx.write_gexf(g, "graphs/%d_graph_%s_%s.gexf" % (diff.days/7, datetime.datetime.strftime(min_date, "%Y-%m-%d"), datetime.datetime.strftime(max_date, "%Y-%m-%d")))
			min_date = min_date + datetime.timedelta(weeks=2)
			max_date = max_date + datetime.timedelta(weeks=2)
			while lower < len(comments) and comments[lower][0] < min_date:
				lower += 1
			while upper < len(comments) and comments[upper][0] <= max_date:
				upper += 1

		diff /= 2
		min_date = comments[0][0]
		max_date = min_date + diff
		

	
	
if __name__ == '__main__': 
	main()
