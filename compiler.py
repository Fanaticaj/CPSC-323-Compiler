import utils
from lexer import Lexer
from rdp import RDP

def main(path, print_tokens, tokens_filename, print_prods, out_filename,
         sym_table_filename, asm_filename, print_arg_help, *, supress_print=False):
    # Read source code
    with open(path, mode='r', encoding='utf-8-sig') as source_file:
        source_code = source_file.read()

    # Parse tokens using lexer
    lexical_analyzer = Lexer(source_code)

    # Save tokens to file if user used --save-tokens arg
    if tokens_filename:
        lexical_analyzer.save_tokens(tokens_filename)

    # Print source code and tokens if user used --print-tokens arg
    if print_tokens:
        utils.print_source_code(source_code)
        lexical_analyzer.print_tokens()

    # Use recursive descent parser to check valid syntax
    rdp_parser = RDP(lexical_analyzer, print_to_console=print_prods,
                     out_filename=out_filename)

    # Check if source code is valid RAT24S program
    is_valid_program = rdp_parser.rat24s()
    if not supress_print:
        if is_valid_program:
            print("Valid RAT24S program")
        else:
            print("Invalid RAT24S program")

    # Write symbol table to a file if user included --symbol-table arg
    if sym_table_filename:
        rdp_parser.write_symbol_table(sym_table_filename)

    # Check if any arg was used
    used_arg = False
    if print_tokens:
        used_arg = True
    elif tokens_filename:
        used_arg = True
    elif print_prods:
        used_arg = True
    elif out_filename:
        used_arg = True
    elif sym_table_filename:
        used_arg = True
    elif asm_filename:
        used_arg = True

    # Let user know how to save productions if no args passed
    if not used_arg and not supress_print:
        print()
        print_arg_help()

if __name__ == "__main__":
    args = utils.parse_arguments()
    main(*args)