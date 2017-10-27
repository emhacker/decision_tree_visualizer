from parser import (IF_RULE, ELSE_RULE, PREDICT_RULE)
from lexer import lex
import parser

'''
Stmt -> IF_RULE Stmt ELSE_RULE Stmt
Stmt -> PREDICT
'''


def sema_if(rules, idx, parent_node):
    if rules[idx].id != IF_RULE:
        raise Exception('Expected IF_RULE!, got {} at index {}'
                        .format(str(rules[idx], idx)))
    if_rule = rules[idx]
    if parent_node is None:
        parent_node = if_rule
    else:
        parent_node.childes.append(if_rule)
    print('DEBUG: ate if rule: {}'.format(rules[idx]))
    idx += 1
    idx = parse_tree(rules, idx, if_rule)
    if rules[idx].id != ELSE_RULE:
        raise Exception('Expected else rule, but seen {} rule at index {}'
                        .format(rules[idx], idx))
    print('DEBUG: ate else rule: {}'.format(rules[idx]))
    idx += 1
    idx = parse_tree(rules, idx, if_rule)
    return idx


def sema_predict(rules, idx, parent_node):
    if parent_node is None:
        raise Exception('Syntactic error, '
                        'predict statement cannot stand alone')
    if rules[idx].id != PREDICT_RULE:
        raise Exception('Expected PREDICT_RULE!, got {} at index {}'
                        .format(str(rules[idx]), idx))
    predict_rule = rules[idx]
    parent_node.childes.append(predict_rule)
    print('DEBUG: ate predict rule: {}'.format(predict_rule))
    return idx + 1


def parse_tree(rules, rule_idx, parent_node=None):
    rule0 = rules[rule_idx]
    if rule0.id == IF_RULE:
        rule_idx = sema_if(rules, rule_idx, parent_node)
    elif rule0.id == PREDICT_RULE:
        rule_idx = sema_predict(rules, rule_idx, parent_node)
    else:
        raise Exception('Uknown rule {}'.format(rule0))
    return rule_idx


def parse(tree_path):
    with open(tree_path) as tree_file:
        rules = parser.parse(lex(tree_file.read()))
        idx = parse_tree(rules, 0)
    return rules[0] if idx == len(rules) else None


if __name__ == '__main__':
    parse('tree.txt')
