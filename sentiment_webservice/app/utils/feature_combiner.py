import numpy as np


class FeatureCombiner(object):
    """Concatenates custom feature matrix with tfidf matrix."""

    def transform(self, X, pre):
        """Tweet tokenisor method.

            Args:
                X (numpy array): Feature matrix.
                pre (:obj:): Preprocessor object.

            Returns:
                Returns numpy array.
        """
        pre.normalise_vect()
        feats = X
        for k, v in pre.feats.iteritems():
            feats = np.c_[feats, np.array(v)]
        return feats

    def fit(self, X, y=None):
        return self
