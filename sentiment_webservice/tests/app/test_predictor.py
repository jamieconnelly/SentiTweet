from __future__ import division
from app.utils.predictor import *
import unittest


class TestPredictor(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_predict_neut(self):
        tweet = ['Apple software, retail chiefs out in overhaul: \
                  SAN FRANCISCO Apple Inc CEO Tim Cook on Monday \
                  replaced the heads... http://bit.ly/XQEhJU']
        prediction = predict(tweet)
        self.assertEquals(prediction, [2])

    def test_predict_pos(self):
        tweet = ['love love love so happy']
        prediction = predict(tweet)
        self.assertEquals(prediction, [4])

    def test_predict_neg(self):
        tweet = ['I hate stuff like that']
        prediction = predict(tweet)
        self.assertEquals(prediction, [0])


if __name__ == '__main__':
    unittest.main()
