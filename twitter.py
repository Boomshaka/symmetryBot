from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import tweepy
import wget
import hashlib
# import symmetry
import requests
import os
import io
import time
import datetime
from datetime import date

# from google.cloud import vision
# from google.cloud.vision import types

import numpy as np
import pandas as pd
import twitter_credentials

### TWITTER CLIENT ###
#In charge of all activities performed on twitter account
class TwitterClient():
    def __init__(self, user=None):
        self.auth = Authentication().authenticate()
        self.api = tweepy.API(self.auth)

        self.user = user

    def get_twitter_client_api(self):#retrieves api to use rest of function
        return self.api

    def getUserTweets(self, num_tweets):#get most recent num_tweets number of tweets by self
        userTweets = []
        for tweet in Cursor(self.api.user_timeline, id=self.user).items(num_tweets):
            userTweets.append(tweet)
        return userTweets

    def getFriendList(self, num_friends):#get list of followers
        friendList = []
        for friend in Cursor(self.twitter_client.friends, id=self.user).items(num_friends):
            friendList.append(friend)
        return friendList

    def getTimelineTweets(self, num_tweets):#Get tweets from timeline
        timelineTweets = []
        for tweet in Cursor(self.twitter_client.home_timeline, id=self.user).items(num_tweets):
            timelineTweets.append(tweet)
        return timelineTweets

    def get_mentions(self, num_tweets):#Get mentions of user on timeline
        lst = []
        tweets = api.mentions_timeline(count = num_tweets)

        for tweet in tweets:
            lst.append(tweet)
        return lst

    def get_in_reply_to(self, tweets):#get the original tweet a tweet is replying to
        lst = []
        for tweet in tweets:
            lst.append(tweet.in_reply_to_status_id)
        return lst

    def get_images_mentioned(self, num_tweets):#get image of tweet a tweet is replying to
        images = get_images(get_in_reply_to(get_mentions(num_tweets)))
        return images

    def get_images(self, tweets):#get image of tweets
        media_files = []
        for status in tweets:
            media = status.entities.get('media', [])
            if(len(media) > 0):
                media_files.append(media[0]['media_url'])
        return media_files



    def tweet_image(self, url, message=""):#Tweet the image associated to the link

        filename = 'temp.jpg'
        request = requests.get(url, stream=True)
        if request.status_code == 200:
            with open(filename, 'wb') as image:
                for chunk in request:
                    image.write(chunk)

            api.update_with_media(filename, status=message)
            os.remove(filename)
        else:
            print("Unable to download image")


    def delete_tweets(self, num_tweets):#Deletes the most recent tweets of user
        my_tweets = api.user_timeline(count=num_tweets)

        for tweet in my_tweets:
            api.destroy_status(tweet.id)


#### TWITTER AUTHENTICATOR ####
class Authentication():
    def authenticate(self):
        auth = tweepy.OAuthHandler(twitter_credentials.CONSUMER_API, twitter_credentials.CONSUMER_API_SECRET)
        auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)
        return auth

#### TWITTER STREAMER ####
class TwitterStreamer():
    def __init__(self):
        self.twitter_authenticator = Authentication()

    def stream_tweets(self, fetched_tweets_filename, hash_tag_list):
        listener = StdOutListener(fetched_tweets_filename)


        stream = tweepy.Stream(auth, listener)

        stream.filter(track= hash_tag_list)

class StdOutListener(StreamListener):

    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

    def on_data(self, data):
        try:
            print(data)
            with open(self.fetched_tweets_filename, 'a') as tf:
                tf.write(data)
            return True
        except BaseException as e:
            print("Error on data: %s" % str(e))
        return True

    def on_error(self, status):
        if status == 420:
            #Returning false in case reached limit
            return False
        print(status)

class TweetAnalyzer():
    def tweets_to_data_frame(self,tweets):
        dataframe = pd.DataFrame(data=[tweet.id for tweet in tweets], columns=['Tweets'])
        #dataframe['source'] = np.array([tweet.entities for tweet in tweets])
        #dataframe['in_reply_to_status_id'] = np.array([tweet.in_reply_to_status_id for tweet in tweets])
        #dataframe['str version'] = np.array([tweet.in_reply_to_status_id_str] for tweet in tweets)

        return dataframe



if __name__ == "__main__":

    twitter_client = TwitterClient()
    tweet_analyzer = TweetAnalyzer()
    api = twitter_client.get_twitter_client_api()

    # df = tweet_analyzer.tweets_to_data_frame(tweets)
    # print(df.head(10))
    # print(dir(tweets[0]))

    while True:
        if datetime.datetime.now().hour == 0 or datetime.datetime.now().hour == 12 or datetime.datetime.now().hour == 18:
            tweets = api.user_timeline(screen_name='GhibliQuotes', count=3, include_rts=False)
            media_files = []
            for status in tweets:
                media = status.entities.get('media', [])
                if(len(media) > 0):
                    media_files.append(media[0]['media_url'])
            for i in media_files:
                twitter_client.tweet_image(i)

            print ('sleeping ... ', datetime.datetime.now())
            time.sleep(3600)

        else:
            print('sleeping ...', datetime.datetime.now())
            time.sleep(1)






        #wget.download(i)

### Work in progress to use face detection and edit an image ###

    # symmetrify = symmetry.Symmetry('nWPANwUxEQ3GtQpoyCnxhv084')
    # for pictures in media_files:
    #     text = ""
    #     # hashed_url = hashlib.md5(pictures.encode()).hexdigest()
    #     # print(hashed_url)
    #     # media_ids = [api.media_upload(pictures).media_id_string]
    #     # api.update_status(status=text, media_ids=media_ids)
    #     sym_result = symmetrify.work(pictures)
    #     for c, n in enumerate(sym_result):
    #         text = ""
    #         media_ids = [api.media_upload(m).media_id_string for m in n]
    #         api.update_status(status=text, media_ids=media_ids)
