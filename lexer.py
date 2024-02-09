import re

keywords = ['function ', 'integer', 'boolean', 'real','if', 'else', 'endif', 'while', 'return', 'scan', 'print', 'true', 'false']
separator = []
operator = []
# regex for validating the identifier: ^[A-Za-z][A-Za-z0-9_]*$


def lexer(line):
    # check against keywords and stuff