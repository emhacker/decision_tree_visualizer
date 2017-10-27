import sys
from parser import parse
import argparse


class State:
    def __init__(self, out_file):
        self.nodes = dict()
        self.counter = 0
        self.out_file = out_file

    def add_node(self, node):
        out_file.write('{} [label="{}"];\n'.format(self.counter, str(node)))
        self.nodes[node] = self.counter
        self.counter += 1


def node_pass(root, state):
    state.add_node(root)
    for node in root.childes:
        node_pass(node, state)


def edge_pass(root, state):
    if not root.childes:
        return
    if (len(root.childes) != 2):
        raise Exception('Semantic error: node {} has {} childes'
                        .format(str(root), len(root.childes)))
    node_l, node_r = root.childes[0], root.childes[1]
    state.out_file.write('{} -> {} [label="{}"];\n'
                         .format(state.nodes[root],
                                 state.nodes[node_l],
                                 'True'))
    state.out_file.write('{} -> {} [label="{}"];\n'
                         .format(state.nodes[root],
                                 state.nodes[node_r],
                                 'False'))
    edge_pass(node_l, state)
    edge_pass(node_r, state)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Decision tree visualizer.')
    parser.add_argument('--input_tree', required=True)
    parser.add_argument('--output_graph', required=True)
    args = parser.parse_args()
    root = parse(args.input_tree)
    if not root:
        print('Parse failed.')
        sys.exit(1)
    out_file = open(args.output_graph, 'w')
    out_file.write('digraph entity_match_flow {\n')
    state = State(out_file)
    node_pass(root, state)
    edge_pass(root, state)
    out_file.write('}\n')
    out_file.close()
