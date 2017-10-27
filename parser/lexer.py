import re

IF_TOKEN = 0
ELSE_TOKEN = 1
LPAREN_TOKEN = 2
RPAREN_TOKEN = 3
LT_TOKEN = 4
LE_TOKEN = 5
GT_TOKEN = 6
GE_TOKEN = 7
PREDICT_TOKEN = 8
COLON_TOKEN = 9
NUMBER_TOKEN = 10
FEATURE_TOKEN = 11

TOKEN_DICT = [
    ('If', IF_TOKEN),
    ('Else', ELSE_TOKEN),
    ('(', LPAREN_TOKEN),
    (')', RPAREN_TOKEN),
    ('<=', LE_TOKEN),
    ('<', LT_TOKEN),
    ('>=', GE_TOKEN),
    ('>', GT_TOKEN),
    ('Predict', PREDICT_TOKEN),
    (':', COLON_TOKEN),
    ('feature', FEATURE_TOKEN)]


class Token:
    def __init__(self, value, id):
        self.value = value
        self.id = id

    def __str__(self):
        return '(id={}, value={})'.format(self.id, self.value)


def lex(tree):
    tokens = []
    number = re.compile('\d+(\.\d+)?')

    def _tokenize(s):
        for (tval, tid) in TOKEN_DICT:
            if s.startswith(tval):
                return Token(tval, tid)
        m = number.match(s)
        if not m:
            raise Exception('Invalid token {}'.format(s))
        return Token(m.group(0), NUMBER_TOKEN)
    for line in tree.splitlines():
        line = line.strip()
        while line:
            token = _tokenize(line)
            tokens.append(token)
            line = line[len(token.value):].strip()
    return tokens


if __name__ == '__main__':
    with open('tree.txt') as tree_file:
        tokens = lex(tree_file.read())
    for token in tokens:
        print(token)
