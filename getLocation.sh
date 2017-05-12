#!/bin/bash

for file in LIWC_DATA/utility_graphs/*
do
	echo $file
	# using the below script with an online geo-coder will \
	# work better but no free tools available to work with lots of data
	#
	# python2 space_trial.py $file
	python2 onlyLocationName.py $file 
done
