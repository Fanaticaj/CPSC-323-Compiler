import argparse
import os

from lexer import Lexer

defaultSourceFile = './RAT24S_programs/RAT24S.source'

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

def main():
    parser = argparse.ArgumentParser()

    # Path to source code file arg
    parser.add_argument('source_code', metavar='SourceCodeFilePath', type=str,
                    nargs='?', default=defaultSourceFile,
                    help="Path to the source code file that will be compiled")

    # Arg to print source code and tokens
    parser.add_argument('-p', '--print-all', action='store_true',
                    default=False, help="print source code and tokens")
    # Arg to print tokens only
    parser.add_argument('-t', '--print-tokens', action='store_true',
                    default=False, help="print tokens returned by lexer")

    # Parse arguments
    path = parser.parse_args().source_code
    print_all = parser.parse_args().print_all
    print_tokens = parser.parse_args().print_tokens

    # Read source code
    with open(path, 'r') as sourceFile:
        sourceCode = sourceFile.read()

    # Parse tokens using lexer
    lexical_analyzer = Lexer(sourceCode)
    tokens = lexical_analyzer.tokenize()

    # Print unmodified source code
    if print_all:
        print_source_code(sourceCode)

    # Print tokens returned by lexer
    if print_all or print_tokens:
        print_formatted_tokens(tokens, lexical_analyzer)

if __name__ == "__main__":
    main()
