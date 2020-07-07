import pandas as pd 
import glob
import re
from datetime import date
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB


class Processor():
    
    def __init__(self,  date = date.today() ):
        self.date = date

    def readAllCSV(self):
        ### Returns the data files from inside the daily data folder.
        #       As more time passes, the folder will just get more data and we will
        #       continually train the model to detect trends 
        filenames = glob.glob("dailyData/*.csv")
        dfs = []
        for filename in filenames:
            dfs.append(pd.read_csv(filename))
        df = pd.concat(dfs, ignore_index=True).drop_duplicates('title')
        return df

    def readAllFinancial(self):
        ### Reads through the financialData folder and returns a large df based on
        #       the ticker name.
        #       CURRENTLY UNDERENGINEERD. NEED TO CREATE AUTOMATION FOR HISTORIAL
        #       DATA SCRUBBING to CSV, BUT THERE ARE CURRENTLY SCRAPING LIMITATIONS
        def labeler(row):
            if abs(row) >= 0.0125:
                return 1
            else:
                return 0
        dfs = []
        counter = 0
        filenames = glob.glob("financialData/*.csv")
        for filename in filenames:
            name = re.search(r'financialData\\(.*)\.csv', filename)
            dfs.append(pd.read_csv(filename, usecols = ['Date','Open','Close']))
            dfs[counter]['ticker'] = name.group(1)
            counter += 1
        df = pd.concat(dfs, ignore_index=True, sort=False)
        df['label'] = (df['Open'] - df['Close'])/df['Close']
        df['label'] = df.apply(lambda row : labeler(row['label']), axis = 1)
        df = df[['Date', 'ticker', 'label']]
        print(df.dtypes)
        return df
    
    def mergeLabels(self):
        ### Merges the labels from the manually created label for the ticker and
        #       the respective stock movement % for the day as a binary distinction

        df0 = self.readAllCSV()
        df1 = self.readAllFinancial()
        df0['date'] = [a[:10] for a in df0['datePublished']]
        df1 = df1.rename(columns = {'Date':'date'})
        df = pd.merge(df0, df1, on=['ticker','date'], how='inner')
        df = df.drop(['Unnamed: 0', 'datePublished'], axis = 1)
        return df
