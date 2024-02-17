import argparse
import os

import lexer

defaultSourceFile = './RAT24S_programs/RAT24S.source'

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('source_code', metavar='Path to source code file', type=str,
                    nargs=1, default=defaultSourceFile)

    path = parser.parse_args().source_code
    with open(path, 'r') as sourceFile:
        sourceCode = sourceFile.read()
        print(sourceCode)
        l = lexer.Lexer(sourceCode)
        print(l.tokenize())

if __name__ == "__main__":
    main()
