import csv
import requests
import json
import pandas as pd
import time
import constants
from datetime import date, datetime
from bs4 import BeautifulSoup

# This is the standard tickers will be
# ['NASDAQ','Dow Jones', 'S&P 500', 'QQQ','MSFT','AAPL','AMZN','GS','GOOG','FB','BRK.B']
# I am keeping the ticker tracking to be static as the purpose of this is to train the model based solely on
#   varying types of news and to eventually allow for the segmentation of market outlook based on news source

class Scraper():
    def __init__( self, ticker = ['NASDAQ','Dow Jones', 'S&P 500', 'QQQ','MSFT','AAPL','AMZN','GS','GOOG','FB'], date = date.today(), hour = int(time.strftime("%H")) ): 
        self.ticker = ticker
        self.date = date
        self.hour = hour
    
    def getHeadlines(self):
        ### This method gets the article names and descriptions from newsapi
        #       This is meant to only get daily information for every article with
        #       the ticker in the title
        ticker_name = ['NASDAQ','Dow Jones','S&P 500', 'QQQ','Microsoft','Apple','Amazon','Goldman Sachs','Google','Facebook']
        ticker_dict = {self.ticker[i]:ticker_name[i] for i in range(len(ticker_name))}
        articles = []
        for tick in self.ticker:
            url = ('http://newsapi.org/v2/everything?'
                    'q={}&'
                    'apiKey={}')
            response = requests.get(url.format(ticker_dict[tick], constants.newsapikey))
            for article in response.json()['articles']:
                articles.append([article['publishedAt'], tick , article['title'], article['description'] ])
        return articles

    def getNewHeadlines(self):
        ### This method gets the newest headline information that isn't necessarily
        #       related to any ticker. This will be used as the basis for daily predictions
        articles = []
        url = ('https://newsapi.org/v2/top-headlines?country=us&category=business&'
                'apiKey={}')
        response = requests.get(url.format(constants.newsapikey))
        for article in response.json()['articles']:
            articles.append([article['publishedAt'], article['title'], article['description'] ])
        df = pd.DataFrame(articles).rename(columns = {0: 'datePublished',1:'title', 2:'description'})
        df.to_csv('dailyHeadlinesUnrelated/{}.csv'.format(self.date), encoding='utf-8')
        return df

        
    def createDataframe(self):
        ### Creates a dataframe of the day using the getArticleHeadlines method
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
    
    def getFinancialData(self):
        def getWebsite(tick):
            r = requests.get('https://finance.yahoo.com/quote/' + tick + '/history?p=' + tick)
            return r
        ticker_name = ['^IXIC', '^DJI', '^GSPC', 'QQQ', 'MSFT', 'AAPL', 'AMZN', 'GS', 'GOOG', 'FB']
        ticker_dict = {ticker_name[i]:self.ticker[i] for i in range(len(ticker_name))}
        date_format = str(date.today())
        for tick in ticker_name:
            r = getWebsite(tick)
            soup = BeautifulSoup(r.text, 'lxml')
            row = soup.find('tr', {"BdT Bdc($seperatorColor) Ta(end) Fz(s) Whs(nw)"}).find_all('td')
            row_info = []
            for i in range(len(row)) :
                if row_info == []:
                    row_info.append(date_format)
                else:
                    row_info.append(row[i].text.replace(',',''))
            with open('financialData/{}.csv'.format(ticker_dict[tick]), 'a', newline = '') as currentCSV:
                writer = csv.writer(currentCSV)
                writer.writerow(row_info)



