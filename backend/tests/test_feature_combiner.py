from utils.classifier import FeatureCombiner
import numpy as np
import unittest


class TestFeatureCombiner(unittest.TestCase):

    def setUp(self):
        self.feat_comb = FeatureCombiner()

    def tearDown(self):
        self.feat_comb = None

    def test_transform(self):
        matrix = np.zeros((2, 2))
        feats = {'caps': [[1], [1]],
                 'reps': [[2], [2]],
                 'pos': [[3], [3]],
                 'neg': [[4], [4]]}
        new_matrix = self.feat_comb.transform(matrix, feats)
        self.assertEqual(new_matrix.shape, (2, 6))


if __name__ == '__main__':
    unittest.main()
