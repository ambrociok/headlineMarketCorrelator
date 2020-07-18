import scraper
import processor
import csv
from datetime import date, datetime
import time
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import processor
import pandas as pd
import numpy as np

def automation(): 
    d = str(date.today())
    t = datetime.now()

    #Create a massive dataframe for processing
    x = processor.Processor()
    df = x.mergeLabels()
    y = scraper.Scraper()
    

    #Seperate dataframes for pre today and today
    df_test = y.getNewHeadlines().drop_duplicates(keep='first')
    df1 = df[df['date'] == d].drop_duplicates(ignore_index = True)
    df = df[~df['date'].str.contains(d)]


    #Vectorizes your phrases and creates your classifier
    counter = CountVectorizer(ngram_range=(2, 3))
    classifier = MultinomialNB()    
    counter.fit(df['title'] + df['description'])
    
    training_counts = counter.transform(df['title'])
    labels = df['label']

    #The vectorized counts of the headlines in df_test
    headline_counts = counter.transform(df_test['title'])
    headline_counts_ticker = counter.transform(df1['title'])

    #Training the model
    classifier.fit(training_counts, labels)
    prediction = classifier.predict(headline_counts)
    prediction1 = classifier.predict(headline_counts_ticker)

    chance = 100*sum(prediction)/len(prediction)
    chanceticker = 100*sum(prediction1)/len(prediction1)

    totalChance = (chance + chanceticker)/2

    print('Chances of market going up tomorrow: {0:.2f}%'.format(totalChance))
    print('New Headline Chances: {0:.2f}%'.format(chance))
    print('Ticker Headline Chances: {0:.2f}%'.format(chanceticker))
    print('Prediction New Headline Length: {}'.format(np.size(classifier.predict_proba(headline_counts), 0 )))
    print('Prediction Ticker Headline Length: {}'.format(np.size(classifier.predict_proba(headline_counts_ticker), 0 )))

    with open('predictions/predictionsForTomorrow.csv', 'a', newline = '') as currentCSV:
        writer = csv.writer(currentCSV)
        writer.writerow([d,t,totalChance])

if __name__ == "__main__":
    automation()
    time.sleep(5)