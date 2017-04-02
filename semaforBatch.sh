#!/bin/bash
export _JAVA_OPTIONS="-Xmx10g"
FILES=data/split/*
for f in $FILES
do
  echo "Processing $f file..."
  # take action on each file. $f store current file name
  time ./Semafor/semafor/bin/runSemafor.sh LymeDisease/$f ~/Capstone/SEMAFOR_OUTPUT/$f.txt 100
done
