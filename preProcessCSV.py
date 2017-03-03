import csv
import sys
from bs4 import BeautifulSoup

filename = sys.argv[1]
with open(filename) as csvfile:
	readCSV = csv.reader(csvfile, delimiter=',')
	for row in readCSV:
		ThreadRef = row[0]
		ReplyNum = row[1]
		PosterID = row[2]
		Content = row[3]
		notes = row[4]
		PostedOn = row[5]
		PosterName = row[6]
		Gathered = row[7]
		
		dateStr = str(PostedOn)
		print(dateStr[:4]+"/"+dateStr[4:6]+"/"+dateStr[6:8]+" "+dateStr[8:10]+":"+dateStr[10:12])
		
		Content = Content.replace(","," ")
		#Content = Content.replace("<br />"," ")
		Content = Content.replace("\n"," ")
		Content = Content.replace("\t"," ")
		soup = BeautifulSoup(Content)
		#Content = Content.replace("<(?:[^>=]|='[^']*'|=\"[^\"]*\"|=[^'\"][^\s>]*)*>","")		
		print( soup.get_text())

		print("\n")
    