import numpy as np


class FeatureCombiner(object):

    def transform(self, X, pre):
        pre.normalise_vect()
        feats = X
        for k, v in pre.feats.iteritems():
            feats = np.c_[feats, np.array(v)]
        return feats

    def fit(self, X, y=None):
        return self
