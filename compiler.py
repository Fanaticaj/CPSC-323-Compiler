import lexer
import argparse
import os

defaultSourceFile = './RAT24S.source'

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('source_code', metavar='Expected file', type=str,
                    nargs=1, default=defaultSourceFile)

    sourceFile = open(str(parser.parse_args().source_code[0]), 'r')
    sourceCode = sourceFile.read()
    l = lexer.Lexer(sourceCode)
    l.validate()


if __name__ == "__main__":
    main()