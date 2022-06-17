# -*- coding: utf-8 -*-
"""
Created on Sat Apr 23 01:23:04 2022

@author: minta
"""

import numpy as np # linear algebra
import pandas as pd # data processing
import zipfile
import re
import sys
import seaborn as sns
import matplotlib.pyplot as plt


from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
 
# function to print sentiments
# of the sentence.
def get_vader_sentiment(sentence):
 
    # Create a SentimentIntensityAnalyzer object.
    sid_obj = SentimentIntensityAnalyzer()
 
    # polarity_scores method of SentimentIntensityAnalyzer
    # object gives a sentiment dictionary.
    # which contains pos, neg, neu, and compound scores.
    sentiment_dict = sid_obj.polarity_scores(sentence)
    sentiment_score = sentiment_dict['compound']

    # print("Overall sentiment dictionary is : ", sentiment_dict)
    # print("sentence was rated as ", sentiment_dict['neg']*100, "% Negative")
    # print("sentence was rated as ", sentiment_dict['neu']*100, "% Neutral")
    # print("sentence was rated as ", sentiment_dict['pos']*100, "% Positive")
    # print("Sentence Overall Rated As", end = " ")

    # sentimen classification
    if sentiment_dict['compound'] >= 0.05 :
        sentiment_type = 'positive'
    elif sentiment_dict['compound'] <= - 0.05 :
        sentiment_type = 'negative'
    else :
        sentiment_type = 'neutral'
    return sentiment_type, sentiment_score

# Read in the clean csv (English only)
def read_csv_chunk(filepath,chunksize):
    num_of_chunk = 0

    df = pd.DataFrame()

    for chunk in pd.read_csv(filepath,lineterminator='\n',
                             chunksize=chunksize):
        num_of_chunk += 1
        df = pd.concat([df, chunk], axis=0)
        print('Processing Chunk No. ' + str(num_of_chunk))     

    print("The dataset's shape: ", df.shape)
    df.reset_index(inplace=True)
    return df

df = read_csv_chunk('clean_16m_btc_tweets.csv',500000)
#df = read_csv_chunk('sample_data_1perc.csv',500000)

print("read file completed")

# Drop unnecessary columns to save memory
# df = df.drop(['index', 'Unnamed: 0'],axis= 1)
from datetime import datetime, date, time, timedelta
# Additional Data Processing

# After diving into the tweet content details and cross checking with the platform
# I decided to drop all the 220 tweets before 2012-01-01, I suspect that the API calling returns incomplete datasets (incontinuous date)
df = df[df.date>='2012-01-01']

df['date'] = list(map(lambda x: datetime.strptime(x,"%Y-%m-%d"),df.date))
df['year_month'] = list(map(lambda x:str(x.year)+"-"+str(x.month), df.date))
df['year'] = list(map(lambda x:x.year, df.date)) 


def text_preprocessing(text):
    """
    - Remove entity mentions (eg. '@united')
    - Correct errors (eg. '&amp;' to '&')
    @param    text (str): a string to be processed.
    @return   text (Str): the processed string.
    """
    # Remove '@name'
    text = re.sub(r'(@.*?)[\s]', ' ', text)

    # Remove Links
    text = re.sub(r'http\S+', '', text)                                

    # Replace '&amp;' with '&'
    text = re.sub(r'&amp;', '&', text)

    # Remove trailing whitespace
    text = re.sub(r'\s+', ' ', text).strip()

    return text

# Light Preprocessing for BERT (~2 min 10s for 13 million tweets)
df['clean_text'] = list(map(lambda x:text_preprocessing(x), df.text))

# Retrieve sentiment classification
# takes ~2 mins 10s to run for every 10,000 tweets 

# df[['sentiment_type','sentiment_score']] = list(map(lambda txt:get_vader_sentiment(txt), df.text)) # common method

vader_res = np.vectorize(get_vader_sentiment)(df.clean_text)
df['sentiment_type'] = vader_res[0]
df['sentiment_score'] = vader_res[1]
print("sentiment extract completed")
df.to_csv("clean_16m_btc_tweets_sentiments.csv")
print("File export completed")