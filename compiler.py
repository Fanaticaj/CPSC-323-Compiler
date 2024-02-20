import argparse
import os

from lexer import Lexer

defaultSourceFile = './RAT24S_programs/RAT24S.source'

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('source_code', metavar='Path to source code file', type=str,
                    nargs='?', default=defaultSourceFile)

    # Read source code
    path = parser.parse_args().source_code
    with open(path, 'r') as sourceFile:
        sourceCode = sourceFile.read()

    # Print unmodified source code
    print('='*32, " Source Code ", '='*33)
    print(sourceCode)
    print('='*80, '\n')

    # Lexical analysis
    l = Lexer(sourceCode)
    tokens = l.tokenize()

    # Print tokens returned by lexer
    token_count = len([token for token in tokens if token.type != 'invalid'])
    print('='*32, f" Tokens ({token_count}) ", '='*33)
    l.print_tokens()
    print('='*80, '\n')

if __name__ == "__main__":
    main()
