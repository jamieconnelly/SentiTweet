from __future__ import division
from app.utils.preprocessor import Preprocessor
import unittest


class TestPreProcessor(unittest.TestCase):

    def setUp(self):
        self.pre = Preprocessor()

    def tearDown(self):
        self.pre = None

    def test_tokeniser(self):
        tweet = '@SomeUser: YAAAAAAY!!! &gt;:-D http://sentimentsymposium.com/'
        tokens = ['_USER', ':', 'yay', '!', '!', '!', '>:-D', '_URL']
        self.assertEqual(self.pre.tokenise(tweet), tokens)
        tweet = 'don\'t she\'d it\'s'
        tokens = ['don\'t', 'she\'d', 'it\'s']
        self.assertEqual(self.pre.tokenise(tweet), tokens)

    def test_remove_stopwords(self):
        tweet = 'this has a lot of stopwords'
        self.assertEqual(self.pre.tokenise(tweet), ['lot', 'stopwords'])

    # def test_append_neg(self):
    #     tweet = 'this has not a lot of stopwords'
    #     self.assertEqual(self.pre.tokenise(tweet), ['not', 'lot_NEG', 'stopwords_NEG'])

    def test_minimise_repeated_chars(self):
        tweet = 'yaaaaaaaaaaay'
        self.assertEqual(self.pre.tokenise(tweet), ['yay'])
        tweet = ':D'
        self.assertEqual(self.pre.tokenise(tweet), [':D'])

    def test_lowercase(self):
        tweet = 'CHANGE LOWER'
        self.assertEqual(self.pre.tokenise(tweet), ['change', 'lower'])

    def test_URL_replacement(self):
        tweet = 'http://www.example'
        self.assertEqual(self.pre.tokenise(tweet), ['_URL'])

    def test_change_hashtags(self):
        tweet = '#hastagone #ALLCAPSHASHTAG #NumbersAndChars123'
        self.assertEqual(self.pre.tokenise(tweet), ['_HASH', '_HASH', '_HASH'])

    def test_change_usertags(self):
        tweet = '@mention @Mention2 @MenT10N_'
        self.assertEqual(self.pre.tokenise(tweet), ['_USER', '_USER', '_USER'])

    def test_word_has_all_caps(self):
        tweet = 'CAPITALS'
        self.assertTrue(self.pre.word_has_all_caps(tweet))
        tweet = 'capitals'
        self.assertFalse(self.pre.word_has_all_caps(tweet))
        tweet = 'I'
        self.assertFalse(self.pre.word_has_all_caps(tweet))
        tweet = 'A'
        self.assertFalse(self.pre.word_has_all_caps(tweet))
        tweet = 'AB10000'
        self.assertFalse(self.pre.word_has_all_caps(tweet))
        tweet = ':)'
        self.assertFalse(self.pre.word_has_all_caps(tweet))
        tweet = '.'
        self.assertFalse(self.pre.word_has_all_caps(tweet))

    def test_caps_intensifier(self):
        tokens = ['not', 'Any', 'only', 'uppercase']
        self.pre.caps_intensifier(tokens)
        self.assertEqual(self.pre.feats['caps'], [[0]])
        tokens = ['HAS', 'uppercase']
        self.pre.caps_intensifier(tokens)
        self.assertEqual(self.pre.feats['caps'], [[0], [1]])
        tokens = ['HAs', 'uppercase', '123A']
        self.pre.caps_intensifier(tokens)
        self.assertEqual(self.pre.feats['caps'], [[0], [1], [0]])

    def test_repeadted_char_intensifier(self):
        tokens = ['this', 'haaaas', 'repitions']
        self.pre.char_repititions(tokens)
        self.assertEqual(self.pre.feats['reps'], [[1]])
        tokens = ['this', 'does', 'not']
        self.pre.char_repititions(tokens)
        self.assertEqual(self.pre.feats['reps'], [[1], [0]])

    def test_pos_tagging(self):
        tokens = ['Jamie', 'this', 'Scotland', 'dog', 'she', 'he']
        self.pre.pos_tags_count(tokens)
        self.assertEqual(self.pre.feats['NNP'], [[2]])
        tokens = ['this', 'dog', 'she', 'her']
        self.pre.pos_tags_count(tokens)
        self.assertEqual(self.pre.feats['NNP'], [[2], [0]])
        self.assertEqual(self.pre.feats['NP'], [[0], [0]])

    def test_reset_feats(self):
        feats = {'a': [1, 2, 3], 'b': [0, 0, 0]}
        self.pre.feats = feats
        self.pre.reset_feats()
        self.assertEqual(self.pre.feats, {'a': [], 'b': []})

    def test_normalise(self):
        feats = {'a':[[0],[5],[6]],
                 'b':[[0],[4],[10]],
                 'c':[[1],[4],[6]]}
        normalised = {'a':[[0.0],[0.5],[0.6]],
                      'b':[[0.0],[0.4],[1.0]],
                      'c':[[0.1],[0.4],[0.6]]}
        self.pre.feats = feats
        norm_feats = self.pre.normalise_vect()
        self.assertEqual(norm_feats, normalised)

    # def test_remove_punctuation(self):
    #     tweet = 'test, punct - removal!!!!?.'
    #     self.assertEqual(self.pre.token(tweet), ['test', 'punct', 'removal'])

    # def test_replace_happy_emojis(self):
    #     tweet = u'\U0001f601 \U0001F60F \U0001F618 \
    #              \U0001F61D \U0001F61A \U0001F638 \U0001F63D \U0001F60E'
    #     self.assertEqual(self.pre.token(tweet),
    #                      ['happy', 'happy', 'happy', 'happy', 'happy',
    #                      'happy', 'happy', 'happy'])

    # def test_replace_sad_emojis(self):
    #     tweet = u'\U0001F612 \U0001F616 \U0001F615 \U0001F61E \U0001F62B \
    #              \U0001F63E \U0001F63F'
    #     self.assertEqual(self.pre.token(tweet),
    #                      ['sad', 'sad', 'sad', 'sad', 'sad', 'sad', 'sad'])


if __name__ == '__main__':
    unittest.main()
