import csv
import sys
import pdb
import os
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

listOfDicts = []
listOfLIWCDictsPosts = []
listOfLIWCDictsComments = []

def drawMe(thisList, fileName, window):
    df = pd.DataFrame(thisList)

    dp = df.plot(subplots=True, figsize=(6, 25), fontsize=6,
                 yticks=(0.00, 1.00, 2.00, 3.00, 4.00))

    plt.savefig('LIWC_DATA/LIWC_OUTPUT/' + window +
                "-" + fileName + '-measures.pdf')

    plt.clf()
    file('LIWC_DATA/LIWC_OUTPUT/%s-graph-%s.csv' %
         (window, fileName), 'w').write(df.to_csv())

def joinFiles():
    

    graphFileList = []
    postsFileList = []
    commentFileList = []
    for filename in os.listdir("LIWC_DATA/CSV/"):
        if 'posts' in filename: postsFileList.append(filename)
        elif 'comments' in filename: commentFileList.append(filename)
        elif 'graph' in filename: graphFileList.append(filename)
    graphFileList = sorted(graphFileList)
    postsFileList = sorted(postsFileList)
    commentFileList = sorted(commentFileList)
    
    for file in graphFileList:
        with open('LIWC_DATA/CSV/'+file) as f:
            d = {}
            for line in f:
                (key, val) = line.split(',')
                d[key] = float(val)
            listOfDicts.append(d)
    for file in postsFileList:
        with open('LIWC_DATA/CSV/'+file) as f:
            d = {}
            for line in f:
                (key, val) = line.split(',')
                d[key] = float(val)
            listOfLIWCDictsPosts.append(d)
    for file in commentFileList:
        with open('LIWC_DATA/CSV/'+file) as f:
            d = {}
            for line in f:
                (key, val) = line.split(',')
                d[key] = float(val)
            listOfLIWCDictsComments.append(d) 

if __name__ == '__main__':
    joinFiles()
    drawMe(listOfDicts, "graph", sys.argv[1])
    drawMe(listOfLIWCDictsPosts, "LIWC-posts", sys.argv[1])
    drawMe(listOfLIWCDictsComments, "LIWC-comments", sys.argv[1])