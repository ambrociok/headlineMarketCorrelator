import scraper
import processor
import csv
from datetime import date, datetime
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import processor
import pandas as pd

def automation(): 
    d = str(date.today())
    t = datetime.now()

    #Update the fincial data to today's. Ensures getting previous day's information
    y = scraper.Scraper()
    y.getFinancialData()
    y.getHeadlines()

    #Create a massive dataframe for processing
    x = processor.Processor()
    df = x.mergeLabels()

    #Seperate dataframes for pre today and today
    df_test = df[df['date'] == d].drop_duplicates(ignore_index = True)
    df = df[~df['date'].str.contains(d)]

    #Vectorizes your phrases and creates your classifier
    counter = CountVectorizer(ngram_range=(2, 3))
    classifier = MultinomialNB()    
    counter.fit(df['title'] + df['description'])
    
    training_counts = counter.transform(df['title'])
    labels = df['label']

    #The vectorized counts of the headlines in df_test
    headline_counts = counter.transform(df_test['title'])

    #Training the model
    classifier.fit(training_counts, labels)
    prediction = classifier.predict(headline_counts)

    chance = 100*sum(prediction)/len(prediction)

    print('Chances of market going up tomorrow: {0:.2f}%'.format(100*sum(prediction)/len(prediction)))
    print(df_test.head())

    with open('predictions/predictionsForTomorrow.csv', 'a', newline = '') as currentCSV:
        writer = csv.writer(currentCSV)
        writer.writerow([d,t,chance])

if __name__ == "__main__":
    automation()