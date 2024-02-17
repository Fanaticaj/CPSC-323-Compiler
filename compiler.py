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
        print(f"Token count: {len(tokens)}\n")
        print(tokens)

if __name__ == "__main__":
    main()
