import argparse
import os
from pathlib import Path

from lexer import Lexer

# If user does not input source file, defaultSourceFile will be used instead
defaultSourceFile = './RAT24S_programs/RAT24S.source'
tokenOutputExt = '_tokens.txt' # Append tokenOutputExt to token files when saving tokens

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
    arg_parser = argparse.ArgumentParser()

    # Path to source code file arg
    arg_parser.add_argument('source_code', metavar='SourceCodeFilePath', type=str,
                    nargs='?', default=defaultSourceFile,
                    help="Path to the source code file that will be compiled")

    # Arg to print source code and tokens
    arg_parser.add_argument('-p', '--print-all', action='store_true',
                    default=False, help="print source code and tokens")
    # Arg to print tokens only
    arg_parser.add_argument('-t', '--print-tokens', action='store_true',
                    default=False, help="print tokens returned by lexer")
    # Arg to specify output file (optional)
    arg_parser.add_argument('-o', '--output', action='store', default=None,
                    help="Specify output file")

    # Parse command-line arguments
    path = Path(arg_parser.parse_args().source_code)
    print_all = arg_parser.parse_args().print_all
    print_tokens = arg_parser.parse_args().print_tokens
    output_arg = arg_parser.parse_args().output

    # Read source code
    with open(path, 'r') as sourceFile:
        sourceCode = sourceFile.read()

    # Parse tokens using lexer
    lexical_analyzer = Lexer(sourceCode)
    tokens = lexical_analyzer.tokenize()

    # Save tokens to txt file
    if output_arg:
        output_path = output_arg
    else:
        output_file = f"{path.stem}{tokenOutputExt}"
        output_path = f"{path.cwd()}/{output_file}"

    # Clear output file if already exists and write headers
    with open(output_path, 'w') as tokens_txt:
        tokens_txt.write(f"{'Token':15}Lexeme\n\n")

    # Append each token to output file
    with open(output_path, 'a') as tokens_txt:
        for token in tokens:
            tokens_txt.write(f"{token.type:15}{token.value}\n")

    # Print unmodified source code
    if print_all:
        print_source_code(sourceCode)

    # Print tokens returned by lexer
    if print_all or print_tokens:
        print_formatted_tokens(tokens, lexical_analyzer)

if __name__ == "__main__":
    main()
