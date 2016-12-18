from flask import Flask, jsonify, request, g
from tweepy import AppAuthHandler, Cursor, API
from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer
import string, re

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')


def connect_twitter():
    consumer_key = app.config['CONSUMER_KEY']
    consumer_secret = app.config['CONSUMER_SECRET']
    auth = AppAuthHandler(consumer_key, consumer_secret)
    return API(auth, wait_on_rate_limit=True,
               wait_on_rate_limit_notify=True)


def get_twitter_api():
    if not hasattr(g, 'twitter_api'):
        g.twitter_api = connect_twitter()
    return g.twitter_api


def tweet_preprocessor(tweet):
    tknzr = TweetTokenizer(preserve_case=True,
                           reduce_len=True,
                           strip_handles=True)
    table = {ord(char): None for char in string.punctuation}
    stop_words = stopwords.words('english')
    remove_pun = tweet.translate(table)
    remove_url = re.sub(r'http\S+', '', remove_pun)
    return [w for w in tknzr.tokenize(remove_url) if w not in stop_words]


@app.route('/search', methods=['GET'])
def query_sentiment():
    try:
        term = request.args.getlist('term')
        api = get_twitter_api()
        tweets = []
        for tweet in Cursor(api.search, q=term, lang='en').items(100):
            if (not tweet.retweeted) and ('RT' not in tweet.text):
                tokens = tweet_preprocessor(tweet.text.lower())
                tweets.append(tokens)
        return jsonify(result=tweets)

    except Exception as ex:
        app.logger.error(type(ex))
        app.logger.error(ex.args)
        return jsonify(error=str(ex))
