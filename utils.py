"""Utility functions used in compiler"""

def print_source_code(sourceCode):
    """Print the source code used by the compiler"""
    print('='*32, " Source Code ", '='*33)
    print(sourceCode)
    print('='*80, '\n')
    
def print_formatted_tokens(tokens, l):
    """Print tokens in same format as source code"""
    token_count = len([token for token in tokens if token.type != 'invalid'])
    print('='*32, f" Tokens ({token_count}) ", '='*33)
    l.print_tokens()
    print('='*80)