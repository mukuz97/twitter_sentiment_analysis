import tweepy
from pymongo import MongoClient
from datetime import datetime
from configparser import ConfigParser

class TwitterStreamListener(tweepy.StreamListener):

    def __init__(self):
        mongoClient = MongoClient()
        self.db = mongoClient.tweet_dump
        super(TwitterStreamListener, self).__init__()

    def on_status(self, status):
        self.db.tweets.insert_one(status._json)

    def on_error(self, status_code):
        print("Status Code: ", status_code)
        return False

    def on_exception(self, exception):
        print(datetime.now(), " Exception: ", exception)
        return


class Dumper:

    def __init__(self):
        parser = ConfigParser()
        parser.read('config.ini')
        consumer_key = parser.get('KEYS', 'consumer_key')
        consumer_secret = parser.get('KEYS', 'consumer_secret')
        access_token = parser.get('KEYS', 'access_token')
        access_token_secret = parser.get('KEYS', 'access_token_secret')
        self.query_terms = list(parser.get('FILTER', 'filter_terms').split(','))

        self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(access_token, access_token_secret)

    def start_dump(self):
        twitterStreamListener = TwitterStreamListener()
        twitter_stream = tweepy.Stream(auth = self.auth, listener = twitterStreamListener)
        twitter_stream.filter(track = self.query_terms, languages=["en"], is_async=True)
        print('Dumping Tweets...')
        print('Use Ctrl+C to stop')