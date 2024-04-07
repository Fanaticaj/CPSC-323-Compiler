import utils
from lexer import Lexer
from rdp import RDP

def main(path, print_all, print_tokens, tokens_filename, print_prods, out_filename):
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
    args = utils.parse_arguments()
    main(*args)
