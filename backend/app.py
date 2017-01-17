from __future__ import division
from flask import Flask, jsonify, request, g
from tweepy import AppAuthHandler, Cursor, API
from utils.predict import predict

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


def calculate_percent(label):
    if label == 0:
        return 0
    return round(((label / 50) * 100), 2)


@app.route('/', methods=['GET'])
def home():
    return 'welcome'


@app.route('/search', methods=['GET'])
def query_sentiment():
    try:
        term = request.args.getlist('term')
        api = get_twitter_api()
        response = {'tweets': [], 'pos': 0, 'neg': 0}
        pos, neg = 0, 0

        for tweet in Cursor(api.search, q=term, lang='en').items(50):
            response['tweets'].append(tweet.text)
            pred = predict([tweet.text])
            if pred == [0]:
                neg += 1
            else:
                pos += 1

        response['neg'] = calculate_percent(neg)
        response['pos'] = calculate_percent(pos)

        return jsonify(**response)

    except Exception as ex:
        app.logger.error(type(ex))
        app.logger.error(ex.args)
        return jsonify(error=str(ex))
