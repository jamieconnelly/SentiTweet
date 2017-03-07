import pickle
import json
import scipy.sparse as sp

from flask import current_app as app
from sklearn.feature_extraction.text import TfidfVectorizer
from app.utils.preprocessor import Preprocessor
from app.utils.feature_combiner import FeatureCombiner
from app.bootstrap import sub_obj_clf, sub_obj_vocab, pos_neg_clf, pos_neg_vocab, _obj_sub_idfs, _pos_neg_idfs


class Obj_Sub_Vectorizer(TfidfVectorizer):
    TfidfVectorizer.idf_ = _obj_sub_idfs


class Pos_Neg_Vectorizer(TfidfVectorizer):
    TfidfVectorizer.idf_ = _pos_neg_idfs


def get_vectorisor(preprocess, vocabulary, obj_vs_sub):

    if obj_vs_sub:
        vec = Obj_Sub_Vectorizer(tokenizer=preprocess,
                                 lowercase=False,
                                 min_df=1,
                                 max_df=0.8,
                                 ngram_range=(1, 1),
                                 norm='l2')
        vec._tfidf._idf_diag = sp.spdiags(_obj_sub_idfs,
                                          diags=0,
                                          m=len(_obj_sub_idfs),
                                          n=len(_obj_sub_idfs))
    else:
        vec = Pos_Neg_Vectorizer(tokenizer=preprocess,
                                 lowercase=False,
                                 min_df=1,
                                 max_df=0.8,
                                 ngram_range=(1, 2),
                                 norm='l2')
        vec._tfidf._idf_diag = sp.spdiags(_pos_neg_idfs,
                                          diags=0,
                                          m=len(_pos_neg_idfs),
                                          n=len(_pos_neg_idfs))

    vec.vocabulary_ = vocabulary
    return vec


def get_prediction(tweet, obj_vs_sub, clf, vocab):

    def preprocess(s):
        if obj_vs_sub:
            return preprocessor.tokenise(s, True)
        else:
            return preprocessor.tokenise(s, False)

    preprocessor = Preprocessor()

    vec = get_vectorisor(preprocess, vocab, obj_vs_sub)
    tfidf_matrix = vec.transform(tweet)

    if not obj_vs_sub:
        return clf.predict(tfidf_matrix)

    feat_comb = FeatureCombiner()
    feat_matrix = feat_comb.transform(tfidf_matrix.todense(), preprocessor)
    return clf.predict(feat_matrix)


def predict(tweet):

    # Objective vs Subjective clf
    y_pred = get_prediction(tweet, True, sub_obj_clf, sub_obj_vocab)
    if y_pred.tolist() == [0]:
        return [2]

    # Positive vs Negative clf
    y_pred = get_prediction(tweet, False, pos_neg_clf, pos_neg_vocab)
    return y_pred.tolist()
