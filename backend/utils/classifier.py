import time
import pickle

from nltk.corpus import twitter_samples

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
def build_and_evaluate(X, y, classifier=SGDClassifier, outpath=None, verbose=True):
    """
    X: a list or iterable of raw strings, each representing a document.
    y: a list or iterable of labels, which will be label encoded.
    Can specify the classifier to build with: if a class is specified then
    this will build the model with the Scikit-Learn defaults, if an instance
    is given, then it will be used directly in the build pipeline.
    If outpath is given, this function will write the model as a pickle.
    If verbose, this function will print out information to the command line.
    """

    @timeit
    def build(classifier, X, y=None):

        if isinstance(classifier, type):
            # classifier = classifier(loss='hinge', penalty='l2',
            #                         alpha=1e-3, n_iter=5, random_state=42)
            classifier = classifier()

        model = Pipeline([
            ('preprocessor', Preprocessor()),
            ('vectorizer', CountVectorizer(tokenizer=identity, ngram_range=(1, 2), preprocessor=None, lowercase=False)),
            ('classifier', classifier),
        ])

        model.fit(X, y)
        return model

    # Label encode the targets
    labels = LabelEncoder()
    y = labels.fit_transform(y)

    # Begin evaluation
    if verbose: print("Building for evaluation")
    X_train, X_test, y_train, y_test = tts(X, y, test_size=0.2)
    model, secs = build(classifier, X_train, y_train)

    if verbose: print("Evaluation model fit in {:0.3f} seconds".format(secs))
    if verbose: print("Classification Report:\n")

    y_pred = model.predict(X_test)
    print(clsr(y_test, y_pred, target_names=labels.classes_))

    if verbose: print("Building complete model and saving ...")
    model, secs = build(classifier, X, y)
    model.labels_ = labels

    if verbose: print("Complete model fit in {:0.3f} seconds".format(secs))

    if outpath:
        with open(outpath, 'wb') as f:
            pickle.dump(model, f)

        print("Model written out to {}".format(outpath))

    return model


if __name__ == "__main__":
    PATH = "../model.pickle"

    X = []
    y = []
    for text in twitter_samples.strings('negative_tweets.json'):
        X.append(text.encode("utf-8"))
        y.append('neg')

    for text in twitter_samples.strings('positive_tweets.json'):
        X.append(text.encode("utf-8"))
        y.append('pos')

    model = build_and_evaluate(X, y, outpath=PATH)
