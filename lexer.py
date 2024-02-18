import re

from parse_token import Token

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
        '$'         : 'separator',
        '('         : 'separator',
        ')'         : 'separator',
        '{'         : 'separator',
        '}'         : 'separator',
        ','         : 'separator',
        ';'         : 'separator',
        #---------- Separators ----------#
        #---------- Operator ----------#
        '+'        : 'operator',
        '-'        : 'operator',
        '*'        : 'operator',
        '/'        : 'operator',
        '='        : 'operator',
        '=='        : 'operator',
        '!='        : 'operator',
        '<'         : 'operator',
        '>'         : 'operator',
        '<='        : 'operator',
        '>='        : 'operator',
        #---------- Operator ----------#
    }

    def __init__(self, sourceCode):
        self.sourceCode = sourceCode
        self.tokens = []

    def tokenize(self):
        """
        This function is used to validate and tokenize the source code.
        This will be called from the compiler.py file.

        Parameters:
        None

	Returns:
	list: A list of tokens identified in the source code.
        """

	# Remove comments from source code
        re_comments = r'\[\*[\s\S]*?\*\]'
        self.sourceCode = re.sub(re_comments, '', self.sourceCode)

        # Split source code into tokens
        re_separators = r'(?=[\(\)\{\}\,\;\$\s])|(?<=[\(\)\{\}\,\;\$\s])'
        potentialTokens = re.split(re_separators, self.sourceCode)

        # Filter out empty strings and whitespace-only strings
        potentialTokens = [token for token in potentialTokens if token.strip() != '']

        for token in potentialTokens:
            if token in self.symbols:
                self.tokens.append(Token(self.symbols[token], token))
            elif re.match('^[A-Za-z][A-Za-z0-9_]*$', token):
                self.tokens.append(Token('identifier', token))
            elif re.match('^\d+$', token):
                self.tokens.append(Token('integer', token))
            elif re.match('^\d+\.\d+$', token):
                self.tokens.append(Token('real', token))
            else:
                self.tokens.append(Token('invalid', token))

        return self.tokens
