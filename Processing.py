from pymongo import MongoClient
from configparser import ConfigParser
import sys
import re


class ProgressBar:

    def __init__(self, items):
        self.width = 40
        self.interval_size = items / (self.width - 1)
        if self.interval_size == 0:
            self.interval_size = 1
        sys.stdout.write("[%s]" % (" " * self.width))
        sys.stdout.flush()
        sys.stdout.write("\b" * (self.width + 1))

    def run(self):
        for i in range(1, self.width+1):
            sys.stdout.write('-')
            sys.stdout.flush()
            yield int(i*self.interval_size)
        sys.stdout.write("]\n")


class Filter:

    def __init__(self):
        parser = ConfigParser()
        parser.read('config.ini')
        self.query_terms = list(parser.get('FILTER', 'filter_terms').split(','))
        mongoClient = MongoClient()
        self.dump_db = mongoClient.tweet_dump
        self.filter_db = mongoClient.tweets
    
    def get_full_text(self, status):
        if "retweeted_status" in status:  # Check if Retweet
            try:
                return status["retweeted_status"]["extended_tweet"]["full_text"]
            except KeyError:
                return status["retweeted_status"]["text"]
        else:
            try:
                return status["extended_tweet"]["full_text"]
            except KeyError:
                return status["text"]

    def filter_tweets(self):
        processed_count = 0
        for stop_index in ProgressBar(items=self.dump_db.tweets.count()).run():
            for tweet in self.dump_db.tweets.find():
                if processed_count == stop_index:
                    break
                # print(tweet)
                for term in self.query_terms:
                    tweet_text = self.get_full_text(tweet)
                    if re.search(term, tweet_text):
                        self.filter_db[term].insert_one(tweet)
                self.dump_db.tweets.delete_one({'_id': tweet['_id']})
                processed_count += 1