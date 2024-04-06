import re

from fsm import FSM
from parse_token import Token

class Lexer:
    """
    This Lexer class is the lexer for the compiler.
    It takes source code as input and outputs a list of Tokens.
    There are 7 kinds of tokens:
    keywords, separators, operators, identifiers, integers, reals, and illegals
    """

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
        'endwhile'  : 'keyword',
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
        '=>'        : 'operator',
        #---------- Operator ----------#
    }

    def __init__(self, sourceCode):
        self.sourceCode = sourceCode
        self.tokens = []
        self.curr_token = 0  # Used to iterate through tokens by get_next_token method
        # Tokenize on initialization
        self.tokenize()

    def tokenize(self):
        """
        This function is used to validate and tokenize the source code.
        This will be called from the compiler.py file.

        Parameters:
        None

	Returns:
	list: A list of tokens identified in the source code.
        """

        self.tokens = []  # Clear tokens list incase tokenize method is run more than once

	# Remove comments from source code
        re_comments = r'\[\*[\s\S]*?\*\]'
        self.sourceCode = re.sub(re_comments, '', self.sourceCode)

        # Split source code into tokens
        re_operators = r'==|!=|<=|=>|\+|\-|\*|\/|<|>|='
        re_separators = r'\(|\)|\{|\}|\,|\;|\$|\s'
        re_split_pattern = f'({re_operators})|({re_separators})'
        potentialTokens = [token for token in re.split(re_split_pattern, self.sourceCode) if token and not token.isspace()]

        token_checker_fsm = FSM()

        # Iterate through each token checking if a match is found
        for token in potentialTokens:
            if token in self.symbols:
                self.tokens.append(Token(self.symbols[token], token))

            elif token_checker_fsm.is_identifier(token): # Identifier
                self.tokens.append(Token('identifier', token))

            elif token_checker_fsm.is_integer(token): # Integer
                self.tokens.append(Token('integer', token))

            elif token_checker_fsm.is_real(token): # Real
                self.tokens.append(Token('real', token))

            else:
                self.tokens.append(Token('illegal', token))

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
            re_operators = r'==|!=|<=|=>|\+|\-|\*|\/|<|>|='
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

    def get_next_token(self):
        """
        Return the token at curr_token position and increment curr_token.
        Return None once all tokens have been returned.
        This method is needed for syntax analyzer since it must iterate through tokens one by one.
        """
        if self.curr_token >= len(self.tokens):
            return None

        next_token = self.tokens[self.curr_token]
        self.curr_token += 1

        return next_token

    def peek_next_token(self):
        if self.curr_token >= len(self.tokens):
            return None
        return self.tokens[self.curr_token]
    
    def backtrack(self):
        """Backtrack one position"""
        if self.curr_token == 0:
            return
        
        self.curr_token -= 1
        
    def get_prev_token(self):
        """
        Return the previous token.
        Used when you need token value of token that you just checked in RDP
        Ex:
        if token_is('identifier', 'myvar'):
            token = lexer.get_prev_token()
            print(token.value)
        """
        idx = self.curr_token - 1
        
        if self.curr_token == 0:
            idx = 0
        
        return self.tokens[idx]
    
    def get_next_token_val(self):
        """Return the value of the next token"""
        if self.curr_token >= len(self.tokens):
            return ''
        next_token = self.tokens[self.curr_token]
        return next_token.value