from __future__ import division
from app.utils.preprocessor import Preprocessor
import unittest


class TestPreProcessor(unittest.TestCase):

    def setUp(self):
        self.pre = Preprocessor()

    def tearDown(self):
        self.pre = None

    def test_tokeniser(self):
        tweet = '@SomeUser: YAAAAAAY!!! :-D http://sentimentsymposium.com/'
        tokens = ['NN', 'NN', 'NN', '_USER', ':', 'yay', '!', '!', '!', ':-D', '_URL']
        self.assertEqual(self.pre.tokenise(tweet, False), tokens)
        tweet = 'don\'t she\'d it\'s'
        tokens = ['NN', 'VBD', 'NN', 'don\'t', 'she\'d', 'it\'']
        self.assertEqual(self.pre.tokenise(tweet, False), tokens)

    def test_remove_stopwords(self):
        tweet = 'this has a lot of stopword'
        tokens = ['VBZ', 'NN', 'NN', 'lot', 'stopword']
        self.assertEqual(self.pre.tokenise(tweet, False), tokens)

    def test_minimise_repeated_chars(self):
        tweet = 'yaaaaaaaaaaay'
        self.assertEqual(self.pre.tokenise(tweet, False), ['NN', 'yay'])
        tweet = ':D'
        self.assertEqual(self.pre.tokenise(tweet, False), ['NN', ':D'])

    def test_lowercase(self):
        tweet = 'CHANGE LOWER'
        self.assertEqual(self.pre.tokenise(tweet, False), ['NNP', 'NNP', 'chang', 'lower'])

    def test_URL_replacement(self):
        tweet = 'http://www.example'
        self.assertEqual(self.pre.tokenise(tweet, False), ['NN', '_URL'])

    def test_change_hashtags(self):
        tweet = '#hastagone #ALLCAPSHASHTAG #NumbersAndChars123'
        self.assertEqual(self.pre.tokenise(tweet, False), ['NN', 'NN', '_HASH', '_HASH', '_HASH'])

    def test_change_usertags(self):
        tweet = '@mention @Mention2 @MenT10N_'
        self.assertEqual(self.pre.tokenise(tweet, False), ['NN', 'NN', '_USER', '_USER', '_USER'])

    def test_pos_tagging(self):
        tokens = ['Jamie', 'this', 'Scotland', 'dog', 'she', 'he']
        tags = self.pre._pos_tags(tokens)
        self.assertEqual(tags, ['NNP', 'NNP', 'NN', 'PRP', 'PRP'])
        tokens = ['this', 'dog', 'she', 'her']
        tags = self.pre._pos_tags(tokens)
        self.assertEqual(tags, ['NN', 'PRP', 'PRP$'])

    def test_lexicon_lookup(self):
        tweet = 'happy sad ABANDONED dog'
        lexicon_feats = {'pos': [[1]], 'neg': [[2]]}
        self.pre.tokenise(tweet, True)
        self.assertEqual(self.pre.feats, lexicon_feats)

    def test_reset_feats(self):
        feats = {'a': [1, 2, 3], 'b': [0, 0, 0]}
        self.pre.feats = feats
        self.pre.reset_feats()
        self.assertEqual(self.pre.feats, {'a': [], 'b': []})

    def test_normalise(self):
        feats = {'a': [[0], [5], [6]],
                 'b': [[0], [4], [10]]}
        normalised = {'a': [[0.0], [7.5], [9]],
                      'b': [[0.0], [6], [15]]}
        self.pre.feats = feats
        self.pre.normalise_vect()
        self.assertEqual(self.pre.feats, normalised)

if __name__ == '__main__':
    unittest.main()
