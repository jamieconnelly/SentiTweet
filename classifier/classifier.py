import pickle
import json
import numpy as np
import pandas as p

from sklearn.linear_model import SGDClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report as clsr
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import confusion_matrix as cm
from SentiVis.sentiment_webservice.app.utils.preprocessor import Preprocessor
from SentiVis.sentiment_webservice.app.utils.feature_combiner import FeatureCombiner


def build_and_evaluate(X, y, X_test, y_test, outpath=None):

    def preprocess(s):
        return preprocessor.tokenise(s)

    # Initialise transformers/estimators
    # clf = MultinomialNB()
    # clf = SGDClassifier()
    clf = LogisticRegression(C=7)
    preprocessor = Preprocessor()
    feat_comb = FeatureCombiner()
    vec = TfidfVectorizer(tokenizer=preprocess,
                          lowercase=False,
                          ngram_range=(1, 2),
                          min_df=1,
                          max_df=0.8,
                          norm='l2')

    # Build model
    print("Building model")
    tfidf_matrix = vec.fit_transform(X)
    # feat_matrix = feat_comb.transform(tfidf_matrix.todense(),
    #                                   preprocessor)
    clf.fit(tfidf_matrix, y)

    # Evaluate on test set
    # preprocessor.reset_feats()
    tfidf_matrix = vec.transform(X_test)
    # feat_matrix = feat_comb.transform(tfidf_matrix.todense(),
    #                                   preprocessor)
    y_pred = clf.predict(tfidf_matrix)

    print("Classification Report:\n")
    print np.mean(y_pred == y_test)
    print cm(y_test, y_pred)
    print(clsr(y_test, y_pred, target_names=['neg', 'pos']))

    # Rebuild model and save with pickle
    print("Building complete model and saving...")
    # preprocessor.reset_feats()
    tfidf_matrix = vec.fit_transform(X)
    feat_matrix = feat_comb.transform(tfidf_matrix.todense(),
                                      preprocessor)
    clf.fit(feat_matrix, y)

    np.set_printoptions(threshold=np.nan)
    print repr(vec.idf_)

    if outpath:
        json.dump(vec.vocabulary_, open(outpath + 'vocabulary.json', mode='wb'))
        with open(outpath + 'model.pickle', 'wb') as f:
            pickle.dump(clf, f)
        print("Model written out to {}".format(outpath))

    return clf


if __name__ == "__main__":
    PATH = '../sentiment_webservice/app/'
    TRAIN_PATH = './data/train_raw.csv'
    TEST_PATH = './data/test_data1.csv'

    train = p.read_csv(TRAIN_PATH, usecols=(['class', 'text'])).dropna()
    test = p.read_csv(TEST_PATH, usecols=(['class', 'text'])).dropna()
    train = train.reindex(np.random.permutation(train.index))

    model = build_and_evaluate(train['text'].values,
                               train['class'].values,
                               test['text'].values,
                               test['class'].values,
                               outpath=PATH)
