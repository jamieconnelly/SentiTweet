from __future__ import division
from app.api import api
from flask import jsonify, request, g
from flask import current_app as app
from tweepy import AppAuthHandler, Cursor, API
from app.utils.predict import predict


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


@api.route('/', methods=['GET'])
def home():
    return 'welcome'


@api.route('/search', methods=['GET'])
def query_sentiment():
    try:
        term = request.args.getlist('term')
        api = get_twitter_api()
        res = {'tweets': [], 'pos': 0, 'neg': 0, 'neut': 0}
        pos, neg, neut = 0, 0, 0

        for tweet in Cursor(api.search, q=term, lang='en').items(50):
            pred = predict([tweet.text])
            res['tweets'].append({'text': tweet.text,
                                  'location': tweet.user.location})
            if pred == [0]:
                neg += 1
            elif pred == [2]:
                neut += 1
            else:
                pos += 1

        res['neg'] = calculate_percent(neg)
        res['pos'] = calculate_percent(pos)
        res['neut'] = calculate_percent(neut)

        return jsonify(**res)

    except Exception as ex:
        app.logger.error(type(ex))
        app.logger.error(ex.args)
        return jsonify(error=str(ex))
