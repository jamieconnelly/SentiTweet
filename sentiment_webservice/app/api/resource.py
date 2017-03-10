from __future__ import division
from app.api import api
from flask import jsonify, request, g
from flask import current_app as app
from tweepy import AppAuthHandler, Cursor, API
from app.utils.predictor import predict

import googlemaps


def get_maps_api():
    """Retrieve or instantiate googlemaps api client.
        Returns:
            googlemaps object.
    """
    if not hasattr(g, 'maps_api'):
        g.maps_api = instantiate_google_maps()
    return g.maps_api


def instantiate_google_maps():
    """Instantiates googlemaps api client.
        Returns:
            googlemaps object.
    """
    key = app.config['GOOGLE_KEY']
    return googlemaps.Client(key=key)


def instantiate_twitter():
    """Instantiates tweepy client.
        Returns:
            tweepy object.
    """
    consumer_key = app.config['CONSUMER_KEY']
    consumer_secret = app.config['CONSUMER_SECRET']
    auth = AppAuthHandler(consumer_key, consumer_secret)
    return API(auth, wait_on_rate_limit=True,
               wait_on_rate_limit_notify=True)


def get_twitter_api():
    """Retrieve or instantiate tweepy client.
        Returns:
            tweepy object.
    """
    if not hasattr(g, 'twitter_api'):
        g.twitter_api = instantiate_twitter()
    return g.twitter_api


def calculate_percent(samples, total_number):
    """Calculate percentages.

        Args:
            samples (int): Text of a tweet.
            total_number (int): Total no. of tweets

        Returns:
            float.
    """
    if samples == 0:
        return 0
    return round(((samples / total_number) * 100), 2)


def get_lat_lng(city):
    """Converts city name into latitude and longitude coordinates.

        Args:
            city (str): City name as a string.

        Returns:
            list containing latitude and longitude.
    """
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
    return 'Welocme...'

@api.route('/search', methods=['GET'])
def query_sentiment():
    """Accepts search term to query twitter for tweets to then classify
       their sentiment.

        Returns:
            {
                'tweets': list of dictionaries containing tweet details,
                'pos': float score for positive sentiment percentage,
                'neg': float score for negative sentiment percentage,,
                'neut': float score for neutral sentiment percentage,
            }
    """
    try:
        term = request.args.getlist('term')
        twitter_api = get_twitter_api()
        response = {'tweets': [], 'pos': 0, 'neg': 0, 'neut': 0}
        pos, neg, neut = 0, 0, 0
        tweets = Cursor(twitter_api.search, q=term, lang='en').items(50)
        print 'collected tweets...'
        for tweet in tweets:
            # Ignore retweets
            if tweet.retweeted or 'RT' in tweet.text:
                continue

            # Classify tweet sentiment
            prediction = predict([tweet.text])
            if prediction == [0]:
                neg += 1
            elif prediction == [2]:
                neut += 1
            else:
                pos += 1
            
            print 'predicted ' + str(prediction)

            # Attempt to find tweet location
            if tweet.coordinates:
                lat_lng = tweet.coordinates
            else:
                lat_lng = get_lat_lng(tweet.user.location)

            response['tweets'].append({'id': tweet.id,
                                       'text': tweet.text,
                                       'location': lat_lng,
                                       'polarity': prediction[0]})

        # Calculate percentages
        no_of_tweets = len(response['tweets'])
        response['neg'] = calculate_percent(neg, no_of_tweets)
        response['pos'] = calculate_percent(pos, no_of_tweets)
        response['neut'] = calculate_percent(neut, no_of_tweets)

        return jsonify(**response)

    except Exception as ex:
        app.logger.error(type(ex))
        app.logger.error(ex.args)
        app.logger.error(ex)
        return jsonify(error=str(ex))
