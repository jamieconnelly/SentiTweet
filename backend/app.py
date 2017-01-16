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


@app.route('/', methods=['GET'])
def home():
    return 'welcome'


@app.route('/search', methods=['GET'])
def query_sentiment():
    try:
        term = request.args.getlist('term')
        api = get_twitter_api()
        response = {'tweets': [], 'pos': [], 'neg': 0, 'neut': 0}

        for tweet in Cursor(api.search, q=term, lang='en').items(50):
            response['tweets'].append(tweet.text)

        return jsonify(**response)

    except Exception as ex:
        app.logger.error(type(ex))
        app.logger.error(ex.args)
        return jsonify(error=str(ex))
