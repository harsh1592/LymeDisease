import csv
import sys
from bs4 import BeautifulSoup

filename = sys.argv[1]
data =[]
with open(filename) as csvfile:
	readCSV = csv.reader(csvfile, delimiter=',')
	for row in readCSV:
		line =[]
		Content = row[3]		
		dateStr = str(row[5])
		dateStamp = dateStr[:4]+"/"+dateStr[4:6]+"/"+dateStr[6:8]+" "+dateStr[8:10]+":"+dateStr[10:12]
		Content = Content.replace(","," ")
		Content = Content.replace(";"," ")
		Content = Content.replace("\n"," ")
		Content = Content.replace("\t"," ")
		soup = BeautifulSoup(Content,"lxml")		
		text = soup.get_text()
		
		line.append(row[0])
		line.append(row[1])
		line.append(row[2])
		line.append(row[6])
		line.append(dateStamp)
		line.append(text)
		data.append(line)

with open(sys.argv[2], 'w') as f:
        writer = csv.writer(f)
        writer.writerows(data)
