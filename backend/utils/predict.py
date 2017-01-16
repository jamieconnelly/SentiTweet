import pickle

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from utils.preprocessor import Preprocessor
from utils.feature_combiner import FeatureCombiner


def open_model():
    model = None
    with open('model.pickle', 'rb') as f:
        model = pickle.load(f)
    return model


def predict(tweets):

    def preprocess(s):
        return preprocessor.tokenise(s)

    model = open_model()
    preprocessor = Preprocessor()
    feat_comb = FeatureCombiner()
    vec = TfidfVectorizer(tokenizer=preprocess,
                          lowercase=False,
                          ngram_range=(1, 1),
                          max_features=5000)
    
    tfidf_matrix = vec.transform(tweets)
    feat_matrix = feat_comb.transform(tfidf_matrix.todense(),
                                      preprocessor)
    X_new_preds = model.predict(feat_matrix)
    return X_new_preds.tolist()
