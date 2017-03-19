#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 17 10:02:45 2017

@author: harsh1692
"""

import json
import csv
import sys

posts=[]

# convert csv to JSON stream
def buildJSON():
    inputFile = input('Enter input filename ')
    outputFile = input('Enter output filename ')
    csvfile = open(inputFile, 'r')
    jsonfile = open(outputFile, 'w')

    reader = csv.DictReader(csvfile)
    for row in reader:
        json.dump(row, jsonfile)
        jsonfile.write('\n')    

# extract frames form semafor output and create a new JSON stream
def buildJSONSemafor():
    semaforOutput = input('Enter semafor output filename ')
    buildFile = input('Enter output filename ')
    buildJSON= open(buildFile,'w',encoding='utf-8')
    f = open(semaforOutput,'r',encoding='utf-8')
    for line in f:
        json_object={}
        json_data=json.loads(line)
        json_object_frames=[]
        for data in json_data['frames']:
            frame_line={}
            frame_line['target_name']=data['target']['name']
            for frame_data in data['target']['spans']:
                frame_line['target_text']=frame_data['text']
            frame_line['frame_roles']=[]    
            for annotation_data in data['annotationSets']:
                for frameElement in annotation_data['frameElements']:
                    frameElementRoles={}
                    for frameElementText in frameElement['spans']:
                        frameElementRoles['name']=frameElement['name']
                        frameElementRoles['text']=frameElementText['text']
                        frame_line['frame_roles'].append(frameElementRoles)
            json_object_frames.append(frame_line)                
        json_object['Frames']=json_object_frames    
        json.dump(json_object, buildJSON, ensure_ascii=False)
        buildJSON.write('\n')
    buildJSON.close()            

def mergeFrames():
    frames = input('Enter semafor frames filename ')
    posts = input('Enter file containing posts ')
    
    listOfFrames = []
    f = open(frames,'r',encoding='utf-8')
    for row in f:
        json_frame=json.loads(row)
        listOfFrames.append(json_frame)
    
    f = open(posts,'r',encoding='utf-8')
    i = 0
    for row in f:
        json_post=json.loads(row)
        json_post['Semafor_Frames'] = listOfFrames[i]
        i = i+1
        print(json_post)
        break

def main():
    print('1.Convert csv to json')
    print('2.Extract frames from semafor output')
    print('3.Combine semafor frames to posts')
    choice = input('Enter your choice ')
    if int(choice) == 1:
        buildJSON()
    elif int(choice) == 2:
        buildJSONSemafor()
    else:
        mergeFrames()

if __name__ == '__main__':
    main()    