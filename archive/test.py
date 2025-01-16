# import ply.lex as lex
#
# # Define token names, including the missing POS command tokens
# tokens = [
#     'IF', 'THEN', 'ECHO', 'EXIT', 'POS', 'ALLOCATION', 'NODE', 'COMMAND',
#     'NUMBER', 'STRING', 'VARIABLE', 'FLAG', 'FILENAME',
#     'POS_ALLOCATE', 'POS_FREE', 'POS_IMAGE', 'POS_VARIABLES', 'POS_RESET', 'POS_LAUNCH'
# ]
#
# # Define regular expressions for tokens
# t_IF = r'if'
# t_THEN = r'then'
# t_ECHO = r'echo'
# t_EXIT = r'exit'
# t_POS = r'pos'
# t_ALLOCATION = r'allocations'
# t_NODE = r'nodes'
# t_COMMAND = r'commands'
# t_FLAG = r'--[a-zA-Z-]+'
# t_FILENAME = r'[a-zA-Z0-9/_-]+\.[a-z]+'
#
# # Rules for specific POS commands
# t_POS_ALLOCATE = r'allocate'
# t_POS_FREE = r'free'
# t_POS_IMAGE = r'image'
# t_POS_VARIABLES = r'variables'
# t_POS_RESET = r'reset'
# t_POS_LAUNCH = r'launch'
#
# # Define other tokens with custom behavior
# def t_VARIABLE(t):
#     r'\$[0-9]+'
#     return t
#
# def t_STRING(t):
#     r'\"([^\\\"]|\\.)*\"'
#     t.value = t.value[1:-1]  # Strip quotes
#     return t
#
# def t_NUMBER(t):
#     r'\d+'
#     t.value = int(t.value)
#     return t
#
# # Ignore spaces and tabs
# t_ignore = ' \t'
#
# # Handle newlines
# def t_newline(t):
#     r'\n+'
#     t.lexer.lineno += len(t.value)
#
# # Error handling rule
# def t_error(t):
#     print(f"Illegal character '{t.value[0]}'")
#     t.lexer.skip(1)
#
# # Build the lexer
# lexer = lex.lex()
#
# # Sample script input
# data = '''
# if test "$#" -ne 2; then
#     echo "Usage: setup.sh loadgen-experiment-node dut-experiment-node"
#     exit
# fi
# echo "allocate hosts"
# pos allocations allocate "$1" "$2"
# pos nodes image "$1" debian-buster
# echo "execute experiment on hosts..."
# pos commands launch --quiet --infile loadgen/measurement.sh --blocking --loop "$1"
# '''
#
# # Give the lexer the input
# lexer.input(data)
#
# # Tokenize
# for tok in lexer:
#     print(tok)

import ply.lex as lex
import json

# Define token names
tokens = [
    'POS', 'ALLOCATION', 'NODE', 'COMMAND',
    'VARIABLE', 'STRING', 'QUOTED_STRING'
]

# Define regular expressions for tokens
t_POS = r'pos'
t_ALLOCATION = r'allocations'
t_NODE = r'nodes'
t_COMMAND = r'allocate|image'

# Rule for quoted variables like "$1"
def t_QUOTED_STRING(t):
    r'"\$[0-9]+"'
    t.value = t.value.strip('"')  # Remove surrounding quotes
    return t

# Rule for unquoted strings like "debian-buster"
def t_STRING(t):
    r'[a-zA-Z0-9-_]+'
    return t

# Ignore spaces and tabs
t_ignore = ' \t'

# Handle newlines (ignored but counts lines)
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Error handling rule
def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

# Sample script input (simplified)
data = '''
pos allocations allocate "$1" "$2"
pos nodes image "$1" debian-buster
'''

# Initialize metadata structure
metadata = []

# Process each line of the script
lexer.input(data)

# Initialize current command with default keys
current_command = {"action": None, "details": {}}

for tok in lexer:
    print(tok)
    if tok.type == 'POS':
        # Start a new command
        current_command = {"action": None, "details": {}}
    elif tok.type == 'ALLOCATION' and tok.value == 'allocations':
        current_command["action"] = "allocate"
    elif tok.type == 'NODE' and tok.value == 'nodes':
        current_command["action"] = "set_image"
    elif tok.type == 'COMMAND':
        if tok.value == 'allocate':
            current_command["details"]["hosts"] = []
    elif tok.type == 'QUOTED_STRING':
        if current_command["action"] == "allocate":
            current_command["details"]["hosts"].append(tok.value)
        elif current_command["action"] == "set_image":
            current_command["details"]["host"] = tok.value
    elif tok.type == 'STRING':
        print("string", tok)
        if tok.value == 'allocate':
            print('allocate', tok.value)
            current_command["action"] = "allocate hosts"
        if current_command["action"] == "set_image":
            current_command["details"]["image"] = tok.value

    print(current_command)
    metadata.append(current_command)
    # # After each complete command line, append and reset
    # if tok.type == 'COMMAND' or lexer.token() is None:
    #     if current_command["action"]:  # Only add non-empty actions
    #         metadata.append(current_command)
    #     current_command = {"action": None, "details": {}}  # Reset for next command

# Convert metadata to JSON
metadata_json = json.dumps(metadata, indent=4)
print(metadata_json)
