#!/bin/bash
python2 try_lda.py data/outfile_content.csv 

python2 splitFileByYear.py

conda install -c https://conda.anaconda.org/amueller wordcloud

wordcloud_cli.py --text data/2001_y.txt --imagefile generatedFiles/2001.png --stopwords data/stopwords_mod.txt --height 480 --width 720
wordcloud_cli.py --text data/2002_y.txt --imagefile generatedFiles/2002.png --stopwords data/stopwords_mod.txt --height 480 --width 720
wordcloud_cli.py --text data/2003_y.txt --imagefile generatedFiles/2003.png --stopwords data/stopwords_mod.txt --height 480 --width 720
wordcloud_cli.py --text data/2004_y.txt --imagefile generatedFiles/2004.png --stopwords data/stopwords_mod.txt --height 480 --width 720
wordcloud_cli.py --text data/2005_y.txt --imagefile generatedFiles/2005.png --stopwords data/stopwords_mod.txt --height 480 --width 720
wordcloud_cli.py --text data/2006_y.txt --imagefile generatedFiles/2006.png --stopwords data/stopwords_mod.txt --height 480 --width 720
wordcloud_cli.py --text data/2007_y.txt --imagefile generatedFiles/2007.png --stopwords data/stopwords_mod.txt --height 480 --width 720
wordcloud_cli.py --text data/2008_y.txt --imagefile generatedFiles/2008.png --stopwords data/stopwords_mod.txt --height 480 --width 720
wordcloud_cli.py --text data/2009_y.txt --imagefile generatedFiles/2009.png --stopwords data/stopwords_mod.txt --height 480 --width 720