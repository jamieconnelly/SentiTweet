from __future__ import unicode_literals
import string
import re
import sys

from nltk.corpus import stopwords as sw
from nltk.corpus import wordnet as wn
from nltk.tokenize import TweetTokenizer
from nltk import WordNetLemmatizer
from nltk import pos_tag
from nltk.compat import python_2_unicode_compatible
from sklearn.base import BaseEstimator, TransformerMixin


@python_2_unicode_compatible
class Preprocessor(BaseEstimator, TransformerMixin):

    def __init__(self):
        self.stopwords = sw.words('english')
        self.punct = set(string.punctuation)
        self.lemmatizer = WordNetLemmatizer()
        self.emoji_happy = self.emoji_happy()
        self.emoji_sad = self.emoji_sad()
        self.tknzr = TweetTokenizer(preserve_case=True,
                                    reduce_len=True,
                                    strip_handles=True)
        # sys.maxunicode == 0xffff

    def fit(self, X, y=None):
        return self

    def inverse_transform(self, X):
        return X

    def transform(self, X):
        return [list(self.token(tweet)) for tweet in X]

    def emoji_happy(self):
        try:
            return re.compile(u'['
                              u'\U0001f600-\U0001F60F'
                              u'\U0001F617-\U0001F61D'
                              u'\U0001F638-\U0001F63D'
                              ']+', re.UNICODE)
        except re.error:
            return re.compile(u'('
                              u'\ud83d[\ude00-\ude0f]|'
                              u'\ud83d[\ude17-\ude1d]|'
                              u'\ud83d[\ude38-\ude3d]'
                              ')+', re.UNICODE)

    def emoji_sad(self):
        try:
            return re.compile(u'['
                              u'\U0001F612-\U0001F616'
                              u'\U0001F61E-\U0001F62B'
                              u'\U0001F63E-\U0001F63F'
                              ']+', re.UNICODE)
        except re.error:
            return re.compile(u'('
                              u'\ud83d[\ude12-\ude16]|'
                              u'\ud83d[\ude1e-\ude2b]|'
                              u'\ud83d[\ude3e-\ude3f]'
                              ')+', re.UNICODE)

    def emoji_patterns(self):
        try:
            return re.compile(u'['
                              u'\U0001F300-\U0001F64F'
                              u'\U0001F680-\U0001F6FF'
                              u'\u2600-\u26FF\u2700-\u27BF]+',
                              re.UNICODE)
        except re.error:
            return re.compile(u'('
                              u'\ud83c[\udf00-\udfff]|'
                              u'\ud83d[\udc00-\ude4f\ude80-\udeff]|'
                              u'[\u2600-\u26FF\u2700-\u27BF])+',
                              re.UNICODE)

    def token(self, tweet):  
        tweet = self.emoji_happy.sub(r'happy', tweet)
        tweet = self.emoji_sad.sub(r'sad', tweet)
        result = []

        for token in self.tknzr.tokenize(tweet):
            token = token.lower()
            token = token.strip()
            token = re.sub(r'http\S+', 'URL', token)
            if token in self.stopwords or token in self.punct:
                continue
            result.append(token)

        return result

    def tokenize(self, tweet):

        for token, tag in pos_tag(self.tknzr.tokenize(tweet)):
            token = token.lower()
            token = token.strip()
            token = token.translate(self.table)
            token = re.sub(r'http\S+', 'URL', token)
            token = self.emoji.sub(r'', token)

            if token in self.stopwords or token in self.punct:
                continue

            lemma = self.lemmatize(token, tag)
            yield lemma

    def lemmatize(self, token, tag):
        tag = {'N': wn.NOUN, 'V': wn.VERB,
               'R': wn.ADV, 'J': wn.ADJ}.get(tag[0], wn.NOUN)
        return self.lemmatizer.lemmatize(token, tag)


def identity(arg):
    return arg
