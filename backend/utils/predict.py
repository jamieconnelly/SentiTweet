import pickle
from utils.preprocessor import Preprocessor, identity


def open_model():
    model = None
    with open('model.pickle', 'rb') as f:
        model = pickle.load(f)
    return model


def predict(tweets):
    model = open_model()
    vectorizer = model.named_steps['vectorizer']
    classifier = model.named_steps['classifier']
    X_new = vectorizer.transform(tweets)
    X_new_preds = classifier.predict(X_new)
    return X_new_preds.tolist()
