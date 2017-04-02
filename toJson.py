import csv
import json
import sys

inFile = sys.argv[1]
outFile = sys.argv[2]

csvfile = open(inFile, 'r')
jsonfile = open(outFile, 'w')

reader = csv.DictReader(csvfile)
for row in reader:
    json.dump(row, jsonfile)
    jsonfile.write('\n')