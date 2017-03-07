from __future__ import division
from app.api import api
from flask import jsonify, request, g
from flask import current_app as app
from tweepy import AppAuthHandler, Cursor, API
from app.utils.predict import predict


import googlemaps
import os

def get_maps_api():
    if not hasattr(g, 'maps_api'):
        g.maps_api = connect_maps()
    return g.maps_api


def connect_maps():
    key = app.config['GOOGLE_KEY']
    return googlemaps.Client(key=key)


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


def calculate_percent(val, num):
    if val == 0:
        return 0
    return round(((val / num) * 100), 2)


def get_lat_lng(city):
    try:
        maps_api = get_maps_api()
        result = maps_api.geocode(city.encode('utf8'))
        if not result:
            return []
        lat_lng = result[0]['geometry']['location']
        return [lat_lng['lat'], lat_lng['lng']]
    except googlemaps.exceptions.HTTPError:
        return []


@api.route('/', methods=['GET'])
def home():
    return 'welcome'


@api.route('/search', methods=['GET'])
def query_sentiment():
    try:
        term = request.args.getlist('term')
        twitter_api = get_twitter_api()
        res = {'tweets': [], 'pos': 0, 'neg': 0, 'neut': 0}
        pos, neg, neut = 0, 0, 0
        tweets = Cursor(twitter_api.search, q=term, lang='en').items(30)

        for tweet in tweets:
            pred = predict([tweet.text])
            if pred == [0]:
                neg += 1
            elif pred == [2]:
                neut += 1
            else:
                pos += 1
            lat_lng = get_lat_lng(tweet.user.location)
            res['tweets'].append({'id': tweet.id,
                                  'text': tweet.text,
                                  'location': lat_lng,
                                  'polarity': pred[0]})

        res['neg'] = calculate_percent(neg, len(res['tweets']))
        res['pos'] = calculate_percent(pos, len(res['tweets']))
        res['neut'] = calculate_percent(neut, len(res['tweets']))

        return jsonify(**res)

    except Exception as ex:
        app.logger.error(type(ex))
        app.logger.error(ex.args)
        app.logger.error(ex)
        return jsonify(error=str(ex))
