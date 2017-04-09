import pickle
import json
import numpy as np

from sklearn.metrics import classification_report as clsr
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import confusion_matrix as cm
from SentiVis.sentiment_webservice.app.utils.preprocessor import Preprocessor
from SentiVis.sentiment_webservice.app.utils.feature_combiner import FeatureCombiner


class Trainer():

    """docstring for Trainers"""
    def __init__(self, clf, n_gram, min_df, max_df, norm, lexicon_feats):
        self.preprocessor = Preprocessor()
        self.feat_comb = FeatureCombiner()
        self.lexicon_feats = lexicon_feats
        self.clf = clf
        self.tfidf_vec = TfidfVectorizer(tokenizer=self.preprocess,
                                         lowercase=False,
                                         ngram_range=n_gram,
                                         min_df=min_df,
                                         max_df=max_df,
                                         norm=norm)

    def preprocess(self, s):
        return self.preprocessor.tokenise(s, self.lexicon_feats)

    def build_model(self, X, y):

        print("Building model...")
        tfidf_matrix = self.tfidf_vec.fit_transform(X)

        if self.lexicon_feats:
            feat_matrix = self.feat_comb.transform(tfidf_matrix.todense(), self.preprocessor)
            self.clf.fit(feat_matrix, y)
        else:
            self.clf.fit(tfidf_matrix, y)

    def evaluate_model(self, X_test, y_test, labels=None):

        print("Evaluating model...")
        if self.lexicon_feats:
            self.preprocessor.reset_feats()
            tfidf_matrix = self.tfidf_vec.transform(X_test)
            feat_matrix = self.feat_comb.transform(tfidf_matrix.todense(), self.preprocessor)
            y_pred = self.clf.predict(feat_matrix)
        else:
            tfidf_matrix = self.tfidf_vec.transform(X_test)
            y_pred = self.clf.predict(tfidf_matrix)

        print "\nAccuracy: {}".format(np.mean(y_pred == y_test))
        print "Confusion matrix:\n {}".format(cm(y_test, y_pred))
        print "Classification Report:\n {}".format(clsr(y_test, y_pred, target_names=[labels[0], labels[1]]))

    def pickle_model(self, vocab_file_name, pickle_name, print_idf_=False, save=False):

        if save:
            json.dump(self.tfidf_vec.vocabulary_, open(vocab_file_name, mode='wb'))

            with open(pickle_name, 'wb') as f:
                pickle.dump(self.clf, f)

            print "Model written out to {}".format(pickle_name)
            print "Tfidf vocab written out to {}".format(vocab_file_name)

        if print_idf_:
            np.set_printoptions(threshold=np.nan)
            print "\n {}".format(repr(self.tfidf_vec.idf_))
