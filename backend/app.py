from flask import Flask, jsonify, request, g
from tweepy import OAuthHandler
import tweepy

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')

consumer_key = app.config['CONSUMER_KEY']
consumer_secret = app.config['CONSUMER_SECRET']
access_token = app.config['ACCESS_TOKEN']
access_secret = app.config['ACCESS_SECRET']


def connect_twitter():
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    return tweepy.API(auth)


def get_twitter_api():
    if not hasattr(g, 'twitter_api'):
        g.twitter_api = connect_twitter()
    return g.twitter_api


@app.route('/search', methods=['GET'])
def query_sentiment():
    try:
        api = get_twitter_api()
        term = request.args.getlist('term')
        return jsonify(result=term)

    except Exception as ex:
        app.logger.error(type(ex))
        app.logger.error(ex.args)
        app.logger.error(ex)
        return jsonify(error=str(ex))
