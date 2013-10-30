# coding:utf-8

'''
TokenStream represents a stream of tokens that a parser will consume.
TokenStream can be used to consume tokens, peek ahead, and synchonize to a
delimiter token. The tokens that the token stream operates on are either
compiled regular expressions or strings.
'''

import re

LBRACKET   = '<'
AT_SYMBOL  = '@'
RBRACKET   = '>'
DQUOTE     = '"'

BAD_DOMAIN = re.compile(r'''                                    # start or end
                        ^-|-$                                   # with -
                        ''', re.MULTILINE | re.VERBOSE)

DELIMITER  = re.compile(r'''
                        [,;][,;\s]*                             # delimiter
                        ''', re.MULTILINE | re.VERBOSE)

WHITESPACE = re.compile(r'''
                        (\ |\t)+                                # whitespace
                        ''', re.MULTILINE | re.VERBOSE)

UNI_WHITE  = re.compile(ur'''
                        [
                            \u0020\u00a0\u1680\u180e
                            \u2000-\u200a
                            \u2028\u202f\u205f\u3000
                        ]*
                        ''', re.MULTILINE | re.VERBOSE | re.UNICODE)

# because we only use an atom in display-names, we've included a dot (.) which
# is normally not part of an atom. this allows us to be a little more relaxed
# in display-name parsing.
ATOM       = re.compile(r'''
                        [A-Za-z0-9\.!#$%&'*+\-/=?^_`{|}~]+        # atext
                        ''', re.MULTILINE | re.VERBOSE)

DOT_ATOM   = re.compile(r'''
                        [A-Za-z0-9!#$%&'*+\-/=?^_`{|}~]+        # atext
                        (\.[A-Za-z0-9!#$%&'*+\-/=?^_`{|}~]+)*   # (dot atext)*
                        ''', re.MULTILINE | re.VERBOSE)

UNI_ATOM   = re.compile(ur'''
                        (
                        \w|                                     # word
                        [\u0080-\u00FF]|                        # latin-1 supplement
                        [\u0100-\u017F]|                        # latin extended-a
                        [\u0180-\u024F]|                        # latin extended-b
                        [\u2000-\u2064]|                        # general punctuation
                        [\u20a0-\u20ba]|                        # currency symbols
                        [\u2100-\u214f]|                        # letterlike symbols
                        [\u2190-\u21ff]|                        # arrows
                        [\u2200-\u22ff]|                        # mathematic operators
                        [\u2300-\u23f4]|                        # miscellaneous technical
                        [\u2460-\u24ff]|                        # enclosed alphanumerics
                        [\u2580-\u259f]|                        # block elements
                        [\u25a0-\u25ff]|                        # geometric shapes
                        [\u2600-\u26ff]|                        # miscellaneous symbols
                        [\u2701-\u27BF]|                        # dingbats
                        [\u2800-\u28ff]|                        # braille patterns
                        [\u2b00-\u2b59]|                        # misc symbols and arrows
                                                                # ancient symbols
                                                                # musical symbols
                        [\ud800-\udbff\udc00-\udfff]|           # emoji
                                                                # emoticons
                                                                # transport and map symbols
                        )+
                        ''', re.MULTILINE | re.VERBOSE | re.UNICODE)

UNI_QSTR   = re.compile(ur'''
                        "
                            (?P<qstr>
                                (
                                    \w|                                     # word
                                    \s|                                     # space
                                    [\u0080-\u00FF]|                        # latin-1 supplement
                                    [\u0100-\u017F]|                        # latin extended-a
                                    [\u0180-\u024F]|                        # latin extended-b
                                    [\u2000-\u2064]|                        # general punctuation
                                    [\u20a0-\u20ba]|                        # currency symbols
                                    [\u2100-\u214f]|                        # letterlike symbols
                                    [\u2190-\u21ff]|                        # arrows
                                    [\u2200-\u22ff]|                        # mathematic operators
                                    [\u2300-\u23f4]|                        # miscellaneous technical
                                    [\u2460-\u24ff]|                        # enclosed alphanumerics
                                    [\u2580-\u259f]|                        # block elements
                                    [\u25a0-\u25ff]|                        # geometric shapes
                                    [\u2600-\u26ff]|                        # miscellaneous symbols
                                    [\u2701-\u27BF]|                        # dingbats
                                    [\u2800-\u28ff]|                        # braille patterns
                                    [\u2b00-\u2b59]|                        # misc symbols and arrows
                                                                            # ancient symbols
                                                                            # musical symbols
                                    [\ud800-\udbff\udc00-\udfff]|           # emoji
                                                                            # emoticons
                                                                            # transport and map symbols
                                )+
                            )
                        "
                        ''', re.MULTILINE | re.VERBOSE | re.UNICODE)

QSTRING    = re.compile(r'''
                        "                                       # dquote
                        (\s*                                    # whitespace
                        ([\x21\x23-\x5b\x5d-\x7e]               # qtext
                        |                                       # or
                        \\[\x21-\x7e\t\ ]))*                    # quoted-pair
                        \s*                                     # whitespace
                        "                                       # dquote
                        ''', re.MULTILINE | re.VERBOSE)

URL        = re.compile(r'''
                        (?:http|https)://
                        [^\s<>{}|\^~\[\]`;,]+
                        ''', re.MULTILINE | re.VERBOSE | re.UNICODE)

class TokenStream(object):
    '''
    Represents the stream of tokens that the parser will consume. The token
    stream can be used to consume tokens, peek ahead, and synchonize to a
    delimiter token.

    When the strem reaches its end, the position is placed
    at one plus the position of the last token.
    '''
    def __init__(self, stream):
        self.position = 0
        self.stream = stream

    def get_token(self, token, ngroup=None):
        '''
        Get the next token from the stream and advance the stream. Token can
        be either a compiled regex or a string.
        '''
        # match single character
        if isinstance(token, basestring) and len(token) == 1:
            if self.peek() == token:
                self.position += 1
                return token
            return None

        # match a pattern
        match = token.match(self.stream, self.position)
        if match:
            advance = match.end() - match.start()
            self.position += advance

            # if we are asking for a named capture, return jus that
            if ngroup:
                return match.group(ngroup)
            # otherwise return the entire capture
            return match.group()

        return None

    def end_of_stream(self):
        '''
        Check if the end of the stream has been reached, if it has, returns
        True, otherwise false.
        '''
        if self.position >= len(self.stream):
            return True
        return False

    def synchronize(self):
        '''
        Advances the stream to synchronizes to the delimiter token. Used primarily
        in relaxed mode parsing.
        '''
        start_pos = self.position
        end_pos = len(self.stream)

        match = DELIMITER.search(self.stream, self.position)
        if match:
            self.position = match.start()
            end_pos = match.start()
        else:
            self.position = end_pos

        skip = self.stream[start_pos:end_pos]
        if skip.strip() == '':
            return None

        return skip

    def peek(self, token=None):
        '''
        Peek at the stream to see what the next token is or peek for a
        specific token.
        '''
        # peek at whats next in the stream
        if token is None:
            if self.position < len(self.stream):
                return self.stream[self.position]
            else:
                return None
        # peek for a specific token
        else:
            match = token.match(self.stream, self.position)
            if match:
                return self.stream[match.start():match.end()]
            return None