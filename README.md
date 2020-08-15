# headlineMarketCorrelater

## Project 1: Headline Market Trend Analyzer: Project Overview
- Created a web scraper that gets both the most popular news headlines based on stock tickers and current stock price information
- Created a pipeline that automatically saves and labels headlines at the end of the day based their ticker's stock price movement
- Incorporated an ngram language model to the data pipeline to tie words and subsets of phrases to stock movement
- Deployed a NB Classifier to fit transformed monogram and bigram dictionary from the data pipeline
- Created executables that can be set to run on windows schedule manager based on desired runtimes

## Code and Resources Used
**Python Version** 3.7
**Packages** pandas, numpy, sklearn, sys, os, re, glob, datetime, csv, requests, json, time, constants, bs4

# Discontinued (Aug 12, 2020)
Due to limited access to historical headline data, creating an accurately trained model using information pre Covid recession is impossible. The current model has a 65% accuracy rate at knowing which way the market would go the following day, but does not have enough data for the outcome to be related. Will consider going back after more market stablization. 

## Intro
This is meant to regularly scrape data online, label it based off of stock movement during the day and the associated stock to the article and train a model. Model can be used to determine stock price movement.

## Architecture
This project is in three parts, the scraper, data processor, and model.

##### Scraper
The scraper interacts with newsapi to get all of the latest headlines based off of the desired ticker to track. This can often return duplicates, but is handled during the data processing stage. The scraper also gathers stock data from Yahoo Finance (end of day). Afterwards, this information is put into respective CSV files for future reading. 

##### Data Processor
The data processing begins by checking the headlines and referencing the stock information of the same date and ticker. Based on if the stock price went up or down by the end of the day, a label is appended to the CSV file [1]. Afterwards, this is put through an ngram model that creates a dictionary of words and phrases of respective frequencies of all of the labeled CSV headline information [2][3].

##### Model
The most efficient model was a Naive Bayes Classifier that takes the input of new headline information at the end of the day and predicts the possible trend for the following day [4]. The modified CSV information is fed into the model and then can make predictions based off of the headlines and movement from the day. Iterations that changed when the model would be implemented have been tested and the end of day model use was the most effective/least random. 

## To Do List
- [x] Automate stock price collection from Yahoo  (07.06.2020)
- [x] Increase resolution from reading the market and labeling the articles
- [ ] Improve bad coding practices such as lack of class function flexibility
- [ ] Create a class for model testing
- [ ] Create a file that constantly runs to convert static data into a proper datastream
- [ ] UI?
- [ ] Create new model based on LSTM -> CNN -> Markov -> Dense layer structure


##### Current Shortcomings
- Difficult to train a model when there is no clear trend in the market
- Difficult to compensate for overly bearish headlines regardless of time of day (reference last two weeks of July)


[1] These labels were binary as this project started during the most volatile market to date
[2] Using tf-idf to slightly modify the weights has been explored, but led to no feasible change
[3] Misspelling of words was not taken into consideration
[4] This assumes isolated conditions. Things like after hours trading and after hours news cannot be taken into account as AH information is behind paywalls for many APIs/inaccessible through platforms like Yahoo Finance and MarketWatch
