"""Utility functions used in compiler"""
import argparse
from pathlib import Path

def print_source_code(sourceCode):
    """Print the source code used by the compiler"""
    print('='*32, " Source Code ", '='*33)
    print(sourceCode)
    print('='*80, '\n')
    
def parse_arguments():
    """Parse command-line arguments using argparse and return arguments"""
    arg_parser = argparse.ArgumentParser()

    # Path to source code file arg
    arg_parser.add_argument('source_code', metavar='source file', type=str,
                    help="Path to the source code file that will be compiled")

    # Arg to print tokens only
    arg_parser.add_argument('--print-tokens', action='store_true',
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
    # ARg to save symbol table to a file
    arg_parser.add_argument('--symbol-table', action='store',
                            default=None, help="Save symbol table to a file")
    
    # Arg to save assembly code and symbol table to a file
    arg_parser.add_argument('-o', '--output', action='store',
                            default=None, help="Save assembly code and symbol table to output file")

    # Parse command-line arguments
    path = Path(arg_parser.parse_args().source_code)
    print_tokens = arg_parser.parse_args().print_tokens
    tokens_filename = arg_parser.parse_args().save_tokens
    print_prods = arg_parser.parse_args().print_productions
    prods_filename = arg_parser.parse_args().save_productions
    sym_table_filename = arg_parser.parse_args().symbol_table
    asm_filename = arg_parser.parse_args().output

    return path, print_tokens, tokens_filename, print_prods, prods_filename, sym_table_filename, asm_filename, arg_parser.print_help