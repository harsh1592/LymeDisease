import matplotlib.pyplot as plt
import pickle
import collections
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
from bson.timestamp import Timestamp
import re


def get_in_node(bi, node):
    return bi.in_edges({node})[0][0]


def collapse_di(poster, comment, commenter):
    global db
    nu_di = nx.MultiDiGraph()
    for x, y in comment.edges():
        t = ''

        try:
            poster_y = get_in_node(poster, y)
            commenter_x = get_in_node(commenter, x)
            commenter_text = comment.node[x]['text']

            try:
                nu_di.add_edge(commenter_x, poster_y, text=commenter_text)
                if not 'text' in nu_di.node[poster_y]:
                    nu_di.node[poster_y]['text'] = set()
                nu_di.node[poster_y]['text'].add(comment.node[y]['text'])
            except Exception as e:
                print "EXCEPTION"
                # print e
                nu_di.add_edge(commenter_x, poster_y, text=t)
                if not 'text' in nu_di.node[poster_y]:
                    nu_di.node[poster_y]['text'] = set()
                nu_di.node[poster_y]['text'].add(comment.node[y]['text'])
        except Exception as e:
            print "exception"
            # print e
            traceback.print_exc()
            pass
    for n in nu_di:
        t = ''
        if 'text' in nu_di.node[n]:
            for x in nu_di.node[n]['text']:
                t += " " + x
        nu_di.node[n]['text'] = t

    # now collapse
    nd = nx.DiGraph()
    for x, y, z in nu_di.edges_iter(data=True):
        if not nd.has_edge(x, y):
            nd.add_edge(x, y, text=list())
        nd.edge[x][y]["text"].append(z["text"])

    for x, z in nu_di.nodes_iter(data=True):
        if not nd.has_node(x):
            print('not present')
            nd.add_node(x, text=str())
        nd.add_node(x, text=str())
        nd.node[x]['text'] = z['text']

    for x, y, z in nd.edges_iter(data=True):
        z["width"] = len(z["text"])
        z["text"] = " ".join(z["text"])

    return nd


def clique_me(g, s):
    ns = set()
    for x in s:
        for y in ns:
            g.add_edge(x, y)
        ns.add(x)
    return g


def collapse_un(poster, comment, commenter):

    nu_un = nx.Graph()
    legal_nodes = set(comment.nodes()) - set(commenter.nodes())
    for y in legal_nodes:
        neighbs = set()
        neighbs.add(y)
        for x, z in comment.in_edges(y):
            neighbs.add(x)
        nu_un = clique_me(nu_un, neighbs)
    return nu_un


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

    f = open("LIWC_DATA/threads_list.pkl")
    posts = pickle.load(f)
    f.close()

    f = open("LIWC_DATA/posts_list.pkl")
    comments = pickle.load(f)
    f.close()

    poster_graph = nx.DiGraph()
    posts_graph = nx.DiGraph()
    commenter_graph = nx.DiGraph()

# here we construct three graph.
# posts_graph is a bipartite graph matching comments to posts

    for post in posts:
        poster_graph.add_edge(post['PosterID'], post['ThreadRef'])
        poster_graph.node[post['ThreadRef']][
            'PostedOn'] = read_date(post['PostedOn'])
        posts_graph.add_node(post['ThreadRef'])
        posts_graph.node[post['ThreadRef']]['text'] = post["Content"]
        posts_graph.node[post['ThreadRef']][
            'PostedOn'] = poster_graph.node[post['ThreadRef']]['PostedOn']
    for comment in comments:
        commenter_graph.add_edge(comment['PosterID'], comment['_id'])
        posts_graph.add_edge(comment['_id'], comment['ThreadRef'])
        posts_graph.node[comment['_id']]['text'] = comment['Content']
        posts_graph.node[comment['_id']][
            'PostedOn'] = read_date(comment["PostedOn"])

    print ("created utility graphs")
    f = open("LIWC_DATA/utility_graphs8/utility_graph_list.pkl", "w")
    pickle.dump([poster_graph, posts_graph, commenter_graph], f)
    f.close()
    print ("dumped utility graphs")
    comments = posts_graph.edges()
    # pdb.set_trace()
    comments = [(posts_graph.node[x]["PostedOn"], x, y, posts_graph.node[x][
                 'text'], posts_graph.node[y]['text']) for x, y in comments]

    # pdb.set_trace()
    comments = sorted(comments, key=operator.itemgetter(0))

    min_date = comments[0][0]  # lower bound of interval
    max_date = comments[-1][0]  # upper bound of interval
    end_date = comments[-1][0]  # stopping condition
    span = len(comments)
    # pdb.set_trace()
    diff = max_date - min_date
    max_date = min_date + diff
    print "max: %s, min: %s, diff: %d" % (datetime.datetime.strftime(max_date, "%Y-%m-%d"), datetime.datetime.strftime(min_date, "%Y-%m-%d"), diff.days / 7)
    while diff.days / 7 >= 2:

        lower = 0
        upper = len(comments) - 1
        while comments[upper][0] > max_date:
            upper -= 1
        upper += 1
        min_date = comments[lower][0]

        while max_date <= end_date:
            # pdb.set_trace()

            nu_comments = [(u, v) for k, u, v, t, w in comments[lower:upper]]
            nu_un = nx.DiGraph()
            nu_un.add_edges_from(nu_comments)
            for k, u, v, t, w in comments[lower:upper]:
                nu_un.node[u]["text"] = t
                nu_un.node[v]["text"] = w

                nu_un.node[u]["type"] = "comment"
                nu_un.node[v]["type"] = "post"
                # print t

            d = collapse_di(poster_graph, nu_un, commenter_graph)

            nx.write_gexf(d, "LIWC_DATA/utility_graphs8/%d_digraph_%s_%s.gexf" % (diff.days / 7,
                                                                                 datetime.datetime.strftime(min_date, "%Y-%m-%d"), datetime.datetime.strftime(max_date, "%Y-%m-%d")))

            f = open("LIWC_DATA/utility_graphs8/%d_posts_%s_%s.pkl" % (diff.days / 7, datetime.datetime.strftime(
                min_date, "%Y-%m-%d"), datetime.datetime.strftime(max_date, "%Y-%m-%d")), "w")
            pickle.dump(nu_un, f)
            f.close()
            # pdb.set_trace()

            g = collapse_un(poster_graph, nu_un, commenter_graph)
            nx.write_gexf(g, "LIWC_DATA/utility_graphs8/%d_graph_%s_%s.gexf" % (diff.days / 7,
                                                                               datetime.datetime.strftime(min_date, "%Y-%m-%d"), datetime.datetime.strftime(max_date, "%Y-%m-%d")))
            min_date = min_date + datetime.timedelta(weeks=8)
            max_date = max_date + datetime.timedelta(weeks=8)
            while lower < len(comments) and comments[lower][0] < min_date:
                lower += 1
            while upper < len(comments) and comments[upper][0] <= max_date:
                upper += 1

        diff /= 16
        #diff /= 2
        min_date = comments[0][0]
        max_date = min_date + diff

if __name__ == '__main__':
    main()
