from flask import Flask, jsonify, request, g
from tweepy import AppAuthHandler, Cursor, API
from utils.text_processor import NLTKPreprocessor

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


@app.route('/search', methods=['GET'])
def query_sentiment():
    try:
        term = request.args.getlist('term')
        api = get_twitter_api()
        preprocessor = NLTKPreprocessor()
        tweets = []
        for tweet in Cursor(api.search, q=term, lang='en').items(100):
            if (not tweet.retweeted) and ('RT' not in tweet.text):
                tokens = list(preprocessor.tokenize(tweet.text))
                tweets.append(tokens)
        return jsonify(result=tweets)

    except Exception as ex:
        app.logger.error(type(ex))
        app.logger.error(ex.args)
        return jsonify(error=str(ex))
