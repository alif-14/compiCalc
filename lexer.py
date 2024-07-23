import re

# Token definitions
TOKEN_REGEX = [
    ('NUM', r'\d+(\.\d*)?([eE][+-]?\d+)?'),  # Number (integer, float, scientific notation)
    ('SIN', r'sin'),                     # sin function
    ('COS', r'cos'),                     # cos function
    ('PRINT', r'print'),                 # print statement
    ('ID', r'[a-zA-Z][a-zA-Z0-9_]*'),    # Identifier (starts with letter, followed by letters, digits, or underscores)
    ('ASSIGN', r'='),                    # Assignment operator
    ('PLUS', r'\+'),                     # Addition operator
    ('MINUS', r'-'),                     # Subtraction operator
    ('POWER', r'\*\*'),                  # Exponentiation operator (two asterisks)
    ('TIMES', r'\*'),                    # Multiplication operator
    ('DIVIDE', r'/'),                    # Division operator
    ('LPAREN', r'\('),                   # Left parenthesis
    ('RPAREN', r'\)'),                   # Right parenthesis
    ('SEMI', r';'),                      # Semicolon
    ('WS', r'\s+'),                      # Whitespace
]

def lexer(input_code):
    tokens = []
    line_number = 1
    position = 0
    while position < len(input_code):
        match = None
        for token_type, regex_pattern in TOKEN_REGEX:
            pattern = re.compile(regex_pattern)
            match = pattern.match(input_code, position)
            if match:
                token_value = match.group(0)
                if token_type != 'WS':  # Skip whitespace tokens
                    tokens.append((token_type, token_value, line_number))
                position = match.end()
                break
        if not match:
            if input_code[position] == '\n':
                line_number += 1
            elif input_code[position] not in [' ', '\t', '\r']:
                raise SyntaxError(f"Unexpected character '{input_code[position]}' at line {line_number}")
            position += 1
    
    return tokens

