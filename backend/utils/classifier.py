import pickle
import numpy
import pandas as p

from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import SGDClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report as clsr
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics import confusion_matrix as cm
from utils.preprocessor import Preprocessor


class FeatureCombiner(object):

    def transform(self, X, caps_feat):
        return numpy.c_[ X, numpy.array(caps_feat) ]

    def fit(self, X, y=None):
        return self


def build_and_evaluate(X, y, X_test, y_test, outpath=None):

    def preprocess(s):
        return preprocessor.token(s)

    # Label encode the targets
    labels_train = LabelEncoder()
    y = labels_train.fit_transform(y)
    labels_test = LabelEncoder()
    y_test = labels_test.fit_transform(y_test)

    # Initialise transformers/estimators
    preprocessor = Preprocessor()
    clf = LogisticRegression()
    feat_comb = FeatureCombiner()
    vec = TfidfVectorizer(tokenizer=preprocess,
                          lowercase=False,
                          ngram_range=(1, 1),
                          max_features=10000)

    # Build model
    print("Building model")
    tfidf_matrix = vec.fit_transform(X)
    feat_matrix = feat_comb.transform(tfidf_matrix.todense(),
                                      preprocessor.micro_feats['caps'])
    clf.fit(feat_matrix, y)

    # Evaluate on test set
    preprocessor.reset_feats()
    tfidf_matrix = vec.transform(X_test)
    feat_matrix = feat_comb.transform(tfidf_matrix.todense(),
                                      preprocessor.micro_feats['caps'])
    y_pred = clf.predict(feat_matrix)

    print("Classification Report:\n")
    print numpy.mean(y_pred == y_test)
    print cm(y_test, y_pred)
    print(clsr(y_test, y_pred, target_names=['neg', 'neut', 'pos']))

    # Rebuild model and save with pickle
    print("Building complete model and saving...")
    preprocessor.reset_feats()
    tfidf_matrix = vec.transform(X)
    feat_matrix = feat_comb.transform(tfidf_matrix.todense(),
                                      preprocessor.micro_feats['caps'])
    clf.fit(feat_matrix, y)
    clf.labels_ = labels_train

    if outpath:
        with open(outpath, 'wb') as f:
            pickle.dump(clf, f)
        print("Model written out to {}".format(outpath))

    return clf


if __name__ == "__main__":
    PATH = "../model.pickle"
    TRAIN_PATH = '../data/training_data.csv'
    TEST_PATH = '../data/test_data.csv'

    train = p.read_csv(TRAIN_PATH, usecols=(['class', 'text']))
    test = p.read_csv(TEST_PATH, usecols=(['class', 'text']))
    train = train.reindex(numpy.random.permutation(train.index))

    model = build_and_evaluate(train['text'].values,
                               train['class'].values,
                               test['text'].values,
                               test['class'].values,
                               outpath=PATH)
