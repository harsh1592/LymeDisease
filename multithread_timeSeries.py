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
import ntpath
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import liwc.categories
#import concurrent
#from concurrent.futures import ProcessPoolExecutor
#from multiprocessing.pool import ThreadPool as Pool
from multiprocessing import Pool,Process, Manager

# pool_size = 3  # your "parallelness"
# pool = Pool(pool_size)


labels = ["first_person","second_person","third_person","posemo","negemo","cognitive","sensory","time","past","present","future","work","leisure","swear","social","family","friend","humans","anx","anger","sad","body","health","sexual","space","time","achieve","home","money","relig","Affect","cause","Quant","Numb","inhib","ingest","motion","nonfl","filler","number_classified_words","number_words"]
    
ListOfDicts=[]

listOfDicts = []
listOfLIWCDictsPosts = []
listOfLIWCDictsComments = []

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
    vals = liwc.categories.classify(text)
    for i in range(0,len(vals)):
        d[labels[i]] = 100 * vals[i]/float(vals[40])
    # d[labels[40]] = float(vals[40])
    return d

def getLIWC (g):
    postsText = " ".join([g.node[x]['text'] for x in g])
    commentsText = " ".join([g.edge[x][y]['text'] for x,y in g.edges()])
    return (getLIWCDictForText(postsText), getLIWCDictForText(commentsText))

def drawMe (listOfDicts, fileName,window):
    df = pd.DataFrame(listOfDicts)

    dp = df.plot(subplots=True, figsize=(6,25), fontsize=6, yticks= (0.00, 1.00, 2.00, 3.00, 4.00))
	
    plt.savefig('LIWC_DATA/LIWC_OUTPUT/'+ window + "-" + fileName + '-measures.pdf')

    plt.clf()
    file('LIWC_DATA/LIWC_OUTPUT/%s-graph-%s.html' % (window,fileName),'w').write(df.to_html())
    file('LIWC_DATA/LIWC_OUTPUT/%s-graph-%s.csv' % (window,fileName),'w').write(df.to_csv())

def tryMultiThread(filepath,all_d,post_d,comment_d):
    D={}
    file = ntpath.basename(filepath)
    if not file.startswith("%s_di" % sys.argv[1]):
        return
    print "Processing %s" % file
    g = nx.read_gexf(filepath) #HACK for top dir
    (posts, comments) = getLIWC(g)
    print "Got LIWC"
    post_d.append (posts)
    comment_d.append (comments)
    
    g.remove_edges_from(g.selfloop_edges())
    all_d.append( get_graph_measures(g) )
    print 'done'

if __name__ == '__main__':
    pool = Pool(processes=4) 
    #shared dicts
    manager = Manager()
    post_d = manager.list()
    comment_d = manager.list()
    all_d = manager.list()


    count=0
    for filename in os.listdir("LIWC_DATA/utility_graphs/"):
        count += 1
        D={}
        if not filename.startswith("%s_di" % sys.argv[1]):
            continue
        g = nx.read_gexf('LIWC_DATA/utility_graphs/'+filename) #HACK for top dir
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
        print "Read files"
        #pdb.set_trace()
    df=pd.DataFrame(ListOfDicts)
    df=order(df,['filename', 'max_core_number',  'nontrivial sccs','NT nontrivial sccs','NT max_core_number' ] )
    #matplotlib inline
    dp = df.plot()
    dp.legend(loc='upper left', fontsize=7)

    

    # multithreading to speed the processing time 
    
    # print "thread start"
    # executor = concurrent.futures.ProcessPoolExecutor(3)
    # future = [executor.submit(tryMultiThread, filename) for filename in os.listdir(".")]
    # concurrent.futures.wait(future)
    # print "thread end"

    for filename in os.listdir("LIWC_DATA/utility_graphs/"):
        pool.apply_async(tryMultiThread, ('LIWC_DATA/utility_graphs/'+filename,all_d,post_d,comment_d))

    pool.close()
    # wait for all the threads to finish
    pool.join()
    #end multiprocess
    for x in all_d:
        listOfDicts.append(x)

    for x in post_d:
        listOfLIWCDictsPosts.append(x)

    for x in comment_d:
        listOfLIWCDictsComments.append(x)

    drawMe(listOfDicts, "graph", sys.argv[1])
    drawMe(listOfLIWCDictsPosts, "LIWC-posts", sys.argv[1])
    drawMe(listOfLIWCDictsComments, "LIWC-comments", sys.argv[1])