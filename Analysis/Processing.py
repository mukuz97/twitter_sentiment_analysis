import re
import preprocessor as p
from bs4 import BeautifulSoup

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

def extract_tweet_data(status):
    data = []
    data.append(get_full_text(status))
    data.append(int(status['timestamp_ms'])/1000)
    data.append(status['user']['screen_name'])
    data.append(get_tweet_source(status))
    data.append(status['id_str'])
    data.append(status['user']['location']) # User location is useless
    data.append(extract_source_device(status['source']))
    return data


# Don't remove hastags
p.set_options(p.OPT.URL, p.OPT.EMOJI, p.OPT.NUMBER, p.OPT.SMILEY, p.OPT.RESERVED, p.OPT.MENTION)

NOT_BASIC_LATIN_PATTERN = re.compile(u'[^\u0000-\u007F]')
PUNCTUATIONS_PATTERN = re.compile(r'[\#\$\%\&\(\)\*\+\-\/\:\;\<\=\>\@\[\\\]\^\_\`\{\|\}\~]')
MULTIPLE_SPACES_PATTERN = re.compile(r' +')

def clean_text(text):
    text = text.lower()
    text = p.clean(text) # Clean using tweet-preprocessor except hashtags
    text = NOT_BASIC_LATIN_PATTERN.sub(' ', text) # Remove everything except basic latin
    text = re.sub(r'&amp;', 'and', text)
    text = PUNCTUATIONS_PATTERN.sub(' ', text) # Remove all punctuations
    text = MULTIPLE_SPACES_PATTERN.sub(' ', text) # Remove multiple consequent spaces
    return text.strip()

def is_retweet(x):
    return x[0] != x[1]