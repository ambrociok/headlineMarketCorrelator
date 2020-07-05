import csv
import requests
import json
import pandas as pd
import time
import constants
from datetime import date, datetime

# This is the standard tickers will be
# ['NASDAQ','Dow Jones', 'S&P 500', 'QQQ','MSFT','AAPL','AMZN','GS','GOOG','FB','BRK.B']

class Scraper():
    def __init__( self, ticker = ['NASDAQ','Dow Jones', 'S&P 500', 'QQQ','MSFT','AAPL','AMZN','GS','GOOG','FB','BRK.B'], date = date.today(), hour = int(time.strftime("%H")) ): 
        self.ticker = ticker
        self.date = date
        self.hour = hour
    
    def getHeadlines(self):
        ### This function gets the article names and descriptions from newsapi
        #       This is meant to only get daily information for every article with
        #       the ticker in the title
        articles = []
        for tick in self.ticker:
            url = ('http://newsapi.org/v2/everything?'
                    'q={}&'
                    'apiKey={}')
            response = requests.get(url.format(tick, constants.newsapikey))
            for article in response.json()['articles']:
                articles.append([article['publishedAt'], tick , article['title'], article['description'] ])
        return articles

    def createDataframe(self):
        ### Creates a dataframe of the day using the getArticleHeadlines function
        newArticles = self.getHeadlines()
        df = pd.DataFrame(newArticles).rename(columns = {0: 'datePublished', 1: 'ticker', 2:'title', 3:'description'})
#        df['date'] = [date] * len(df) Redundant
        return df 

    def createCSV(self):
        ### This creates a new CSV file that will be compiled every month. Monthly information reader will
        #       be made in a different file. Headlines are only scrubbed EOD
        quarter = int(self.hour/5)
        df = self.createDataframe()
        df.to_csv('dailyData/{}q{}.csv'.format(self.date,quarter), encoding='utf-8')
    
    def getEODData(self):
        changes = []
        for tick in self.ticker:
            url = ('https://financialmodelingprep.com/api/v3/historical-price-full/^DJI?apikey={}')
            response = requests.get(url.format(constants.apikey)).json()
            print(response)
            changes.append([tick, response['open'], response['close'], response['changePercent']])
        return changes

