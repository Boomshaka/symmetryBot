#import importlib.util
#import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import tweepy
import wget
import hashlib
import symmetry
import requests
import os

import numpy as np
import pandas as pd
import twitter_credentials

class TwitterClient():
    def __init__(self, user=None):
        self.auth = Authentication().authenticate()
        self.api = tweepy.API(self.auth)

        self.user = user

    def get_twitter_client_api(self):
        return self.api

    def getUserTweets(self, num_tweets):
        userTweets = []
        for tweet in Cursor(self.api.user_timeline, id=self.user).items(num_tweets):
            userTweets.append(tweet)
        return userTweets

    def getFriendList(self, num_friends):
        friendList = []
        for friend in Cursor(self.twitter_client.friends, id=self.user).items(num_friends):
            friendList.append(friend)
        return friendList

    def getTimelineTweets(self, num_tweets):
        timelineTweets = []
        for tweet in Cursor(self.twitter_client.home_timeline, id=self.user).items(num_tweets):
            timelineTweets.append(tweet)
        return timelineTweets

    def tweet_image(self, url, message=""):

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

    # logger = plugin_api.getLogger()
    # config = plugin_api.config.secret.symmetrify
    # spec = importlib.util.spec_from_file_location("symmetry", os.path.join(os.path.dirname(os.path.abspath(__file__)), "symmetry.py"))
    # mod = importlib.util.module_from_spec(spec)
    # spec.loader.exec_module(mod)
    # sym = mod.Symmetry(api_key=config["cloudvision_key"], save_dir=plugin_api.dirs.cache, logger=logger)

    twitter_client = TwitterClient()
    tweet_analyzer = TweetAnalyzer()
    api = twitter_client.get_twitter_client_api()

    tweets = api.user_timeline(screen_name='GhibliQuotes', count=15, include_rts=False)

    df = tweet_analyzer.tweets_to_data_frame(tweets)
    #print(df.head(40))
    #print(dir(tweets[0]))

    media_files = []
    for status in tweets:
        media = status.entities.get('media', [])
        if(len(media) > 0):
            media_files.append(media[0]['media_url'])
            #media_files.append(media[0]['media_url_https'])
            #media_files.append(media[0]['media_id_string'])


    for i in media_files:
        print(i)
        twitter_client.tweet_image(i)

        #wget.download(i)


    #symmetrify = symmetry.Symmetry('nWPANwUxEQ3GtQpoyCnxhv084')
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


    #print(dir(tweets[0]))






    # hash_tag_list = ["ghibli", "coding", "python", "c++", "ssbu"]
    # fetched_tweets_filename = "tweets.txt"
    #
    # twitterStreamer = TwitterStreamer()
    # twitterStreamer.stream_tweets(fetched_tweets_filename, hash_tag_list)

"""
api = tweepy.API(auth)

user = api.get_user('hikakin')

mentions = api.mentions_timeline(count = 1) ##class status

if mentions:


print(user.screen_name)
print(user.followers_count)
"""


#def do(api, stream):
    #logger = api.getLogger()
    #config = api.config.secret.symmetrify
    #twitter = api.getTwitterAccount("symmetrify").getTweepyHandler(retry_count=5, retry_delay=10)
    #spec = importlib.util.spec_from_file_location("symmetry", os.path.join(os.path.dirname(os.path.abspath(__file__)), "symmetry.py"))
    #mod = importlib.util.module_from_spec(spec)
    #spec.loader.exec_module(mod)
    #sym = mod.Symmetry(api_key=config["cloudvision_key"], save_dir= api.dirs.cache, logger=logger)

    # if stream["user"]["screen_name"].lower() == "hikakin"
    #     result = stream.get("extended_entities", stream.get("entities", {})).get("media")
    #     if result is not None:
    #         logger.info("Twitter found a new image")
    #         for i in result:
    #             img_url = i.get("media_url_https")
    #
    #             if img_url is not None:
    #                 #sym_result = sym.do(img_url)
    #                 for c, n in enumerate(img_url):    #sym_result):
    #                     text = ""
    #                     media_ids = [api.media_upload(m).media_id_string for m in n]
    #                     api.update_status(status=text, media_ids=media_ids)
    #                 [[os.remove(m) for m in n if os.path.exists(m)] for n in sym_result]
    #
    #     else:
    #         logger.info("No image found!!!!!!")




#@PluginMeta(PluginType.TwitterTimeline, twitterAccount='')
#def do(plugin_api, stream):
#    logger = plugin_api.getLogger()
#    config = plugin_api.config.secret.###
#    twitter = plugin_api.getTwitterAccount('').getTweepyHandler()
