import sys
import numpy as np
import pandas as p
import argparse

from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from trainers import Trainer


def objective_vs_subjective(print_tfidf=False, save=False):
    """Objective vs Subjective tweet trainer."""
    # Variables for subjective vs objective classifier
    OBJ_SUB_VOCAB_FILE = PATH + 'sub_obj_vocab.json'
    CLF_PCKL_NAME = PATH + 'sub_obj_clf'
    LABELS = ['objecitve', 'subjective']
    obj_sub_train = p.read_csv('./sub_obj_data/train_new.csv', usecols=(['class', 'text'])).dropna()
    obj_sub_test = p.read_csv('./sub_obj_data/test_ds.csv', usecols=(['class', 'text'])).dropna()
    obj_sub_train = obj_sub_train.reindex(np.random.permutation(obj_sub_train.index))

    # initialise classifier
    clf = MultinomialNB(alpha=0.9)
    n_gram = (1, 1)
    min_df = 1
    max_df = 0.8
    norm = 'l2'
    ob_sub_trainer = Trainer(clf, n_gram, min_df, max_df, norm, True)

    # build model
    ob_sub_trainer.build_model(obj_sub_train['text'].values,
                               obj_sub_train['class'].values)

    # evaluate model
    ob_sub_trainer.evaluate_model(obj_sub_test['text'].values,
                                  obj_sub_test['class'].values,
                                  labels=LABELS)

    # Save model with pickle
    ob_sub_trainer.pickle_model(OBJ_SUB_VOCAB_FILE, CLF_PCKL_NAME, print_idf_=print_tfidf, save=save)


def positive_vs_negative(print_tfidf=False, save=False):
    """Positive vs Negative tweet trainer."""
    # Variables for positive vs negative classifier
    POS_NEG_VOCAB_FILE = PATH + 'pos_neg_vocab.json'
    CLF_PCKL_NAME = PATH + 'pos_neg_clf'
    LABELS = ['negative', 'positive']
    pos_neg_train = p.read_csv('./data/train_raw.csv', usecols=(['class', 'text'])).dropna()
    pos_neg_test = p.read_csv('./data/test_data1.csv', usecols=(['class', 'text'])).dropna()
    pos_neg_train = pos_neg_train.reindex(np.random.permutation(pos_neg_train.index))

    # initialise classifier
    clf = LogisticRegression(C=7)
    n_gram = (1, 2)
    min_df = 1
    max_df = 0.8
    norm = 'l2'

    pos_neg_trainer = Trainer(clf, n_gram, min_df, max_df, norm, False)

    # build model
    pos_neg_trainer.build_model(pos_neg_train['text'].values,
                                pos_neg_train['class'].values)

    # evaluate model
    pos_neg_trainer.evaluate_model(pos_neg_test['text'].values,
                                   pos_neg_test['class'].values,
                                   labels=LABELS)

    # Save model with pickle
    pos_neg_trainer.pickle_model(POS_NEG_VOCAB_FILE, CLF_PCKL_NAME, print_idf_=print_tfidf, save=save)


if __name__ == "__main__":

    PATH = '../sentiment_webservice/app/'
    print_tfidf = False
    save = False

    parser = argparse.ArgumentParser(description='Train sentiment classifiers.')
    parser.add_argument('-o', '--obj-sub', help='train objective vs subjective classifier', action='store_true')
    parser.add_argument('-p', '--pos-neg', help='train positive vs negative classifier', action='store_true')
    parser.add_argument('-t', '--tfidf', help='print tfidf matrix', action='store_true')
    parser.add_argument('-s', '--save', help='save vocabulary and model', action='store_true')
    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    if args.tfidf:
        print_tfidf = True

    if args.save:
        save = True

    if args.obj_sub:
        objective_vs_subjective(print_tfidf, save)
    elif args.pos_neg:
        positive_vs_negative(print_tfidf, save)
