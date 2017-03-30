 # usage: python time_series_analyze.py interval
 # e.g. python time_series_analyze.py 9 
 # will run over all graph file w/ the name, e.g., 9_digraph_2013-07-24_2013-09-29.gexf
 
import networkx as nx
import pickle
import sys
import os
import operator
import pdb
import nltk
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import liwc.categories
import concurrent
from concurrent.futures import ProcessPoolExecutor
from multiprocessing.pool import ThreadPool as Pool


labels = ["first_person","second_person","third_person","posemo","negemo","cognitive","sensory","time","past","present","future","work","leisure","swear","social","family","friend","humans","anx","anger","sad","body","health","sexual","space","time","achieve","home","money","relig","Affect","cause","Quant","Numb","inhib","ingest","motion","nonfl","filler","number_classified_words","number_words"]
    
ListOfDicts=[]


def order(frame,var):
    varlist =[w for w in frame.columns if w not in var]
    frame = frame[var+varlist]
    return frame 

def get_graph_measures(g):
        retdic = dict()

        u = g.to_undirected()
        ccs = nx.weakly_connected_components(g)
        ccs = list(ccs)
        #pdb.set_trace()
        max_ccsl = max([len(x) for x in ccs])
        max_cc = [x for x in ccs if len(x) == max_ccsl][0]
        c = nx.core_number(g)
        max_subgraph = g.subgraph(max_cc).to_undirected()
        centrality = list(nx.closeness_centrality(g).values())
        max_cent = max(centrality)

        #pdb.set_trace()
        return {'ave. shortest path': nx.average_shortest_path_length(max_subgraph), \
                'cluster coefficient': nx.average_clustering(u), \
                'lcc': max_ccsl, \
                'ncc': len(ccs), \
                'triangles': np.mean(nx.triangles(u).values()), \
                'degree': np.mean(nx.average_neighbor_degree(g).values()), \
                'core': np.mean(list(nx.core_number(g).values())), \
                'diameter': nx.diameter(max_subgraph),
                'centrality': np.mean(centrality),
                'centralization': np.mean([max_cent - x for x in centrality])/len(centrality)}

def getLIWCDictForText (text):
    global labels

    d = dict()
    print "getting",len(text)
    vals = liwc.categories.classify(text)
    for i in range(0,len(vals)):
        d[labels[i]] = 100 * vals[i]/float(vals[40])
    # d[labels[40]] = float(vals[40])
    print "got"
    return d

def getLIWC (g):
    print 'getting'
    postsText = " ".join([g.node[x]['text'] for x in g])
    commentsText = " ".join([g.edge[x][y]['text'] for x,y in g.edges()])
    print postsText
    return (getLIWCDictForText(postsText), getLIWCDictForText(commentsText))

def drawMe (listOfDicts, fileName,window):
    df = pd.DataFrame(listOfDicts)

    dp = df.plot(subplots=True, figsize=(6,25), fontsize=6, yticks= (-0.06, -0.03, 0.00, 0.03, 0.06))
	
    plt.savefig(window + "-" + fileName + '-measures.pdf')

    plt.clf()
    file('%s-graph-%s.html' % (window,fileName),'w').write(df.to_html())
    file('%s-graph-%s.csv' % (window,fileName),'w').write(df.to_csv())

def tryMultiThread(file):
    print "inside multi"
    D={}
    if not file.startswith("%s_di" % sys.argv[1]):
        return
    print "Processing %s" % file
    g = nx.read_gexf(file) #HACK for top dir
    print 'read gefx'
    (posts, comments) = getLIWC(g)
    print "Got LIWC"
    listOfLIWCDictsPosts.append (posts)
    listOfLIWCDictsComments.append (comments)
    
    g.remove_edges_from(g.selfloop_edges())
    listOfDicts.append( get_graph_measures(g) )
    print "Got graph measures"

def main():
    count=0
    for filename in os.listdir("."):
        print "reading", count
        count += 1
        D={}
        if not filename.startswith("%s_di" % sys.argv[1]):
            continue
        g = nx.read_gexf(filename) #HACK for top dir
        g.remove_edges_from(g.selfloop_edges())
        D['numNodes/10']=len(g.nodes())/10

        # find elements with highest core number
        sorted_by_core_number = sorted(nx.core_number(g).items(), key=operator.itemgetter(1))
        max_core_number = sorted_by_core_number[-1][1]

        # report on strongly connected components
        size_of_sccs = [len(x) for x in nx.strongly_connected_components(g)]
        #print (filename)
        D['filename']=filename[10:-5]
        
        #print ("max_core_number: %d" % max_core_number)
        D['max_core_number']=max_core_number    

        #print ("nontrivial sccs:")
        #print ([x for x in size_of_sccs if x > 1])
        D['nontrivial sccs'] = ([x for x in size_of_sccs if x > 1])
        D['len NT sccs']  = len(D['nontrivial sccs'])


        g.remove_nodes_from([x for x,y in nx.core_number(g).items() if y == max_core_number])

        sorted_by_core_number = sorted(nx.core_number(g).items(), key=operator.itemgetter(1))
        max_core_number = sorted_by_core_number[-1][1]

        # report on strongly connected components
        size_of_sccs = [len(x) for x in nx.strongly_connected_components(g)]

        #print ("max_core_number: %d" % max_core_number)
        D['NT max_core_number'] = max_core_number
        
        #print ("nontrivial sccs:")
        #print ([x for x in size_of_sccs if x > 1])
        D['NT nontrivial sccs'] = ([x for x in size_of_sccs if x > 1])
        D['len NT nontrivial sccs'] = len(D['NT nontrivial sccs'])

        #print ("")
        ListOfDicts.append(D)
        print "Read"
        #pdb.set_trace()
    df=pd.DataFrame(ListOfDicts)
    df=order(df,['filename', 'max_core_number',  'nontrivial sccs','NT nontrivial sccs','NT max_core_number' ] )
    #matplotlib inline
    dp = df.plot()
    dp.legend(loc='upper left', fontsize=7)

    listOfDicts = []
    listOfLIWCDictsPosts = []
    listOfLIWCDictsComments = []

    # multithreading to speed the processing time 
    print "thread start"
    executor = concurrent.futures.ProcessPoolExecutor(1)
    future = [executor.submit(tryMultiThread, filename) for filename in os.listdir(".")]
    concurrent.futures.wait(future)
    print "thread end"

    drawMe(listOfDicts, "graph", sys.argv[1])
    drawMe(listOfLIWCDictsPosts, "LIWC-posts", sys.argv[1])
    drawMe(listOfLIWCDictsComments, "LIWC-comments", sys.argv[1])

if __name__ == '__main__': 
    main()