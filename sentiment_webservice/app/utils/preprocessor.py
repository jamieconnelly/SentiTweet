from __future__ import unicode_literals, division
import string
import re
import htmlentitydefs
import csv
import app.utils.regex as r

from nltk.corpus import stopwords as sw
from nltk.stem import PorterStemmer
from nltk import pos_tag


class Preprocessor():
    def __init__(self):
        self.stopwords = list(sw.words('english'))
        self.word_re = word_re
        self.emoticon_re = emoticon_re
        self.html_entity_digit_re = html_entity_digit_re
        self.html_entity_alpha_re = html_entity_alpha_re
        self.amp = amp
        self.url_re = url_re
        self.rep_char_re = rep_char_re
        self.hashtag_re = hashtag_re
        self.user_tag_re = user_tag_re
        self.lexicon = self.load_lexicon()
        self.stemmer = PorterStemmer()
        self.feats = {'pos': [], 'neg': []}

    def load_lexicon(self):
        with open('./app/data/lexicon.csv', 'rb') as f:
            reader = csv.reader(f)
            return dict((rows[2], rows[5]) for rows in reader)

    def reset_feats(self):
        self.feats = {k: [] for k, v in self.feats.iteritems()}

    def normalise_vect(self):
        max_val = 0
        for v in self.feats.itervalues():
            temp = max(map(lambda x: x[0], v))
            if temp > max_val:
                max_val = temp

        for k, v in self.feats.iteritems():
            self.feats[k] = map(lambda x: [0] if x[0] == 0 else [(x[0] / max_val) * 15], v)

    def pos_tags(self, tokens):
        TAG_MAP = ["NN", "NNP", "NNS", "VBP", "VB",
                   "VBD", 'VBG', "VBN", "VBZ", "MD",
                   "UH", "PRP", "PRP$"]
        tags = pos_tag(tokens)
        return [tag[1] for tag in tags if tag[1] in TAG_MAP]

    def normalise(self, tokens):

        vect = []

        for t in tokens:
            if t in self.stopwords:# or t in string.punctuation:
                continue

            if not self.emoticon_re.search(t):
                t = t.lower()

            t = self.rep_char_re.sub(r'\1', t)
            t = self.url_re.sub('_URL', t)
            t = self.hashtag_re.sub('_HASH', t)
            t = self.user_tag_re.sub('_USER', t)

            vect.append(self.stemmer.stem(t))

        tags = self.pos_tags(tokens)
        vect = tags + vect
        return vect

    def tokenise(self, tweet, lexicon_feats):
        tweet = self.__html2unicode(tweet)
        tokens = self.word_re.findall(tweet)
        if lexicon_feats:
            self.lexicon_lookup(tokens)
        return self.normalise(tokens)

    def lexicon_lookup(self, tokens):
        for k, v in self.feats.iteritems():
            self.feats[k].append([0])

        idx = len(self.feats['pos']) - 1

        for t in tokens:
            t = t.lower()
            if t in self.lexicon:
                if self.lexicon[t] == '4':
                    self.feats['pos'][idx][0] += 1
                elif self.lexicon[t] == '0':
                    self.feats['neg'][idx][0] += 1

    def ensure_unicode(self, tweet):
        try:
            return unicode(tweet)
        except UnicodeDecodeError:
            tweet = str(tweet).encode('string_escape')
            return unicode(tweet)

    def __html2unicode(self, s):
        """
        This function is curtosy of Christopher Potts
        http://sentiment.christopherpotts.net/index.html
        Internal metod that seeks to replace all the HTML entities in
        s with their corresponding unicode characters.
        """
        # First the digits:
        ents = set(self.html_entity_digit_re.findall(s))
        if len(ents) > 0:
            for ent in ents:
                entnum = ent[2:-1]
                try:
                    entnum = int(entnum)
                    s = s.replace(ent, unichr(entnum))
                except:
                    pass
        # Now the alpha versions:
        ents = set(self.html_entity_alpha_re.findall(s))
        ents = filter((lambda x: x != amp), ents)
        for ent in ents:
            entname = ent[1:-1]
            try:
                s = s.replace(ent,
                              unichr(htmlentitydefs.name2codepoint[entname]))
            except:
                pass
            s = s.replace(self.amp, " and ")
        return s


"""
    This file is based on the work of Christopher Potts
    however the file has been altered and extended for
    my purposes
    http://sentiment.christopherpotts.net/index.html
"""
emoticon_string = r"""
    (?:
      [<>]?
      [:;=8]                     # eyes
      [\-o\*\']?                 # optional nose
      [\)\]\(\[dDpP/\:\}\{@\|\\] # mouth
      |
      [\)\]\(\[dDpP/\:\}\{@\|\\] # mouth
      [\-o\*\']?                 # optional nose
      [:;=8]                     # eyes
      [<>]?
    )"""

# The components of the tokenizer:
regex_strings = (
    # Phone numbers:
    # r""""
    # (?:
    #   (?:            # (international)
    #     \+?[01]
    #     [\-\s.]*
    #   )?
    #   (?:            # (area code)
    #     [\(]?
    #     \d{3}
    #     [\-\s.\)]*
    #   )?
    #   \d{3}          # exchange
    #   [\-\s.]*
    #   \d{4}          # base
    # )""",
    # Emoticons:
    emoticon_string,
    # HTML tags:
    r'<[^>]+>',
    # Twitter username:
    r'(?:@[\w_]+)',
    # Links
    r'http\S+',
    # Twitter hashtags:
    r'(?:\#+[\w_]+[\w\'_\-]*[\w_]+)',
    # Remaining word types:
    r"""
    (?:[a-z][a-z'\-_]+[a-z])       # Words with apostrophes or dashes.
    # |
    # (?:[+\-]?\d+[,/.:-]\d+[+\-]?)  # Numbers, including fractions, decimals.
    |
    (?:[\w_]+)                    # Words without apostrophes or dashes.
    |
    (?:\.(?:\s*\.){1,})            # Ellipsis dots.
    |
    (?:\S)                         # Everything else that isn't whitespace
    """
)

negation_words = (
    """
    (?x)(?:
    ^(?:never|no|nothing|nowhere|noone|none|not|
        havent|hasnt|hadnt|cant|couldnt|shouldnt|
        wont|wouldnt|dont|doesnt|didnt|isnt|arent|aint
     )$
    )
    |
    n't
    """
)

# ######################################################################

word_re = re.compile(r'(%s)' % "|".join(regex_strings), re.VERBOSE | re.I | re.UNICODE)
emoticon_re = re.compile(regex_strings[1], re.VERBOSE | re.I | re.UNICODE)
html_entity_digit_re = re.compile(r'&#\d+;')
html_entity_alpha_re = re.compile(r'&\w+;')
amp = "&amp;"
punct_re = re.compile("^[.:;!?]$")
negation_re = re.compile(negation_words)
url_re = re.compile(r'http\S+')
rep_char_re = re.compile(r'(\w)\1{3,}')
hashtag_re = re.compile(r'(?:\#+[\w_]+[\w\'_\-]*[\w_]+)')
user_tag_re = re.compile(r'(?:@[\w_]+)')