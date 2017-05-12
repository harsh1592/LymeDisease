import time
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
import csv
import sys
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import spacy
import geocoder
import googlemaps
from geopy.geocoders import Nominatim
geolocator = Nominatim()
nlp = spacy.load('en')

gmaps = googlemaps.Client(key='AIzaSyBF7sF05T-DdLN-8bnFFS5IRmV3UUxQXvU')

nlp.vocab[u'lyme'].is_stop = True
nlp.vocab[u'Borrelia'].is_stop = True

stopwords = ['lyme','borrelia','chlorella']

def getLocation(g):
    location_name = []
    location_coord = []
    for x in g:
        doc5 = nlp(g.node[x]['text'])
        for ent in doc5.ents:
            if str(ent).lower() not in stopwords:
                if ent.label_=="GPE": 
                    geocode_result = gmaps.geocode(str(ent))
                    # code = geocoder.google(str(ent))
                    if geocode_result:
                        location =  geocode_result[0]['geometry']['location']
                        latitude, longitude = location['lat'], location['lng']
                        print latitude,longitude
                        location_coord.append({'latitude':latitude,'longitude': longitude})
    return location_coord

def WriteDictToCSV(csv_file,csv_columns,dict_data):
    try:
        with open(csv_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in dict_data:
                writer.writerow(data)
    except IOError as (errno, strerror):
        print("I/O error({0}): {1}".format(errno, strerror))    
    return 

if __name__ == '__main__':
    for filename in os.listdir("LIWC_DATA/utility_graphs/"):
        print filename
        g = nx.read_gexf("LIWC_DATA/utility_graphs/"+filename) 
        place = getLocation(g)
        csv_columns = ['latitude','longitude']
        file = ntpath.basename(filename)
        url = 'LIWC_DATA/LOCATION_FILES/'+file+'post_Location.csv'
        WriteDictToCSV(url,csv_columns,place)
        

        
        