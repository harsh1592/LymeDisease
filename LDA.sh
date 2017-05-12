#!/bin/bash
python2 LDA_lymeDisease.py data/outfile_content.csv 

python2 splitFileByYear.py

conda install -c https://conda.anaconda.org/amueller wordcloud

python2 try_wc.py data/2001_y.txt generatedFiles/2001.png 
python2 try_wc.py data/2002_y.txt generatedFiles/2002.png 
python2 try_wc.py data/2003_y.txt generatedFiles/2003.png 
python2 try_wc.py data/2004_y.txt generatedFiles/2004.png 
python2 try_wc.py data/2005_y.txt generatedFiles/2005.png 
python2 try_wc.py data/2006_y.txt generatedFiles/2006.png 
python2 try_wc.py data/2007_y.txt generatedFiles/2007.png 
python2 try_wc.py data/2008_y.txt generatedFiles/2008.png 
python2 try_wc.py data/2009_y.txt generatedFiles/2009.png
