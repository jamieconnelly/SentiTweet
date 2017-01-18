from __future__ import unicode_literals, division
import re
import htmlentitydefs
import csv
import app.utils.regex as r

from nltk.corpus import stopwords as sw
from nltk import pos_tag


class Preprocessor():

    def __init__(self):
        self.stopwords = sw.words('english')
        self.emoji_happy = self.emoji_happy()
        self.emoji_sad = self.emoji_sad()
        # self.acrynoms = self.load_acrynoms()
        self.pos_tags = None
        self.feats = {'caps': [], 'reps': [], 'NNP': [], 'UH': [], 'NPS': [],
                      'NP': [], 'NNS': [], 'PP': [], 'PP$': []}
        self.word_re = r.word_re
        self.emoticon_re = r.emoticon_re
        self.html_entity_digit_re = r.html_entity_digit_re
        self.html_entity_alpha_re = r.html_entity_alpha_re
        self.amp = r.amp
        self.punct_re = r.punct_re
        self.negation_re = r.negation_re
        self.url_re = r.url_re
        self.rep_char_re = r.rep_char_re
        self.hashtag_re = r.hashtag_re
        self.user_tag_re = r.user_tag_re

    def load_acrynoms(self):
        with open('../data/acrynom.csv', 'rb') as f:
            reader = csv.reader(f)
            slang = dict((rows[0], rows[1]) for rows in reader)
            return slang

    def reset_feats(self):
        self.feats = {k: [] for k, v in self.feats.iteritems()}

    def normalise_vect(self):
        max_val = 0
        for v in self.feats.itervalues():
            temp = max(map(lambda x: x[0], v))
            if temp > max_val:
                max_val = temp

        for k, v in self.feats.iteritems():
            self.feats[k] = map(lambda x: [0] if x[0] == 0 else [x[0]/max_val], v)

    def normalise(self, tokens):
        append_neg = False
        
        vect = []
        for t in tokens:
            if (t in self.stopwords and
                    not self.negation_re.match(t)):
                continue
            if not self.emoticon_re.search(t):
                t = t.lower()
            t = self.rep_char_re.sub(r'\1', t)
            t = self.url_re.sub('_URL', t)
            t = self.hashtag_re.sub('_HASH', t)
            t = self.user_tag_re.sub('_USER', t)
            

            # if r.punct_re.match(t):
            #     append_neg = False
            # if append_neg:
            #     vect.append(t + "_NEG")
            # else:
            #     vect.append(t)
            # if r.negation_re.match(t):
            #     append_neg = True
            vect.append(t)
        return vect

    def tokenise(self, tweet):
        tweet = self.__html2unicode(tweet)
        tokens = self.word_re.findall(tweet)
        self.pos_tags_count(tokens)
        self.caps_intensifier(tokens)
        self.char_repititions(tokens)
        return self.normalise(tokens)

    def pos_tags_count(self, tokens):
        useful_tags = ['NNP', 'NP', 'UH', 'NPS', 'NNS', 'PP', 'PP$']

        for tag in useful_tags:
            self.feats[tag].append([0])

        tags = pos_tag(tokens)
        idx = len(self.feats['NP']) - 1

        for tag in tags:
            if tag[1] in useful_tags:
                self.feats[tag[1]][idx][0] += 1

    def append_binary_feats(self, intensify, feat):
        if intensify:
            self.feats[feat].append([1])
        else:
            self.feats[feat].append([0])

    def char_repititions(self, tokens):
        reps = any(self.rep_char_re.search(word) for word in tokens)
        self.append_binary_feats(reps, 'reps')

    def caps_intensifier(self, tokens):
        caps = any(self.word_has_all_caps(word) for word in tokens)
        self.append_binary_feats(caps, 'caps')

    def word_has_all_caps(self, token):
        if (self.emoticon_re.search(token)
            or self.punct_re.match(token)
                or self.has_num(token)):
            return False

        if (token.upper() == token
            and (token != 'I'
                 and token != 'A')):
            return True

        return False

    def has_num(self, s):
        return any(i.isdigit() for i in s)

    def ensure_unicode(self, tweet):
        try:
            return unicode(tweet)
        except UnicodeDecodeError:
            tweet = str(tweet).encode('string_escape')
            return unicode(tweet)

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
        ents = filter((lambda x: x != r.amp), ents)
        for ent in ents:
            entname = ent[1:-1]
            try:
                s = s.replace(ent,
                              unichr(htmlentitydefs.name2codepoint[entname]))
            except:
                pass
            s = s.replace(self.amp, " and ")
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
