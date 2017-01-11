# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
import htmlentitydefs
import csv

from nltk.corpus import stopwords as sw
from nltk import pos_tag
import utils.regex as r


class Preprocessor():

    def __init__(self):
        self.stopwords = sw.words('english')
        self.emoji_happy = self.emoji_happy()
        self.emoji_sad = self.emoji_sad()
        self.acrynoms = self.load_acrynoms()
        self.micro_feats = {'caps': []}

    def load_acrynoms(self):
        with open('../data/acrynom.csv', 'rb') as f:
            reader = csv.reader(f)
            slang = dict((rows[0], rows[1]) for rows in reader)
            return slang

    def reset_feats(self):
        self.micro_feats['caps'] = []

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

    def normalise(self, tweet):
        vect = []
        caps = False
        
        for w in tweet:
            # Check for uppercase intensifier
            if not r.emoticon_re.search(w):
              if w.upper() == w and not r.PUNCT_RE.match(w):
                  caps = True

        if caps:
            self.micro_feats['caps'].append([1])
        else:
            self.micro_feats['caps'].append([0])

        caps = False
        
        for w in tweet:
            # Remove stopwords unless they are negative stopwords
            if w in self.stopwords and not r.NEGATION_RE.match(w):
                continue
            # Preserve case of emoticons i.e. :D
            if not r.emoticon_re.search(w):
                w = w.lower()
            # Replace repeated characters with 3 occurances
            w = re.sub(r'(\w)\1{3,}', r'\1\1\1', w)
            # Replace urls with _URL tag
            w = re.sub(r'http\S+', '_URL', w)
            # Replace hash with _HASH tag
            w = re.sub(r'(?:\#+[\w_]+[\w\'_\-]*[\w_]+)', '_HASH', w)
            # Replace user mentions with _USER tag
            w = re.sub(r'(?:@[\w_]+)', '_USER', w)
            vect.append(w)
        # print self.micro_feats['all_caps']
        return vect

    def token(self, tweet):
        # Try to ensure unicode:
        try:
            tweet = unicode(tweet)
        except UnicodeDecodeError:
            tweet = str(tweet).encode('string_escape')
            tweet = unicode(tweet)
        # Fix HTML character entitites:
        tweet = self.__html2unicode(tweet)
        # Tokenise tweet
        tweet = r.word_re.findall(tweet)
        return self.normalise(tweet)

    def __html2unicode(self, s):
        """
        This function is curtosy of Christopher Potts
        http://sentiment.christopherpotts.net/index.html
        Internal metod that seeks to replace all the HTML entities in
        s with their corresponding unicode characters.
        """
        # First the digits:
        ents = set(r.html_entity_digit_re.findall(s))
        if len(ents) > 0:
            for ent in ents:
                entnum = ent[2:-1]
                try:
                    entnum = int(entnum)
                    s = s.replace(ent, unichr(entnum))
                except:
                    pass
        # Now the alpha versions:
        ents = set(r.html_entity_alpha_re.findall(s))
        ents = filter((lambda x: x != r.amp), ents)
        for ent in ents:
            entname = ent[1:-1]
            try:
                s = s.replace(ent,unichr(htmlentitydefs.name2codepoint[entname]))
            except:
                pass
            s = s.replace(r.amp, " and ")
        return s

# tweet = self.emoji_happy.sub(r'happy', tweet)
# tweet = self.emoji_sad.sub(r'sad', tweet)
# words = [w for segments in words for w in segments.split()]
# lmtzr = WordNetLemmatizer()
# lmtzr = SnowballStemmer("english")
# words = [lmtzr.stem(w) for w in words]
# for i, item in enumerate(results):
#     rep = self.acrynoms.get(item.lower())
#     if rep is not None:
#         results[i] = ' _ABREV'
# words = [w for segments in words for w in segments.split()]
# results = [w for segments in results for w in segments.split()]
# append_neg = False
# if r.PUNCT_RE.match(w):
    #     append_neg = False

    # if append_neg:
    #     results.append(w + "_NEG")
    # else:
    #     results.append(w)

    # if r.NEGATION_RE.match(w):
    #     append_neg = True
