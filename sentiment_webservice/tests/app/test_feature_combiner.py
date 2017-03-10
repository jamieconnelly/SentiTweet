from app.utils.classifier import FeatureCombiner
from app.utils.preprocessor import Preprocessor
import numpy as np
import unittest


class TestFeatureCombiner(unittest.TestCase):

    def setUp(self):
        self.feat_comb = FeatureCombiner()
        self.pre = Preprocessor()

    def tearDown(self):
        self.feat_comb = None

    def test_transform(self):
        matrix = np.zeros((2, 2))
        self.pre.feats = {'pos': [[3], [3]],
                          'neg': [[4], [4]]}
        new_matrix = self.feat_comb.transform(matrix, self.pre)
        self.assertEqual(new_matrix.shape, (2, 4))

if __name__ == '__main__':
    unittest.main()
