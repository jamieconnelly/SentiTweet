from flask import Flask
import os
import pickle
import json

from sklearn.feature_extraction.text import TfidfVectorizer

from app.utils.pos_neg_idfs import pos_neg_idfs
from app.utils.obj_sub_idfs import obj_sub_idfs


SUB_OBJ_CLF = './app/sub_obj_clf'
SUB_OBJ_VOCAB = './app/sub_obj_vocab.json'
POS_NEG_CLF = './app/pos_neg_clf'
POS_NEG_VOCAB = './app/pos_neg_vocab.json'


def open_model(pickle_name, vocab_name):

    vocab = json.load(open(vocab_name, mode='rb'))

    with open(pickle_name, 'rb') as f:
        model = pickle.load(f)

    return model, vocab


sub_obj_clf, sub_obj_vocab = open_model(SUB_OBJ_CLF, SUB_OBJ_VOCAB)
pos_neg_clf, pos_neg_vocab = open_model(POS_NEG_CLF, POS_NEG_VOCAB)
_obj_sub_idfs = obj_sub_idfs
_pos_neg_idfs = pos_neg_idfs


def bootstrap():
    instance_path = os.path.abspath(os.path.join(__file__, os.pardir, "config"))
    app = Flask(__name__, instance_path=instance_path, instance_relative_config=True)

    load_app_config(app)

    from app.api import api as api_blueprint
    app.register_blueprint(api_blueprint)
    return app


def load_app_config(app):
    app.config.from_object("config.app.default")
    app.config.from_envvar("APP_CONFIG", silent=False)
    app.config["VERSION"] = os.environ.get("VERSION", "local")
    app.config["HOSTNAME"] = os.environ.get("HOSTNAME")
