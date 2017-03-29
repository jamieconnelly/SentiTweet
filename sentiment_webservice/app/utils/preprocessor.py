from __future__ import unicode_literals, division

import csv
import app.utils.regex as r

from nltk.corpus import stopwords as sw
from nltk import pos_tag
from nltk.stem import PorterStemmer


class Preprocessor:
    """Tweet tokenisor and feature extractor.

       Attributes:
           feats (dict of lists): Contains counts for lexicon features.

    """
    def __init__(self):
        self.stopwords = list(sw.words('english'))
        self.word_re = r.word_re
        self.emoticon_re = r.emoticon_re
        self.url_re = r.url_re
        self.rep_char_re = r.rep_char_re
        self.hashtag_re = r.hashtag_re
        self.user_tag_re = r.user_tag_re
        self.lexicon = self._load_lexicon()
        self.stemmer = PorterStemmer()
        self.feats = {'pos': [], 'neg': []}

    def tokenise(self, tweet, lexicon_feats=False):
        """Tweet tokenisor method.

            Args:
                tweet (str): Text of a tweet.
                lexicon_feats (bool): Whether to include lexicon
                    features or not.

            Returns:
                Returns list of str.
        """
        tokens = self.word_re.findall(tweet)
        if lexicon_feats:
            self._lexicon_lookup(tokens)
        return self._normalise(tokens)

    def reset_feats(self):
        """Re-initialises the feats attribute."""
        self.feats = {k: [] for k, v in self.feats.iteritems()}

    def normalise_vect(self):
        """Normalises each value in the feats attribute."""
        max_val = 0
        for v in self.feats.itervalues():
            temp = max(map(lambda x: x[0], v))
            if temp > max_val:
                max_val = temp

        for k, v in self.feats.iteritems():
            self.feats[k] = map(lambda x: [0] if x[0] == 0 else [(x[0] / max_val) * 15], v)

    def _load_lexicon(self):
        with open('./app/data/lexicon.csv', 'rb') as f:
            reader = csv.reader(f)
            return dict((rows[2], rows[5]) for rows in reader)

    def _pos_tags(self, tokens):
        TAG_MAP = ["NN", "NNP", "NNS", "VBP", "VB", "VBD", 'VBG',
                   "VBN", "VBZ", "MD","UH", "PRP", "PRP$"]
        tags = pos_tag(tokens)
        return [tag[1] for tag in tags if tag[1] in TAG_MAP]

    def _normalise(self, tokens):

        token_list = []

        for t in tokens:
            # Ignore stopwords
            if t in self.stopwords:
                continue

            # lowercase all tokens except for emoticons
            if not self.emoticon_re.search(t):
                t = t.lower()

            # Normalise tokens
            t = self.rep_char_re.sub(r'\1', t)
            t = self.url_re.sub('_URL', t)
            t = self.hashtag_re.sub('_HASH', t)
            t = self.user_tag_re.sub('_USER', t)

            # Get token's stem and append it to the list
            token_list.append(self.stemmer.stem(t))

        # Get list of pos tags and append to token_list
        tags = self._pos_tags(tokens)
        token_list = tags + token_list
        return token_list

    def _lexicon_lookup(self, tokens):
        # Initialise new 'row' to list
        for k, v in self.feats.iteritems():
            self.feats[k].append([0])

        idx = len(self.feats['pos']) - 1

        # Check if token is in lexicon dictionary.
        # If it is increment pos/neg feature count
        for t in tokens:
            t = t.lower()
            if t in self.lexicon:
                if self.lexicon[t] == '4':
                    self.feats['pos'][idx][0] += 1
                elif self.lexicon[t] == '0':
                    self.feats['neg'][idx][0] += 1
