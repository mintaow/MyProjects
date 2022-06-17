# -*- coding: utf-8 -*-
"""
Created on Wed May  4 23:27:48 2022

@author: minta
"""

import numpy as np # linear algebra
import pandas as pd # data processing
import tweepy as tw
import oauth2 as oauth
import time

CONSUMER_KEY = '3wXfXQKBZKG6GcXh0d8j03GRR'
CONSUMER_SECRET = 'LMgT2HTbsiUVxDX5XrItWwfNBnAhWa34ihkRwI83XmhgLMfXq0'
ACCESS_KEY = '1511369498204409861-fANsQDZjWyKVxmHgalQdWOwDQAQlWQ'
ACCESS_SECRET = 'ArgE3tBJCZvYYlN12zQHmxEMeKEje7GnQJtuJtKHQlVv3'
BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAAKnLcAEAAAAAGYnIkFsqJu4O%2BuIvkx1SPn2htBU%3DYNKxPPDLNr1uIMhjUI071W8Wy2lLDs8e2V2J3XL5Q31GVUNLMc'
# This method is done for you.
def build_connection():
    """ Construct a twitter api instance using your tokens entered above.
    Returns:
      An instance of the twitter API.
    """
    client = tw.Client(BEARER_TOKEN, wait_on_rate_limit=True) 

    if(client):
        print('Established Twitter connection Using OAuth2.')
    return client

# running example
client = build_connection()


# Replace with your own search query
query = '(btc OR bitcoin OR crypto OR eth OR memecoin) -is:retweet lang:en' # keyword list is verified in several articles. 
start_time = '2019-01-01T00:00:00Z'
end_time = '2019-12-01T00:00:00Z'
df = pd.read_csv('crypto_tweets_20191123_20191130.csv',parse_dates = ['create_ts'])

def tweepy_search_tweets(query, start_time, end_time, max_results):
    tweets = client.search_all_tweets(query=query, 
                                      start_time = start_time,
                                      end_time = end_time,
                                        tweet_fields=['created_at','public_metrics','geo'], 
                                        expansions=['author_id','geo.place_id'], # according to Twitter official doc, only a small portion of tweets is geo-tagged. (https://developer.twitter.com/en/docs/tutorials/building-high-quality-filters)
                                        place_fields = ['place_type','geo'],
                                        max_results=max_results) # max_results – The maximum number of search results to be returned by a request. A number between 10 and the system limit (currently 500)
    if tweets:
      print(f'Retrieved Tweets Response Successfully')
    else:
      print("None Response.")
    return tweets



def write_search_tweets_to_df(tweets, df):
    tweets_data = tweets.data

    tmp1 = pd.DataFrame(columns = ['tweet_id','user_id','text','create_ts','retweet_cnt','reply_cnt','like_cnt','quote_cnt','geo_place_id'])
    
    for i in range(len(tweets.data)):
      print(i)
      tmp1 = tmp1.append(pd.DataFrame([[
                tweets_data[i].id,
                tweets_data[i].author_id,
                tweets_data[i].text,
                tweets_data[i].created_at,            
                tweets_data[i].public_metrics['retweet_count'],
                tweets_data[i].public_metrics['reply_count'],
                tweets_data[i].public_metrics['like_count'],
                tweets_data[i].public_metrics['quote_count'],
                'NoGeoInfo' if tweets_data[i].geo is None else tweets_data[i].geo['place_id']]],
              columns = ['tweet_id','user_id','text','create_ts','retweet_cnt','reply_cnt','like_cnt','quote_cnt','geo_place_id']),
              sort = True,
              ignore_index = True)

#    for i in range(len(tweets_user_includes)):
#      tmp2 = tmp2.append(pd.DataFrame([[
#                tweets_user_includes[i].id,
#                tweets_user_includes[i].username]],
#              columns = ['user_id','user_name']),
#              ignore_index = True)
    df = pd.concat([df, tmp1], axis = 0, ignore_index = True, sort = True) 

    if len(df)>df.tweet_id.nunique():
      print("Duplicates detected.")
      df = df.drop_duplicates()
    else:
      print("---------- Response Info ------------------")
      print(f"Number of tweets: {len(tmp1)};\nResponse Time Range: [{tmp1.create_ts.min()}, {tmp1.create_ts.max()}];")
      print("------------ Complete ---------------------")
    return df
  
    
i = 584
while True:
  try:
    i+=1
    print(f"========= {i}th Request ==================")
    end_time = df.create_ts.min()
    df = write_search_tweets_to_df(tweepy_search_tweets(query, start_time, end_time, 500),df)
    print(f"df now has {len(df)} rows \n")
    print(f"==========================================")
  except Exception as e:
      print("Error Captured:", e)
      # time.sleep(60)
      break