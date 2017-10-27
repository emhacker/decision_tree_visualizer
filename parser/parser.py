from lexer import lex
import lexer

IF_RULE = 1
ELSE_RULE = 2
PREDICT_RULE = 3


class Rule:
    def __init__(self, rule_id, tokens):
        self.id = rule_id
        self.tokens = tokens
        self.childes = list()

    def __str__(self):
        return ' '.join(map(lambda x: x.value, self.tokens))


def parse(tokens):
    rules = []
    while tokens:
        RELATIONS = [lexer.GT_TOKEN, lexer.GE_TOKEN, lexer.LT_TOKEN,
                     lexer.LE_TOKEN]
        token0 = tokens[0]
        print ('token0 is {}'.format(token0))
        if token0.id == lexer.IF_TOKEN or token0.id == lexer.ELSE_TOKEN:
            if len(tokens) < 7:
                raise Exception('Not enough tokens in stream')
            if tokens[1].id != lexer.LPAREN_TOKEN:
                raise Exception("Expected lparen token after '{}'"
                                .format(token0.value))
            if tokens[2].id != lexer.FEATURE_TOKEN:
                raise Exception("Expected feature token after 'lparen'")
            if tokens[3].id != lexer.NUMBER_TOKEN:
                raise Exception("Expected a number token after 'feature'")
            id4 = tokens[4].id
            if id4 not in RELATIONS:
                raise Exception("Expected relation after '{}'"
                                .format(tokens[3].value))
            if tokens[5].id != lexer.NUMBER_TOKEN:
                raise Exception("Expected a number after '{}'"
                                .format(tokens[4].value))
            if tokens[6].id != lexer.RPAREN_TOKEN:
                raise Exception("Expected a rparen token after '{}'"
                                .format(tokens[6].value))
            rule = Rule(IF_RULE if token0.id == lexer.IF_TOKEN else ELSE_RULE,
                        tokens[:7])
        elif token0.id == lexer.PREDICT_TOKEN:
            if len(tokens) < 3:
                raise Exception('Not enough tokens in stream')
            if tokens[1].id != lexer.COLON_TOKEN:
                raise Exception("Expected ':' after '{}'".format(token0.value))
            if tokens[2].id != lexer.NUMBER_TOKEN:
                raise Exception("Expected number after ':'")
            rule = Rule(PREDICT_RULE, tokens[:3])
        else:
            raise Exception('Unkown rule')
        rules.append(rule)
        print ('ate {} tokens'.format(len(rule.tokens)))
        tokens = tokens[len(rule.tokens):]
    return rules

if __name__ == '__main__':
    with open('tree.txt') as tree_file:
        rules = parse(lex(tree_file.read()))
    for rule in rules:
        print(rule)
