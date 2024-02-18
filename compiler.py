import argparse
import os

from lexer import Lexer

defaultSourceFile = './RAT24S_programs/RAT24S.source'

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('source_code', metavar='Path to source code file', type=str,
                    nargs='?', default=defaultSourceFile)

    path = parser.parse_args().source_code
    with open(path, 'r') as sourceFile:
        sourceCode = sourceFile.read()
        print('='*32, " Source Code ", '='*33)
        print(sourceCode)
        print('='*80, '\n')
        l = Lexer(sourceCode)
        tokens = l.tokenize()
        valid_tokens = [token for token in tokens if token.type != 'invalid']
        invalid_tokens = [token for token in tokens if token.type == 'invalid']
        print(f"Token count: {len(valid_tokens)}\n")
        print(valid_tokens)
        if len(invalid_tokens):
            print(f"\nInvalid Token count: {len(invalid_tokens)}\n")
            print(invalid_tokens)

if __name__ == "__main__":
    main()
