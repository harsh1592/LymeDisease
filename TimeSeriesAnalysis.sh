#!/bin/bash

#convert csv to json
python2 toJson.py data/community_posts_Processed.csv data/community_posts_Processed.json

#now perform mongo import
mongoimport --db db --collection testCollection < data/community_posts_Processed.json

python2 create_utility_files.py

python2 create_graph_files.py

python2 multithread_timeSeries.py