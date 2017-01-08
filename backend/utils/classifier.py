import time
import pickle
import numpy
import pandas as p

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import classification_report as clsr
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.cross_validation import train_test_split as tts
from utils.preprocessor import Preprocessor, identity


def timeit(func):
    def wrapper(*args, **kwargs):
        start  = time.time()
        result = func(*args, **kwargs)
        delta  = time.time() - start
        return result, delta
    return wrapper


@timeit
def build_and_evaluate(X, y,
                       classifier=SGDClassifier, outpath=None):
# def build_and_evaluate(X_train, y_train, X_test, y_test,
#                        classifier=SGDClassifier, outpath=None):

    @timeit
    def build(classifier, X, y):

        if isinstance(classifier, type):
            classifier = classifier()

        model = Pipeline([
            ('preprocessor', Preprocessor()),
            ('vectorizer', CountVectorizer(tokenizer=identity, ngram_range=(1, 2), preprocessor=None, lowercase=False)),
            ('classifier', classifier),
        ])

        model.fit(X, y)
        return model

    # Label encode the targets
    labels_train = LabelEncoder()
    y = labels_train.fit_transform(y)
    # labels_test = LabelEncoder()
    # y_test = labels_test.fit_transform(y_test)

    # Begin evaluation
    print("Building for evaluation")
    X_train, X_test, y_train, y_test = tts(X, y, test_size=0.2)
    model, secs = build(classifier, X_train, y_train)
    print("Evaluation model fit in {:0.3f} seconds".format(secs))

    y_pred = model.predict(X_test)
    print("Classification Report:\n")
    print(clsr(y_test, y_pred, target_names=['neg', 'neut', 'pos']))

    print("Building complete model and saving...")
    model, secs = build(classifier, X_train, y_train)
    model.labels_ = labels_train

    print("Complete model fit in {:0.3f} seconds".format(secs))

    if outpath:
        with open(outpath, 'wb') as f:
            pickle.dump(model, f)
        print("Model written out to {}".format(outpath))

    return model


if __name__ == "__main__":
    PATH = "../model.pickle"
    TRAIN_PATH = '../data/training_data.csv'
    TEST_PATH = '../data/test_data.csv'

    train = p.read_csv(TRAIN_PATH, usecols=(['class', 'text']), encoding='latin-1')
    test = p.read_csv(TEST_PATH, usecols=(['class', 'text']), encoding='latin-1')
    train = train.reindex(numpy.random.permutation(train.index))
    model = build_and_evaluate(train['text'].values,
                               train['class'].values,
                               outpath=PATH)
    # model = build_and_evaluate(train['text'].values,
    #                            train['class'].values,
    #                            test['text'].values,
    #                            test['class'].values,
    #                            outpath=PATH)
