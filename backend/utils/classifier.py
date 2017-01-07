import pickle
import numpy
import pandas as p

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import SGDClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report as clsr
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.cross_validation import train_test_split as tts
from utils.preprocessor import Preprocessor, identity


def build(X, y):
    model = Pipeline([('preprocessor', Preprocessor()),
                      ('vectorizer', CountVectorizer(tokenizer=identity,
                                                     ngram_range=(1, 2),
                                                     preprocessor=None,
                                                     lowercase=False)),
                      ('classifier', MultinomialNB())])
    model.fit(X, y)
    return model


def build_and_evaluate(X, y, outpath=None):

    # Label encode the targets
    labels_train = LabelEncoder()
    y = labels_train.fit_transform(y)

    # Begin evaluation
    print("Building for evaluation")
    X_train, X_test, y_train, y_test = tts(X, y, test_size=0.2)
    model = build(X_train, y_train)

    y_pred = model.predict(X_test)
    print("Classification Report:\n")
    print(clsr(y_test, y_pred, target_names=['neg', 'neut', 'pos']))

    print("Building complete model and saving...")
    model = build(X_train, y_train)
    model.labels_ = labels_train

    if outpath:
        with open(outpath, 'wb') as f:
            pickle.dump(model, f)
        print("Model written out to {}".format(outpath))

    return model


if __name__ == "__main__":
    PATH = "../model.pickle"
    TRAIN_PATH = '../data/training_data.csv'
    train = p.read_csv(TRAIN_PATH, usecols=(['class', 'text']), encoding='latin-1')
    train = train.reindex(numpy.random.permutation(train.index))
    model = build_and_evaluate(train['text'].values,
                               train['class'].values,
                               outpath=PATH)
