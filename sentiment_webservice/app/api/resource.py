from __future__ import division

import app.utils.regex as r
import htmlentitydefs

import googlemaps

from flask import jsonify, request, g
from flask import current_app as app
from tweepy import AppAuthHandler, Cursor, API

from app.api import api
from app.utils.predictor import predict


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


def html2unicode(s):
    """ This method is courtesy of Christopher Potts
        http://sentiment.christopherpotts.net/index.html
        Internal method that seeks to replace all the HTML
        entities with their corresponding unicode characters.
    """
    # First the digits:
    ents = set(r.html_entity_digit_re.findall(s))
    if len(ents) > 0:
        for ent in ents:
            entnum = ent[2:-1]
            try:
                entnum = int(entnum)
                s = s.replace(ent, unichr(entnum))
            except:
                pass
    # Now the alpha versions:
    ents = set(r.html_entity_alpha_re.findall(s))
    ents = filter((lambda x: x != r.amp), ents)
    for ent in ents:
        entname = ent[1:-1]
        try:
            s = s.replace(ent,
                          unichr(htmlentitydefs.name2codepoint[entname]))
        except:
            pass
        s = s.replace(r.amp, " and ")
    return s


@api.route('/', methods=['GET'])
def home():
    return 'Welcome...'


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
        tweets = Cursor(twitter_api.search, q=term, lang='en').items(100)

        print 'collected tweets...'
        for tweet in tweets:
            # Ignore retweets
            if tweet.retweeted or 'RT' in tweet.text:
                continue

            # Convert html characters to unicode
            tweet_text = html2unicode(tweet.text)

            # Classify tweet sentiment
            prediction = predict([tweet_text])
            if prediction == [0]:
                neg += 1
            elif prediction == [2]:
                neut += 1
            else:
                pos += 1

            # Attempt to find tweet location
            if tweet.coordinates:
                lat_lng = tweet.coordinates
            else:
                lat_lng = get_lat_lng(tweet.user.location)

            response['tweets'].append({'id': tweet.id,
                                       'text': tweet_text,
                                       'location': lat_lng,
                                       'polarity': prediction[0]})

        # Calculate percentages
        print 'calculating percentages...'
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
