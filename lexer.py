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
        re_operators = r'==|!=|<=|>=|\+|\-|\*|\/|<|>|='
        re_separators = r'\(|\)|\{|\}|\,|\;|\$|\s'
        re_split_pattern = f'({re_operators})|({re_separators})'
        potentialTokens = [token for token in re.split(re_split_pattern, self.sourceCode) if token and not token.isspace()]

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

    def print_tokens(self):
        """
        Print all tokens in the same structure as the source code
        Each token should be printed like this: <token_type='token_value'>
        For example: <integer='123'>
        """
        lines = self.sourceCode.split('\n')
        token_count_per_line = []
        for line in lines:
            re_operators = r'==|!=|<=|>=|\+|\-|\*|\/|<|>|='
            re_separators = r'\(|\)|\{|\}|\,|\;|\$|\s'
            re_split_pattern = f'({re_operators})|({re_separators})'
            potentialTokens = [token for token in re.split(re_split_pattern, line) if token and not token.isspace()]
            if potentialTokens:
                token_count_per_line.append(len(potentialTokens))
        current_token = 0
        for token_count in token_count_per_line:
            for i in range(token_count):
                curr_token = self.tokens[current_token]
                formatted_str = f"<{curr_token.type}='{curr_token.value}'>"
                print(formatted_str, end=" ")
                current_token += 1
            print()
