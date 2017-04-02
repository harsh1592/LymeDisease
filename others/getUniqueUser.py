import csv
import collections
import pymongo
import copy
import sys
from pymongo import MongoClient
from pymongo.cursor import _QUERY_OPTIONS
from pymongo.errors import AutoReconnect
from bson.timestamp import Timestamp
from collections import defaultdict

def main ():
	user_dict = {}
	client = MongoClient('mongodb://localhost:27017/')
	db = client.test
	collection = db.posts
	count=0
	for post in collection.find():
		if post['PosterID'] not in user_dict:			
			user_dict[post['PosterID']] = post['PosterName']

	with open('users.csv', 'w') as csv_file:
		writer = csv.writer(csv_file)
		for key, value in user_dict.items():
			writer.writerow([key, value])

if __name__ == '__main__': 
	main()