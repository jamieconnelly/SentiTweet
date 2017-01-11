from utils.preprocessor import Preprocessor
import unittest


class TestPreProcessor(unittest.TestCase):

    def setUp(self):
        self.pre = Preprocessor()

    def tearDown(self):
        self.pre = None

    def test_tokeniser(self):
        tweet = u'@SentimentSymp: lol can\'t Wait BRB #Sentiment talks! lol YAAAAAAY!!! &gt;:-D http://sentimentsymposium.com/'
        #self.assertEqual(self.pre.token(tweet), ['split', 'tweet', 'tokens'])
        print tweet
        l =  self.pre.token(tweet)
        print l
        # for w in l:
        #     print w + '\n'

    # def test_remove_stopwords(self):
    #     tweet = 'this has a lot of stopwords'
    #     self.assertEqual(self.pre.token(tweet), ['lot', 'stopwords'])

    # def test_minimise_repeated_chars(self):
    #     tweet = 'yaaaaaaaaaaay'
    #     self.assertEqual(self.pre.token(tweet), ['yaaay'])

    # def test_URL_replacement(self):
    #     tweet = 'http://www.example'
    #     self.assertEqual(self.pre.token(tweet), ['URL'])

    # def test_lowercase(self):
    #     tweet = '@hello: CHANGE TWEET LOWER'
    #     self.assertEqual(self.pre.token(tweet), ['change', 'tweet', 'lower'])

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
