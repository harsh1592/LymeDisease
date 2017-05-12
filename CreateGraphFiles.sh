#!/bin/bash
mkdir LIWC_DATA

year = $1
#convert csv to json
python2 toJson.py data/community_thread.csv data/community_thread.json
python2 toJson.py data/community_posts_Processed.csv data/community_posts_Processed.json

#now perform mongo import
mongoimport --db db --collection threads < data/community_thread.json
mongoimport --db db --collection posts < data/community_posts_Processed.json

python2 create_utility_files_mod.py year

python2 create_graph_files_mod.py