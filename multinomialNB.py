#%%
import os
import sys
os.getcwd()
sys.path
#%%
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
import processor
import pandas as pd
#%%
x = processor.Processor()
df = x.mergeLabels()
print(df.dtype)

#%% Initialize the models

counter = CountVectorizer(ngram_range=(2, 3))
classifier = MultinomialNB()

#%% Fits the model

counter.fit(df['title'] + df['description'])
training_counts = counter.transform(df['title'])# + df['description'])
#print(counter.get_feature_names())

#%%
example_headline = ["When U.S. cases of COVID-19 started multiplying back in March, the economy pretty much imploded overnight, and by late March, stocks plunged into bear market territory for the first time in over a decade. Since then, things have picked up in the stock market, and despite a recent patch of volatility, stocks have largely recovered their value. But the worst may not be over.",\
    'Tesla shares skyrocket due to the new discoveries that they have exceeded expectations for this quarter',\
    'House Passes Second Stimulus Legislation of 5.4 trillion dollars',\
    'Amazon stock makes great leaps after quarter of increased sales and gains',\
    'Hiring Surged In June With 4.8 Million Jobs Added Before New Spike In Infections',\
    'The dollar is worth nothing now. Child labor is at an all time high. The united states has run down. Epstein didn\'t kill himself',\
    'The United states has beaten the Coronavirus. Stores are reopening and stocks are at an all time high',\
    'Starting tomorrow there will be a an increased tax on fossil fuels and every other industry',\
    'A process of mass producing a vaccine for covid has been found and is now easily accessible to the United States',\
    'Trump reelected',\
    'The JFK airport has been 9/11\'ed and can is no longer operational',\
    'Disney executive moved to tiktok during pandemic',\
    'Disney executive moved to tiktok']
headline_counts = counter.transform(example_headline)

# %%
labels = df['label']

classifier.fit(training_counts, labels)
prediction = classifier.predict(headline_counts)
print(prediction)
print(classifier.predict_proba(headline_counts))


# %% 