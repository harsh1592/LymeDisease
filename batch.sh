#!/bin/bash
echo "What is your preferred programming / scripting language"
echo "1) Perform LDA topic modelling"
echo "2) Perform Time Series Analysis"
echo "3) Create word cloud"
echo "4) Install word cloud"
echo "5) Download Data folder"
echo "6) Exit"
read case;

case $case in
	    1) 
	echo "Performing LDA...";;
	    2) 
	echo "Performing Time Series Analysis..."
	#convert csv to json
	echo "Step 1. Converting CSV to JSON..."
	python2 toJson.py data/community_posts_Processed.csv data/community_posts_Processed.json
	echo "community_posts_Processed.json created under /data"
	#now perform mongo import
	echo "Step 2. Importing data to mongodb..."
	mongoimport --db db --collection testCollection < data/community_posts_Processed.json
	echo "Finished importing csv file to mongodb"
	echo "Step 3. Starting time series analysis"
	echo "Step 3a. Creating post and comment graphs"
	python2 create_utility_files.py
	echo "Step 3b. Creating utility graphs"
	python2 create_graph_files.py
	echo "Step 3c. Starting time series analysis"
	python2 multithread_timeSeries.py
	echo "Finished time series analysis";;
	    3)
	echo "Performing word cloud visualization..."
	wordcloud_cli.py --text data/postsContent.csv --imagefile generatedFiles/wordcloud.png --stopwords data/stopwords_mod.txt
	echo "Word Cloud created in /generated";;
		4)
	echo "Installing word cloud..."
	conda install -c https://conda.anaconda.org/amueller wordcloud
	echo "Downloading Data folder..." 
   	wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=0B1LdyitP3FKbMXJHTE9nM0R4SFE' -O data/stopwordsDrive.txt
   	wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=0B1LdyitP3FKbaE8zX2pCSnNnMW8' -O data/community_posts_Processed.csv
   	wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=0B1LdyitP3FKbbHVmZkMwNEpBY2c' -O data/frequentWords.txt
   	wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=0B1LdyitP3FKbMjhRSG1fbXZnZDg' -O data/postsContent.csv
   	wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=0B1LdyitP3FKbRzNfdjFnMHZXR28' -O data/users.json
   	echo "Finieshed downloading all data";;
		5)
    echo "Finished Installing word cloud";;
		6)
	exit
esac 
