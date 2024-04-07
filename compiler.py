import argparse
from pathlib import Path

import utils
from lexer import Lexer
from rdp import RDP

# Append tokenOutputExt to token files when saving tokens
tokenOutputExt = '_tokens.txt'

def main():
    arg_parser = argparse.ArgumentParser()

    # Path to source code file arg
    arg_parser.add_argument('source_code', metavar='SourceCodeFilePath', type=str,
                    help="Path to the source code file that will be compiled")

    # Arg to print source code and tokens
    arg_parser.add_argument('-p', '--print-all', action='store_true',
                    default=False, help="print source code and tokens")
    # Arg to print tokens only
    arg_parser.add_argument('-t', '--print-tokens', action='store_true',
                    default=False, help="print tokens returned by lexer")
    # Arg to specify output file (optional)
    arg_parser.add_argument('--save-tokens', action='store', default=None,
                    help="Specify output file for tokens")
    # Arg to print proudctions to console
    arg_parser.add_argument('--print-productions', action='store_true',
                            default=False, help='Print productions to console')
    # Arg to save RDP productions to file
    arg_parser.add_argument('-s', '--save-productions', action='store',
                            default=None, help="Save syntax analyzer productions to a file")

    # Parse command-line arguments
    path = Path(arg_parser.parse_args().source_code)
    print_all = arg_parser.parse_args().print_all
    print_tokens = arg_parser.parse_args().print_tokens
    tokens_filename = arg_parser.parse_args().save_tokens
    print_prods = arg_parser.parse_args().print_productions
    out_filename = arg_parser.parse_args().save_productions

    # Read source code
    with open(path, mode='r', encoding='utf-8-sig') as sourceFile:
        sourceCode = sourceFile.read()

    # Parse tokens using lexer
    lexical_analyzer = Lexer(sourceCode)

    if tokens_filename:
        lexical_analyzer.save_tokens(tokens_filename)

    # Print unmodified source code
    if print_all:
        utils.print_source_code(sourceCode)

    # Print tokens returned by lexer
    if print_all or print_tokens:
        lexical_analyzer.print_tokens()

    rdp_parser = RDP(lexical_analyzer, print_to_console=print_prods, out_filename=out_filename)
    is_valid_program = rdp_parser.rat24s()
    if is_valid_program:
        print("Valid RAT24S program")
    else:
        print("Invalid RAT24S program")
        
if __name__ == "__main__":
    main()
