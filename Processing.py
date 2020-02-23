class Cleaner:

    def get_full_text(self, status):
        if hasattr(status, "retweeted_status"):  # Check if Retweet
            try:
                return status.retweeted_status.extended_tweet["full_text"]
            except AttributeError:
                return status.retweeted_status.text
        else:
            try:
                return status.extended_tweet["full_text"]
            except AttributeError:
                return status.text

    def clean_tweets():
        pass