script = r"""#!/bin/bash
pos allocations free "$1"
pos allocations free "$2"
"""

import bashlex

ast = bashlex.parse(script)

def is_command_node(node):
    return hasattr(node, 'kind') and node.kind == 'command'

def is_word_node(node):
    return hasattr(node, 'kind') and node.kind == 'word'

def host_name(arg):
    if arg == '$1':
        return "host one"
    elif arg == '$2':
        return "host two"
    return arg

def get_command_action(tokens):
    if not tokens or tokens[0] != 'pos':
        return None

    if tokens[1] == 'allocations':
        if tokens[2] == 'free' and len(tokens) == 4:
            return f"Free {host_name(tokens[3])}"
    return None

def traverse_ast(node):
    steps = []
    if is_command_node(node):
        tokens = [part.word for part in getattr(node, 'parts', []) if is_word_node(part)]
        action = get_command_action(tokens)
        if action:
            steps.append(action)

    for attr_name in ['parts', 'list', 'commands']:
        if hasattr(node, attr_name):
            for child in getattr(node, attr_name):
                steps.extend(traverse_ast(child))

    return steps

def get_experiment_steps(script_ast):
    steps = []
    for node in script_ast:
        steps.extend(traverse_ast(node))
    return {i+1: step for i, step in enumerate(steps)}

final_steps = get_experiment_steps(ast)
print(final_steps)
