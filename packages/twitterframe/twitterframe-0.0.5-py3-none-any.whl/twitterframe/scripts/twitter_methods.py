'''
twitter-trends.py : uh
'''
#

from . import utils
import tweepy
import json
import csv
import os
from pathlib import Path
import logging

h = utils.hatching_chick
b = utils.baby_chick
p = utils.party
pidgeon = utils.pidgeon
w = utils.warning
check = utils.checkmark

config_path = utils.config_path

class TwitterWrapper(object):
    '''
    subclass of SetupAPI
    TwitterTrends class.
    Methods that I want to make in the future...:
    Get Twitter Trends by location
    Get top 10 Twitter Trends
    I guess just the get methods from the API, just as methods from this class...
    '''

    def __init__(self,
                 access_token,
                 access_secret,
                 consumer_key,
                 consumer_secret):
        self.access_token = access_token
        self.access_secret = access_secret
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret

    def setup(self):

        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token, self.access_secret)

        api = tweepy.API(auth)

        return api

    def verify_creds(self):

        api = self.setup()

        try:
            api.verify_credentials()
            print(check, 'Credentials have been verified!')
            print(pidgeon, 'Enjoy using twitterframe.')

       except:
            print(w*3, 'Credentials are not valid.')

    def get_timeline(self):
        '''
        https://tweepy.readthedocs.io/en/v3.5.0/api.html#API.home_timeline
        '''
        return [tweet.text for tweet in self.setup().home_timeline()]

    def get_user_tweets(self, username):
        '''
           Get tweets by username with the tweepy.API method --> user_timeline.
           This works.
        '''
        api = self.setup()

        tweets = []

        for tweet in tweepy.Cursor(api.user_timeline, id=username,
                                   ).items():

            tweets.append([username, tweet.id_str, tweet.created_at,
                           tweet.text.encode('utf-8')])

        print(pidgeon, 'Downloaded {} tweets from user: {}'.format(len(tweets), username))

        return tweets

    def crawl(self, hashtag, count):
        '''
            Crawl method for hashtags.
            This may not work yet lol.
            Will push to pypi.org when this is done.
            since='{}'.format(time) <-- removed this from api.search.
        '''
        api = self.setup()

        tweets = []

        try:

            for tweet in tweepy.Cursor(api.search, q='{}'.format(hashtag),
                                       count=count, lang='en',
                                       ).items():

                tweets.append([hashtag, tweet.id_str, tweet.created_at,
                               tweet.text.encode('utf-8')])

        except tweepy.error.RateLimitError:

            print(w*3, "Reached Twitter rate limit. Ending loop.")

        print(pidgeon, '{} Downloaded tweets, with the hashtag {} !'.format(len(tweets),hashtag))

        return tweets




