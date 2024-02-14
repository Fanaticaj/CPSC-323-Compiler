import re

# regex for validating the identifier: ^[A-Za-z][A-Za-z0-9_]*$

class Lexer:
    symbols = {
        #---------- Keywords ----------#
        'function'  : 'keyword',
        'integer'   : 'keyword',
        'boolean'   : 'keyword',
        'real'      : 'keyword',
        'if'        : 'keyword',
        'else'      : 'keyword',
        'endif'     : 'keyword',
        'while'     : 'keyword',
        'return'    : 'keyword',
        'scan'      : 'keyword',
        'print'     : 'keyword',
        'true'      : 'keyword',
        'false'     : 'keyword',
        #---------- Keywords ----------#
        #---------- Separators ----------#
        '('         : 'separator',
        ')'         : 'separator',
        '{'         : 'separator',
        '}'         : 'separator',
        '['         : 'separator',
        ']'         : 'separator',
        ','         : 'separator',
        ';'         : 'separator',
        #---------- Separators ----------#
        #---------- Operator ----------#
        '::='       : 'operator',
        '$'         : 'operator',
        '|'         : 'operator',
        '<'         : 'operator',
        '>'         : 'operator',
        '<='        : 'operator',
        '>='        : 'operator',
        '!='        : 'operator',
        '=='        : 'operator',
        #---------- Operator ----------#

    }

    def __init__(self, sourceCode):
        self.sourceCode = sourceCode
    
    # validate: This function is used to validate the source code
    # Parameters: sourceCode - String - This will be the code from the RAT24S file.
    # This will be called from the compiler.py file
    def validate(sourceCode):
        print('validate')