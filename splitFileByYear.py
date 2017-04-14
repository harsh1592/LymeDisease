import os
import csv
import pymongo
import sys
import time
import string
import datetime
import pdb
from pymongo import MongoClient
from pymongo.cursor import _QUERY_OPTIONS
from pymongo.errors import AutoReconnect
from bson.timestamp import Timestamp

yearDict = {'2001':[],'2002':[],'2003':[],'2004':[],'2005':[],'2006':[],'2007':[],'2008':[],'2009':[]}

def read_date(date):
    try:
        output = datetime.datetime.strptime(date, "%Y/%m/%d %H:%M")
    except ValueError as e:
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


def createFiles():
	client = MongoClient('mongodb://localhost:27017/')
	db = client.test
	collection = db.posts
	for post in collection.find():
		# date = post['PostedOn'].split(" ")[0]
		date = read_date(post['PostedOn'])
		# date = datetime.datetime.strptime(date, "%Y/%m/%d")
		if date < datetime.datetime(2002,1,1):
			yearDict['2001'].append(post['Content'])
		elif date < datetime.datetime(2003,1,1):
			yearDict['2002'].append(post['Content'])
		elif date < datetime.datetime(2004,1,1):
			yearDict['2003'].append(post['Content'])
		elif date < datetime.datetime(2005,1,1):
			yearDict['2004'].append(post['Content'])
		elif date < datetime.datetime(2006,1,1):
			yearDict['2005'].append(post['Content'])
		elif date < datetime.datetime(2007,1,1):
			yearDict['2006'].append(post['Content'])
		elif date < datetime.datetime(2008,1,1):
			yearDict['2007'].append(post['Content'])
		elif date < datetime.datetime(2009,1,1):
			yearDict['2008'].append(post['Content'])
		elif date < datetime.datetime(2010,1,1):
			yearDict['2009'].append(post['Content'])

	for x,v in yearDict.items():
		f = open('data/'+x+'_y.txt','w')
		f.write("\n".join(v).encode('utf8'))
		f.close()
if __name__ == '__main__':
	createFiles()