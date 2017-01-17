import pickle
import json
import scipy.sparse as sp

from sklearn.feature_extraction.text import TfidfVectorizer
from utils.preprocessor import Preprocessor
from utils.feature_combiner import FeatureCombiner
from idfs import idfs


class MyVectorizer(TfidfVectorizer):
    TfidfVectorizer.idf_ = idfs


def open_model():
    model = None
    vocab = json.load(open('vocabulary.json', mode='rb'))

    with open('model.pickle', 'rb') as f:
        model = pickle.load(f)

    return model, vocab


def get_vec(preprocess, vocabulary):
    vec = MyVectorizer(tokenizer=preprocess,
                       lowercase=False,
                       ngram_range=(1, 1),
                       max_features=5000,
                       norm='l2')
    vec._tfidf._idf_diag = sp.spdiags(idfs, diags=0, m=len(idfs), n=len(idfs))
    vec.vocabulary_ = vocabulary
    return vec


def predict(tweets):
    def preprocess(s):
        return preprocessor.tokenise(s)

    model, vocabulary = open_model()
    preprocessor = Preprocessor()
    feat_comb = FeatureCombiner()
    vec = get_vec(preprocess, vocabulary)

    tfidf_matrix = vec.transform(tweets)
    feat_matrix = feat_comb.transform(tfidf_matrix.todense(),
                                      preprocessor)
    y_pred = model.predict(feat_matrix)
    return y_pred.tolist()
