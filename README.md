LymeDisease

Run the following command in sequence to replicate the project structure, 

1) Download Data
	->>>	downloadFiles.sh

2) Perform LDA topic modelling
	->>>	LDA.sh

3) Perform Time Series Analysis, this will most likely take a LOT of time to complete(anywhere from 3 to 24 hours)
   Since the new code performs a milestone operation on processing every file, you can look at the results obtained and run
   the graphing program simultaneously 

	eg.	TimeSeriesAnalysis.sh year windowNumber
	->>>	TimeSeriesAnalysis.sh 2006 13

4) Geo Mapping user comments and posts
	->>>	getLocation.sh 

5) Graphing time series analysis resutls simultaneously, try running this file on obtaining a sufficient amount of results from the step 3
	->>>	
