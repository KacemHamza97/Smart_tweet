import re

from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import load_model
import pickle
import tweepy
from tweepy import OAuthHandler
from time import sleep
from google_trans_new import google_translator

from web_app import db


class Tweet:
    def __init__(self, id, text, tweet_url, media_url, date, type):
        self.id = id
        self.text = text
        self.tweet_url = tweet_url
        self.media_url = media_url
        self.date = date
        self.type = type

    def __str__(self):
        return f"tweet text:{self.text}\ntweet_url: {self.tweet_url}\nimage_url: {self.media_url}\n" \
               f"date: {self.date}\ntype: {self.type}"


# KERAS
SEQUENCE_LENGTH = 300
# SENTIMENT
SENTIMENT_THRESHOLDS = (0.4, 0.7)

tokenizer = Tokenizer()
with open('/home/hamza/Desktop/project/trained_models/tokenizer.pkl', 'rb') as f:
    tokenizer = pickle.load(f)


def predict(text):
    # Tokenize text
    x_test = pad_sequences(tokenizer.texts_to_sequences([text]), maxlen=SEQUENCE_LENGTH)
    # Predict
    score = model.predict([x_test])[0]
    # Decode sentiment
    if score <= SENTIMENT_THRESHOLDS[0]:
        return "NEGATIVE"
    elif score >= SENTIMENT_THRESHOLDS[1]:
        return "POSITIVE"
    else:
        return "NEUTRAL"


model = load_model('/home/hamza/Desktop/project/trained_models/model.h5')

translator = google_translator()
ACCESS_TOKEN = "241949174-J7mlaEePXSl59Ee7SUSWxJ7UX1pIunz6dTck9IaK"
ACCESS_TOKEN_SECRET = "KPGs3ZZBcSXRzwxNNOu1vSs0wxdTXPYmjb80O06AwhTmv"
CONSUMER_KEY = "SSip5qurDw27uvKcDbUZlp7Ub"
CONSUMER_SECRET = "gis20uRU4KJ4fpCHZrwYVSxl16DWsppC9dlMgLATYzOE0HYJBC"
auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)
tweets = set()
posts = db.posts
while True:
    for status in tweepy.Cursor(api.home_timeline, include_entities=True).items(50):
        if 'media' in status.entities:
            for media in status.extended_entities['media']:

                tweet_text = translator.translate(status._json["text"], lang_tgt='en')
                tweet_url = (re.search("(?P<url>https?://[^\s]+)", tweet_text).group("url"))
                tweet = Tweet(status._json["id"], tweet_text.replace(tweet_url, ''), tweet_url,
                              media['media_url'], status.created_at, predict(tweet_text))
                tweets.add(tweet)
                print(tweet)
                posts.insert(
                    {"id": tweet.id, "tweet_text": tweet.text, "tweet_url": tweet.tweet_url,
                     "media_url": tweet.media_url, "date": tweet.date, "type": tweet.type})
    sleep(10)
