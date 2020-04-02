import numpy as np
import pandas as pd
import csv
from pymongo import MongoClient
from configparser import ConfigParser
from bs4 import BeautifulSoup

mongoClient = MongoClient()
db = mongoClient.tweets

parser = ConfigParser()
parser.read('config.ini')
query_terms = list(parser.get('FILTER', 'filter_terms').split(','))

cols = ['text','timestamp','user','tweet_source','tweet_id','user_location','source_device','company']


def get_full_text(status):
    if "retweeted_status" in status: # Check if Retweet
        try:
            return status["retweeted_status"]["extended_tweet"]["full_text"]
        except KeyError:
            return status["retweeted_status"]["text"]
    else:
        try:
            return status["extended_tweet"]["full_text"]
        except KeyError:
            return status["text"]

def get_tweet_source(status):
    if "retweeted_status" in status:
        return status["retweeted_status"]['id_str']
    else:
        return status['id_str']

def extract_source_device(html_data):
    soup = BeautifulSoup(html_data, 'html.parser')
    return soup.text

def get_row(status, company):
    data = []
    data.append(str(get_full_text(status)))
    data.append(int(int(status['timestamp_ms'])/1000))
    data.append(str(status['user']['screen_name']))
    data.append(str(get_tweet_source(status)))
    data.append(str(status['id_str']))
    data.append(str(status['user']['location']))
    data.append(str(extract_source_device(status['source'])))
    data.append(str(company))
    return data

def create_csv():
    with open('data/data.csv', 'w', encoding='utf-8') as file:
        csvwriter = csv.writer(file)
        csvwriter.writerow(cols)
        for term in query_terms:
            for tweet in db[term].find():
                if tweet['lang'] == 'en':
                    csvwriter.writerow(get_row(tweet, term))
            print('Done for ' + term)