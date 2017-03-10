import re

"""
    This file is based on the work of Christopher Potts.
    However, the file has been altered and extended for
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

regex_strings = (
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
    |
    (?:[\w_]+)                     # Words without apostrophes or dashes.
    |
    (?:\.(?:\s*\.){1,})            # Ellipsis dots.
    |
    (?:\S)                         # Everything else that isn't whitespace
    """
)

word_re = re.compile(r'(%s)' % "|".join(regex_strings), re.VERBOSE | re.I | re.UNICODE)
emoticon_re = re.compile(regex_strings[0], re.VERBOSE | re.I | re.UNICODE)
html_entity_digit_re = re.compile(r'&#\d+;')
html_entity_alpha_re = re.compile(r'&\w+;')
amp = "&amp;"
url_re = re.compile(r'http\S+')
rep_char_re = re.compile(r'(\w)\1{3,}')
hashtag_re = re.compile(r'(?:\#+[\w_]+[\w\'_\-]*[\w_]+)')
user_tag_re = re.compile(r'(?:@[\w_]+)')
