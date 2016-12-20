from __future__ import unicode_literals
import string
import re

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
        self.stopwords  = sw.words('english')
        self.punct      = set(string.punctuation)
        self.lemmatizer = WordNetLemmatizer()
        self.table      = {ord(char): None for char in string.punctuation}
        self.emoji      = self.emoji_patterns()
        self.tknzr      = TweetTokenizer(preserve_case=True,
                                         reduce_len=True,
                                         strip_handles=True)

    def fit(self, X, y=None):
        return self

    def inverse_transform(self, X):
        return X

    def transform(self, X):
        return [list(self.tokenize(tweet)) for tweet in X]

    def emoji_patterns(self):
        try:
            # Wide UCS-4 build
            return re.compile(u'['
                              u'\U0001F300-\U0001F64F'
                              u'\U0001F680-\U0001F6FF'
                              u'\u2600-\u26FF\u2700-\u27BF]+',
                              re.UNICODE)
        except re.error:
            # Narrow UCS-2 build
            return re.compile(u'('
                              u'\ud83c[\udf00-\udfff]|'
                              u'\ud83d[\udc00-\ude4f\ude80-\udeff]|'
                              u'[\u2600-\u26FF\u2700-\u27BF])+',
                              re.UNICODE)

    def tokenize(self, tweet):

        for token, tag in pos_tag(self.tknzr.tokenize(tweet)):
            token = token.lower()
            token = token.strip()
            token = token.translate(self.table)
            token = re.sub(r'http\S+', '', token)
            token = self.emoji.sub(r'', token)

            if token in self.stopwords:
                continue

            lemma = self.lemmatize(token, tag)
            yield lemma

    def lemmatize(self, token, tag):
        tag = {'N': wn.NOUN, 'V': wn.VERB,
               'R': wn.ADV, 'J': wn.ADJ}.get(tag[0], wn.NOUN)
        return self.lemmatizer.lemmatize(token, tag)
