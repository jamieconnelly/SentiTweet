import re
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
    r"""
    (?:
      (?:            # (international)
        \+?[01]
        [\-\s.]*
      )?
      (?:            # (area code)
        [\(]?
        \d{3}
        [\-\s.\)]*
      )?
      \d{3}          # exchange
      [\-\s.]*
      \d{4}          # base
    )""",
    # Emoticons:
    emoticon_string,
    # HTML tags:
    r"""<[^>]+>""",
    # Twitter username:
    r"""(?:@[\w_]+)""",
    # Links
    r"""http\S+""",
    # Twitter hashtags:
    r"""(?:\#+[\w_]+[\w\'_\-]*[\w_]+)""",
    # Remaining word types:
    r"""
    (?:[a-z][a-z'\-_]+[a-z])       # Words with apostrophes or dashes.
    |
    (?:[+\-]?\d+[,/.:-]\d+[+\-]?)  # Numbers, including fractions, decimals.
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

######################################################################

word_re = re.compile(r"""(%s)""" % "|".join(regex_strings),
                     re.VERBOSE | re.I | re.UNICODE)
emoticon_re = re.compile(regex_strings[1], re.VERBOSE | re.I | re.UNICODE)
html_entity_digit_re = re.compile(r"&#\d+;")
html_entity_alpha_re = re.compile(r"&\w+;")
amp = "&amp;"
punct_re = re.compile("^[.:;!?]$")
negation_re = re.compile(negation_words)
url_re = re.compile(r'http\S+')
rep_char_re = re.compile(r'(\w)\1{3,}')
hashtag_re = re.compile(r'(?:\#+[\w_]+[\w\'_\-]*[\w_]+)')
user_tag_re = re.compile(r'(?:@[\w_]+)')
