import tweepy
from pymongo import MongoClient
from configparser import ConfigParser

import preprocessor as p

class Authentication:

    def __init__(self):
        parser = ConfigParser()
        parser.read('config.ini')
        consumer_key = parser.get('KEYS', 'consumer_key')
        consumer_secret = parser.get('KEYS', 'consumer_secret')
        access_token = parser.get('KEYS', 'access_token')
        access_token_secret = parser.get('KEYS', 'access_token_secret')

        self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(access_token, access_token_secret)