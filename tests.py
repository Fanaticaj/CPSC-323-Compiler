import os
import unittest

from compiler import main
from lexer import Lexer
from parse_token import Token
from rdp import RDP
from sym_table import Symbol, SymbolTable

class TestToken(unittest.TestCase):
    """Test Token class"""
    def test_valid_types(self):
        """Test that all valid types create Token"""
        valid_types = ['identifier', 'illegal', 'integer', 'keyword',
                        'operator', 'real', 'separator']
        # Create token with each type of valid type
        # Test will fail if there is an error raise by Token class
        for t in valid_types:
            tok = Token(t, 'random val')

    def test_invalid_type(self):
        """
        Test that Token class will raise error if user tries to create
        an invalid token type
        """
        invalid_type = "fake_type"
        raised_err = False
        try:
            tok = Token(invalid_type, 'random val')
        except ValueError:
            # ValueError was raised, test passed
            raised_err = True
        self.assertTrue(raised_err, "Token class did not raise error when user created token with invalid type.")

    def test_uppercase_to_lowercase(self):
        """
        Test that Token class will convert upper case characters to lowercase
        """
        upper_val = "MyVarIsUPPER"
        lower_val = "myvarisupper"
        tok = Token('identifier', upper_val)
        self.assertEqual(tok.value, lower_val)

class TestLexer(unittest.TestCase):
    """Test that lexer works"""

    def test_get_next_token(self):
        """Test that get_next_token returns one token at a time"""
        source_code = "$function convertx (fahr integer)"
        l = Lexer(source_code)
        tokens = l.tokenize()

        res = []
        for i in range(8):  # Test 1 more than length of tokens to check that it return None
            curr_token = l.get_next_token()
            res.append(curr_token)

        tokens.append(None)  # Add None to tokens since res should have None at end
        self.assertEqual(tokens, res)

    def test_comments(self):
        """Test that comments are removed and not tokenized"""
        source_code = "[* This is a one line comment *]"
        l = Lexer(source_code)
        tokens = l.tokenize()

        token_count = len(tokens)
        self.assertEqual(token_count, 0)

    def test_keywords(self):
        """Test that keywords are tokenized as keywords"""
        source_code = "boolean         else            endif"
        l = Lexer(source_code)
        tokens = l.tokenize()
        expected_tokens = [Token(type='keyword', value='boolean'), Token(type='keyword', value='else'), Token(type='keyword', value='endif')]

        self.assertEqual(tokens, expected_tokens)

    def test_separators(self):
        """Test that separators are tokenized as separators"""
        source_code = "(){},;$"
        l = Lexer(source_code)
        tokens = l.tokenize()
        expected_tokens = [
                Token(type='separator', value='('), Token(type='separator', value=')'), Token(type='separator', value='{'), Token(type='separator', value='}'),
                Token(type='separator', value=','), Token(type='separator', value=';'), Token(type='separator', value='$')
            ]

        self.assertEqual(tokens, expected_tokens)

    def test_operators(self):
        """Test that operators are tokenized as operators"""
        source_code = "+ - * / == != > < <= => ="
        l = Lexer(source_code)
        tokens = l.tokenize()
        expected_tokens = [
                Token(type='operator', value='+'), Token(type='operator', value='-'), Token(type='operator', value='*'), Token(type='operator', value='/'),
                Token(type='operator', value='=='), Token(type='operator', value='!='), Token(type='operator', value='>'), Token(type='operator', value='<'),
                Token(type='operator', value='<='), Token(type='operator', value='=>'), Token(type='operator', value='=')
            ]

        self.assertEqual(tokens, expected_tokens)

    def test_identifiers(self):
        """Test that identifiers are tokenized as identifiers"""
        source_code = "abc123 testIdentifier variable_1"
        l = Lexer(source_code)
        tokens = l.tokenize()
        expected_tokens = [Token(type='identifier', value='abc123'), Token(type='identifier', value='testidentifier'), Token(type='identifier', value='variable_1')]

        self.assertEqual(tokens, expected_tokens)

    def test_integers(self):
        """Test that integers are tokenized as integers"""
        source_code = "7 153 1849375932"
        l = Lexer(source_code)
        tokens = l.tokenize()
        expected_tokens = [Token(type='integer', value='7'), Token(type='integer', value='153'), Token(type='integer', value='1849375932')]

        self.assertEqual(tokens, expected_tokens)

    def test_reals(self):
        """Test that reals are tokenized as reals"""
        source_code = "3.14 22.5 0.99 25.0 26. .009"
        l = Lexer(source_code)
        tokens = l.tokenize()
        expected_tokens = [
                Token(type='real', value='3.14'), Token(type='real', value='22.5'), Token(type='real', value='0.99'), Token(type='real', value='25.0'),
                Token(type='illegal', value='26.'), Token(type='illegal', value='.009')
            ]

        self.assertEqual(tokens, expected_tokens)
        
class TestRDP(unittest.TestCase):
    """Test recursive descent parser"""
    
    def test_rat24s(self):
        """
        R1. <Rat24S> ::= $ <Opt Function Definitions> $ <Opt Declaration List> $ <Statement List> $
        """
        programs = [
            '$ $ $ print (true); $',
            '$ function myvar () { print (true); } $ $ print (true); $',
            '$ $ integer myint ; $ print (true); $',
            '$ function myvar () { print (true); } $ integer myint ; $ print (true);$'
        ]
        
        for program in programs:
            l = Lexer(program)
            parser = RDP(l)
            is_program = parser.rat24s()
            self.assertTrue(is_program, f"Not recognized as rat24s program: {program}")
            self.assertEqual(l.curr_token, len(l.tokens), f"Did not parse all tokens {l.curr_token}/{len(l.tokens)} in str: {program}")

            
    def test_opt_function_definitions(self):
        """
        R2. <Opt Function Definitions> ::= <Function Definitions> | <Empty>
        """
        tests = [
            '', # Empty
            'function myvar () { print (true); }'
        ]
        
        for t in tests:
            l = Lexer(t)
            parser = RDP(l)
            is_opt_function_definition = parser.opt_function_definitions()
            self.assertTrue(is_opt_function_definition, f"Not recognized as Opt Function Definitions: {t}")
            self.assertEqual(l.curr_token, len(l.tokens), f"Did not parse all tokens {l.curr_token}/{len(l.tokens)} in str: {t}")
        
    def test_function_definitions(self):
        """
        R3. <Function Definitions> ::= <Function> | <Function> <Function Definitions>
        """
        function_defs = [
            'function myvar () { print (true); }',
            'function myvar () { print (true); } function mysecondvar () { print (false); }'
        ]
        
        for func_def in function_defs:
            l = Lexer(func_def)
            parser = RDP(l)
            is_func_def = parser.function_definitions()
            self.assertTrue(is_func_def, f"Not recognized as function definitions: {func_def}")
            self.assertEqual(l.curr_token, len(l.tokens), f"Did not parse all tokens {l.curr_token}/{len(l.tokens)} in str: {func_def}")
            
    def test_function(self):
        """
        R4. <Function> ::= function <Identifier> ( <Opt Parameter List> ) <Opt Declaration List> <Body>
        """
        funcs = [
            "function myfunc () {print(myvar * 3 + 1);}",
            "function myfunc (myid integer) {print(myvar * 3 + 1);}",
            "function myfunc () real myvar, myvar2 ;  {print(myvar * 3 + 1);}",
        ]
        
        for func in funcs:
            l = Lexer(func)
            parser = RDP(l)
            is_func = parser.function()
            self.assertTrue(is_func, f"Not recognized as a function: {func}")
            self.assertEqual(l.curr_token, len(l.tokens), f"Did not parse all tokens {l.curr_token}/{len(l.tokens)} in str: {func}")
            
    def test_opt_parameter_list(self):
        """
        R5. <Opt Parameter List> ::= <Parameter List> | <Empty>
        """
        param_lists = [
            '', # Empty
            'istrue boolean',
        ]
        
        for opt_param_list in param_lists:
            l = Lexer(opt_param_list)
            parser = RDP(l)
            is_opt_param_list = parser.opt_parameter_list()
            self.assertTrue(is_opt_param_list, f"Not recognized as Opt Parameter List: {opt_param_list}")
            self.assertEqual(l.curr_token, len(l.tokens), f"Did not parse all tokens {l.curr_token}/{len(l.tokens)} in str: {opt_param_list}")
            
    def test_parameter_list(self):
        """
        R6. <Parameter List> ::= <Parameter> | <Parameter> , <Parameter List>
        """
        param_lists = [
            'myint integer',
            'myint integer , mybool boolean'
        ]
        
        for param_list in param_lists:
            l = Lexer(param_list)
            parser = RDP(l)
            is_param_list = parser.parameter_list()
            self.assertTrue(is_param_list, f"Not recognized as Parameter List: {param_list}")
            self.assertEqual(l.curr_token, len(l.tokens), f"Did not parse all tokens {l.curr_token}/{len(l.tokens)} in str: {param_list}")
            
    def test_parameter(self):
        """
         R7. <Parameter> ::= <IDs> <Qualifier>
        """
        param = 'myint integer'
        l = Lexer(param)
        parser = RDP(l)
        is_param = parser.parameter()
        self.assertTrue(is_param, f"Not recognized as parameter: {param}")
        self.assertEqual(l.curr_token, len(l.tokens), f"Did not parse all tokens {l.curr_token}/{len(l.tokens)} in str: {param}")
        
    def test_qualifier(self):
        """
        R8. <Qualifier> ::= integer | boolean | real
        """
        qualifiers = ['integer', 'boolean', 'real']
        for q in qualifiers:
            l = Lexer(q)
            parser = RDP(l)
            is_qualifier = parser.qualifier()
            self.assertTrue(is_qualifier, f"Not recognized as qualifier: {q}")
            self.assertEqual(l.curr_token, len(l.tokens), f"Did not parse all tokens {l.curr_token}/{len(l.tokens)} in str: {qualifiers}")
            
    def test_body(self):
        """
        R8. <Body> ::= { <Statement List> }
        """
        body = '{ print (42); }'
        l = Lexer(body)
        parser = RDP(l)
        is_body = parser.body()
        self.assertTrue(is_body, f"Not recognized as Body: {body}")
        self.assertEqual(l.curr_token, len(l.tokens), f"Did not parse all tokens {l.curr_token}/{len(l.tokens)} in str: {body}")
        
    def test_opt_declaration_list(self):
        """
        R9. <Opt Declaration List> ::= <Declaration List> | <Empty>
        """
        opt_dec_lists = [
            '', # Empty\
            'integer count;'
        ]
        
        for odl in opt_dec_lists:
            l = Lexer(odl)
            parser = RDP(l)
            is_opt_declartion_list = parser.opt_declaration_list()
            self.assertTrue(is_opt_declartion_list, f"Not recognized as Opt Declaration List: {odl}")
            self.assertEqual(l.curr_token, len(l.tokens), f"Did not parse all tokens {l.curr_token}/{len(l.tokens)} in str: {odl}")
            
    def test_declaration_list(self):
        """
        R10. <Declaration List> := <Declaration> ; | <Declaration> ; <Declaration List>
        """
        dec_lists = [
            'real myrealvar ;',
            'boolean myboolvar ; real myrealvar ;'
        ]
        
        for dec_list in dec_lists:
            l = Lexer(dec_list)
            parser = RDP(l)
            is_dec_list = parser.declaration_list()
            self.assertTrue(is_dec_list, f"Not recognized as Declaration List: {dec_list}")
            self.assertEqual(l.curr_token, len(l.tokens), f"Did not parse all tokens {l.curr_token}/{len(l.tokens)} in str: {dec_list}")
            
    def test_declaration(self):
        """
        R11. <Declaration> ::= integer <IDs> | boolean <IDs> | real <IDs>
        """
        declarations = [
            'integer myint',
            'boolean mybool',
            'real myreal'
        ]
        
        for dec in declarations:
            l = Lexer(dec)
            parser = RDP(l)
            is_dec = parser.declaration()
            self.assertTrue(is_dec, f"Not recognized as Declaration: {dec}")
            self.assertEqual(l.curr_token, len(l.tokens), f"Did not parse all tokens {l.curr_token}/{len(l.tokens)} in str: {dec}")
            
    def test_IDs(self):
        """
        R12. <IDs> ::= <Identifier> | <Identifier>, <IDs>
        """
        ids = [
            'myvar123',
            'myvar456, myvar123',
            'myvar456, myvar123, myvar789'
        ]
        
        for id in ids:
            l = Lexer(id)
            parser = RDP(l)
            is_IDs = parser.IDs()
            self.assertTrue(is_IDs, f"Not recognized as IDs: {id}")      
            self.assertEqual(l.curr_token, len(l.tokens), f"Did not parse all tokens {l.curr_token}/{len(l.tokens)} in str: {id}")
            
    def test_statement_list(self):
        """
        R13. <Statement List> ::= <Statement> | <Statement> <Statement List>
        """
        statement_lists = [
            'print (true);',
            'if ( 3 < 10 ) islessthan = true; endif print (true);'
        ]
        
        for statement_list in statement_lists:
            l = Lexer(statement_list)
            parser = RDP(l)
            is_statement_list = parser.statement_list()
            self.assertTrue(is_statement_list, f"Not recognized as Statement List: {statement_list}")
            self.assertEqual(l.curr_token, len(l.tokens), f"Did not parse all tokens {l.curr_token}/{len(l.tokens)} in str: {statement_list}")
            
    def test_statement(self):
        """
        R14. <Statement> ::= <Compound> | <Assign> | <If> | <Return> | <Print> | <Scan> | <While>
        """
        statements = [
            '{ scan (myvar); }', # <Compound>
            'myvar = 1;', # <Assign>
            'if ( 3 => 4 ) myvar = 1; endif', # <If>
            'return;', # <Return>
            'print ( false);', # <Print>
            'scan (myvar);', # <Scan>
            'while ( 3 < 1 ) { scan (myvar); } endwhile' # <While>
        ]
        
        for statement in statements:
            l = Lexer(statement)
            parser = RDP(l)
            parser.ignore_symbol_table = True
            is_statement = parser.statement()
            self.assertTrue(is_statement, f"Not recognized as Statement: {statement}")
            self.assertEqual(l.curr_token, len(l.tokens), f"Did not parse all tokens {l.curr_token}/{len(l.tokens)} in str: {statement}")

    def test_compound(self):
        """
        R15. <Compound> ::= { <Statement List> }
        """
        compound = '{ print (true); }'
        l = Lexer(compound)
        parser = RDP(l)
        is_compound = parser.compound()
        self.assertTrue(is_compound, f"Not recognized as Compound: {compound}")
        self.assertEqual(l.curr_token, len(l.tokens), f"Did not parse all tokens {l.curr_token}/{len(l.tokens)} in str: {compound}")
        
    def test_assign(self):
        """
        R16. <Assign> ::= <Identifier> = <Expression> ;
        """
        assign = "pi = 3.14 ;"
        l = Lexer(assign)
        parser = RDP(l)
        is_assign = parser.assign()
        self.assertTrue(is_assign, f"Not recognized as Assign: {assign}")
        self.assertEqual(l.curr_token, len(l.tokens), f"Did not parse all tokens {l.curr_token}/{len(l.tokens)} in str: {assign}")
        
    def test_If(self):
        """
        R17. <If> ::= if ( <Condition> ) <Statement> <If_prime>
        """
        if_statement = 'if ( 3 < 1 ) { scan (myvar); } endif'
        l = Lexer(if_statement)
        parser = RDP(l)
        is_If = parser.If()
        self.assertTrue(is_If, f"Not recognized as If: {if_statement}")
        self.assertEqual(l.curr_token, len(l.tokens), f"Did not parse all tokens {l.curr_token}/{len(l.tokens)} in str: {if_statement}")
        
    def test_If_prime(self):
        """
        R18. <If_prime> ::= endif | else <Statement> endif
        """
        if_primes = [
            'endif',
            'else { scan (myvar); } endif'
        ]
        
        for if_prime in if_primes:
            l = Lexer(if_prime)
            parser = RDP(l)
            is_If_prime = parser.If_prime()
            self.assertTrue(is_If_prime, f"Not recognized as If_prime: {if_prime}")
            self.assertEqual(l.curr_token, len(l.tokens), f"Did not parse all tokens {l.curr_token}/{len(l.tokens)} in str: {if_prime}")
            
    def test_Return(self):
        """
        R19. <Return> ::= return ; | return <Expression> ;
        """
        returns = [
            'return ;',
            'return 1 + 2 ;'
        ]
        
        for r in returns:
            l = Lexer(r)
            parser = RDP(l)
            is_return = parser.Return()
            self.assertTrue(is_return, f"Not recognized as Return: {r}")
            self.assertEqual(l.curr_token, len(l.tokens), f"Did not parse all tokens {l.curr_token}/{len(l.tokens)} in str: {r}")
            
    def test_Print(self):
        """
        R20. <Print> ::= print ( <Expression>);
        """
        print_statement = "print ( 1 + 2);"
        l = Lexer(print_statement)
        parser = RDP(l)
        is_Print = parser.Print()
        self.assertTrue(is_Print, f"Not recognized as Print: {print_statement}")
        self.assertEqual(l.curr_token, len(l.tokens), f"Did not parse all tokens {l.curr_token}/{len(l.tokens)} in str: {print_statement}")

    def test_scan(self):
        """
        R21. <Scan> ::= scan ( <IDs> );
        """
        source = "scan (var123);"
        l = Lexer(source)
        parser = RDP(l)
        is_scan = parser.scan()
        self.assertTrue(is_scan, f"Not recognized as scan: {source}")
        self.assertEqual(l.curr_token, len(l.tokens), f"Did not parse all tokens {l.curr_token}/{len(l.tokens)} in str: {source}")
        
    def test_While(self):
        """
        R22. <While> ::= while ( <Condition> ) <Statement> endwhile
        """
        source = "while (3 < 1) return; endwhile"
        l = Lexer(source)
        parser = RDP(l)
        is_while = parser.While()
        self.assertTrue(is_while, f"Not recognized as while: {source}")
        self.assertEqual(l.curr_token, len(l.tokens), f"Did not parse all tokens {l.curr_token}/{len(l.tokens)} in str: {source}")
        
    def test_condition(self):
        """
        R23. <Condition> ::= <Expression> <Relop> <Expression>
        """
        operators = ['==', '!=', '>', '<', '<=', '=>']
        for op in operators:
            condition = f"3 {op} 1"
            l = Lexer(condition)
            parser = RDP(l)
            is_condition = parser.condition()
            self.assertTrue(is_condition, f"Not recognized as condition: {condition}")
            self.assertEqual(l.curr_token, len(l.tokens), f"Did not parse all tokens {l.curr_token}/{len(l.tokens)} in str: {operators}")
    
    def test_relop(self):
        """
        R24. <Relop> ::= == | != | > | < | <= | =>
        """
        operators = ['==', '!=', '>', '<', '<=', '=>']
        for op in operators:
            source = op
            l = Lexer(source)
            parser = RDP(l)
            is_relop = parser.relop()
            self.assertTrue(is_relop, f"Not recognized as operator: {op}")
            self.assertEqual(l.curr_token, len(l.tokens), f"Did not parse all tokens {l.curr_token}/{len(l.tokens)} in str: {op}")
            
    def test_expression(self):
        """
        R25. <Expression> ::= <Term> <Expression_prime>
        """
        expressions = [
            "1 + 2",
        ]
        for exp in expressions:
            l = Lexer(exp)
            parser = RDP(l)
            is_exp = parser.expression()
            self.assertTrue(is_exp, f"Not recognized as expression: {exp}")
            self.assertEqual(l.curr_token, len(l.tokens), f"Did not parse all tokens {l.curr_token}/{len(l.tokens)} in str: {exp}")
            
    def test_expression_prime(self):
        """
        R26. <Expression_prime> ::= + <Term> <Expression_prime> | - <Term> <Expression_prime> | <Empty>
        """
        tests = [
            '', # Empty
            '+ 5',
            '- a',
        ]
        for t in tests:
            l = Lexer(t)
            parser = RDP(l)
            is_expression_prime = parser.expression_prime()
            self.assertTrue(is_expression_prime, f"Not recognized as expression prime: {t}")
            self.assertEqual(l.curr_token, len(l.tokens), f"Did not parse all tokens {l.curr_token}/{len(l.tokens)} in str: {t}")
            
    def test_term(self):
        """
        R27. <Term> ::= <Factor> <Term_prime>
        """
        terms = [
            '3',
            '4 * x',
        ]
        
        for term in terms:
            l = Lexer(term)
            parser = RDP(l)
            is_term = parser.term()
            self.assertTrue(is_term, f"Not recognized as term: {term}")
            self.assertEqual(l.curr_token, len(l.tokens), f"Did not parse all tokens {l.curr_token}/{len(l.tokens)} in str: {term}")
            
    def test_term_prime(self):
        """
        R28. <Term_prime> ::= * <Factor> <Term_prime> | / <Factor> <Term_prime> | <Empty>
        """
        term_primes = [
            '', # Empty
            '* 5',
            '/ a',
            '* 5 / a'
        ]
        
        for tp in term_primes:
            l = Lexer(tp)
            parser = RDP(l)
            is_term_prime = parser.term_prime()
            self.assertTrue(is_term_prime, f"Not recognized as term prime: {tp}")
            self.assertEqual(l.curr_token, len(l.tokens), f"Did not parse all tokens {l.curr_token}/{len(l.tokens)} in str: {tp}")
            
    def test_factor(self):
        """
        R29. <Factor> ::= - <Primary> | <Primary>
        """
        factors = [
            '- 3',
            'myvar123'
        ]
        
        for f in factors:
            l = Lexer(f)
            parser = RDP(l)
            is_factor = parser.factor()
            self.assertTrue(is_factor, f"Not recognized as factor: {f}")
            self.assertEqual(l.curr_token, len(l.tokens), f"Did not parse all tokens {l.curr_token}/{len(l.tokens)} in str: {f}")
            
    def test_primary(self):
        """
        R30. <Primary> ::= <Identifier> | <Integer> | <Identifier> ( <IDs> ) |
        ( <Expression> ) | <Real> | true | false        
        """
        primaries = [
            'myvar', # <Identifier>
            '123', # <Integer>
            'func(x)', # <Identifier> ( <IDs> )
            '(a + b)', # ( <Expression> )
            '45.67', # <Real>
            'true',
            'false'
        ]
        
        for p in primaries:
            l = Lexer(p)
            parser = RDP(l)
            is_primary = parser.primary()
            self.assertTrue(is_primary, f"Not recognized as primary: {p}")
            self.assertEqual(l.curr_token, len(l.tokens), f"Did not parse all tokens {l.curr_token}/{len(l.tokens)} in str: {p}")
            
    def test_empty(self):
        """
        R31. <Empty> ::= None
        """
        empty = ''
        l = Lexer(empty)
        parser = RDP(l)
        is_empty = parser.empty()
        self.assertTrue(is_empty, f"Not recognized as Empty: {empty}")
        self.assertEqual(l.curr_token, len(l.tokens), f"Did not parse all tokens {l.curr_token}/{len(l.tokens)} in str: {empty}")
        
    def test_output(self):
        """Run compiler with print_true.source program and check productions output"""
        exprected_res = [
            'Token: separator       Lexeme: $',
            '  <Rat24S> --> $ <Opt Function Definitions> $ <Opt Declaration List> $ <Statement List> $',
            '  <Opt Function Definitions> --> <Empty>',
            'Token: separator       Lexeme: $',
            '  <Opt Declaration List> --> <Empty>',
            'Token: separator       Lexeme: $',
            '  <Statement List> --> <Statement>',
            'Token: keyword         Lexeme: print',
            '  <Statement> --> <Print>',
            '  <Print> --> print ( <Expression>);',
            'Token: separator       Lexeme: (',
            '  <Expression> --> <Term> <Expression_prime>',
            '  <Term> --> <Factor> <Term_prime>',
            '  <Factor> --> <Primary>',
            'Token: keyword         Lexeme: true',
            '  <Primary> --> true',
            '  <Term_prime> --> <Empty>',
            '  <Expression_prime> --> <Empty>',
            'Token: separator       Lexeme: )',
            'Token: separator       Lexeme: ;',
            'Token: separator       Lexeme: $'
            ]
                
        # Save productions to temp_out file
        filepath = "RAT24S_programs/print_true.source"
        temp_out = "test_out.txt"

        # Raise error if temp_out file exists before running tests
        if os.path.isfile(temp_out):
            raise ValueError(f"{temp_out} already exists before running test")
        try:
            main(filepath, False, None, False, temp_out, None, supress_print=True)
        
            # Open temp_out file
            with open(temp_out) as txt:
                res = txt.read().strip().split('\n')
            self.assertEqual(res, exprected_res)
        finally:
            # Remove output file
            os.remove(temp_out)

    def test_symbol_table_arg(self):
        """
        Test that using the --symbol-table argument in the command line
        will save the symbol table correctly to a file
        """
        # Save symbol table to out file
        testcase_file = "RAT24S_programs/add_sum.txt"
        out_filename = "sym_table_out.txt"

        # Raise error if out_filename exists before running test
        if os.path.isfile(out_filename):
            raise ValueError(f"{out_filename} exists before testing")

        try:
            main(testcase_file, False, None, False, None, out_filename,
                supress_print=True)
            
            # Assert file was saved
            self.assertTrue(os.path.isfile(out_filename))

            # Open output file
            with open(out_filename) as out_txt:
                res = out_txt.read().split()
            expected_res = [
                'Identifier', 'Memory', 'Location', 'Type',
                'i', '1', 'integer',
                'max', '2', 'integer',
                'sum', '3', 'integer',
                'j', '4', 'boolean',
                'k', '5', 'boolean',
                'l', '6', 'boolean'
                ]

            self.assertEqual(res, expected_res)
        finally:
            # Remove test file
            os.remove(out_filename)

    def test_insert_integer_symbol(self):
        """
        Test that the RDP parser correctly inserts integer identifiers
        """
        # Integer declaration source code
        source = "integer count"
        l = Lexer(source)
        parser = RDP(l)

        # Run declaration method
        parser.declaration()

        # Assert that count integer was inserted
        expected_symbols = {
            Symbol(name='count', type='integer') : 1
            }
        self.assertEqual(parser.symbol_table.symbols, expected_symbols,
                         "Did not insert integer identifier to symbol table")
    
    def test_insert_boolean_symbol(self):
        """
        Test that RDP parser correctly inserts boolean identifiers
        """
        # Boolean delcaration source code
        source = "boolean is_cold"
        l = Lexer(source)
        parser = RDP(l)

        # Run declaration method
        parser.declaration()

        # Assert that boolean symbol was inserted
        expected_symbols = {
            Symbol(name='is_cold', type='boolean') : 1
        }

        self.assertEqual(parser.symbol_table.symbols, expected_symbols,
                         "Did not insert boolean identifier to symbol table ")

    def test_insert_declaration_list(self):
        """
        Test that RDP parser inserts all identifers when a single type defines
        more than one identifier.
        ie integer i, j, k;  <-- Should insert 3 symbols to table
        """
        source = "integer i, j, k;boolean l, m, n;"
        l = Lexer(source)
        parser = RDP(l)

        # Run declaration method
        parser.declaration_list()

        # Assert all identifers were inserted to symbol table
        expected_length = 6
        self.assertEqual(len(parser.symbol_table.symbols), expected_length,
                         "RDP parser does not insert all identifers in declartion list to symbol table")
 
        # Assert symbols are in correct order
        expected_symbols = {
            Symbol(name='i', type='integer') : 1,
            Symbol(name='j', type='integer') : 2,
            Symbol(name='k', type='integer') : 3,
            Symbol(name='l', type='boolean') : 4,
            Symbol(name='m', type='boolean') : 5,
            Symbol(name='n', type='boolean') : 6,
        }

        self.assertEqual(parser.symbol_table.symbols,  expected_symbols)

class TestSymbolTable(unittest.TestCase):
    """Test Symbol table methods"""
    def test_initial_mem_address(self):
        """Test that memory address starts at 1"""
        init_mem_address = 1
        symbol_table = SymbolTable()
        self.assertEqual(symbol_table.mem_address, init_mem_address)

    def test_exists_identifier(self):
        """
        Test exists_identifier method
        """
        id_tok = Token('identifier', 'count') # Will exist
        id_tok2 = Token('identifier', 'sum') # Will not exist
        sym_type = 'integer'

        symbol_table = SymbolTable()
        symbol_table.insert(id_tok, sym_type)

        self.assertTrue(symbol_table.exists_identifier(id_tok, sym_type))
        self.assertFalse(symbol_table.exists_identifier(id_tok2, sym_type))

    def test_insert_symbol(self):
        """Test inserting a symbol to the symbol table"""
        # Identifier token
        id_tok = Token('identifier', 'count')
        symbol_type = 'integer'

        # Insert symbol to table
        symbol_table = SymbolTable()
        symbol_table.insert(id_tok, symbol_type)

        # Assett symbol as added to symbol table
        expected_symbol_table = {
            Symbol(name='count', type='integer') : 1
            }
        self.assertEqual(symbol_table.symbols, expected_symbol_table)

        # Assert memory address was increased
        expected_mem_address = 2
        self.assertEqual(symbol_table.mem_address, expected_mem_address)

    def test_duplicate_err(self):
        """
        Test that symbol table will raise error if an identifier with same name
        and same type is inserted to the table more than once
        """
        id_tok = Token('identifier', 'count')
        id_tok2 = Token('identifier', 'count')
        sym_type = 'integer'

        symbol_table = SymbolTable()
        symbol_table.insert(id_tok, sym_type)

        with self.assertRaises(ValueError):
            symbol_table.insert(id_tok2, sym_type)

    def test_same_name_diff_type_entry(self):
        """
        Test that identifiers of the same name but different type can be 
        inserted to the symbol table
        """
        id_tok = Token('identifier', 'count')
        id_type = 'integer'
        id2_tok = Token('identifier', 'count')
        id2_type = 'identifier'

        symbol_table = SymbolTable()
        
        # Insert first identifier
        symbol_table.insert(id_tok, id_type)

        # Insert second identifier
        symbol_table.insert(id2_tok, id2_type)

        expected_symbols = {
            Symbol(name='count', type='integer'): 1,
            Symbol(name='count', type='identifier'): 2
            }
        
        self.assertEqual(symbol_table.symbols, expected_symbols)

    def test_write(self):
        """
        Test that write method correctly formats symbol table
        """
        # Identifier token : integer token  pairs for test
        symbol_pairs = [
            (Token('identifier', 'i'), 'integer'),
            (Token('identifier', 'max'), 'integer'),
            (Token('identifier', 'sum'), 'integer'),
        ]

        # Create symbol table
        symbol_table = SymbolTable()
        for id_tok, symbol_type in symbol_pairs:
            symbol_table.insert(id_tok, symbol_type)

        filename = "symbol_table_out.txt"
        # Raise error if filename already exists
        if os.path.isfile(filename):
            raise ValueError(f"{filename} already exists before testing")
        
        # Write to filename
        try:
            symbol_table.write(filename)

            # Assert that filename exists
            filename_exists = os.path.isfile(filename)
            self.assertTrue(filename_exists, "SymbolTable.write(filename) method does not output a file")

            # Conver filename to array for testing
            with open(filename) as f:
                output_arr = f.read().split()

            expected_output_arr = [
                'Identifier', 'Memory', 'Location', 'Type',
                'i', '1', 'integer',
                'max', '2', 'integer',
                'sum', '3', 'integer'
                ]
            
            self.maxDiff = None
            self.assertEqual(output_arr, expected_output_arr, "Write method did not write correct content")

        finally:
            # Remove test output file
            if os.path.isfile(filename):
                os.remove(filename)

    def test_append(self):
        """
        Test that write method can append to files
        """
        filename = "out_file.txt"
        # Raise error if output file exists before testing
        if os.path.isfile(filename):
            raise ValueError(f"{filename} already exists before test")
        try:
            # Write to file before appending
            with open(filename, 'w') as f:
                f.write("testing123...\n")

            # Create symbol table
            id_tok = Token('identifier', 'count')
            id_type = 'integer'
            symbol_table = SymbolTable()
            symbol_table.insert(id_tok, id_type)

            # Append to file
            symbol_table.write(filename, append_to_file=True)

            # Read output file
            with open(filename) as f:
                output_file = f.read().split()
            
            # Assert that file was appending to
            expected_output = [
                'testing123...',
                'Identifier', 'Memory', 'Location', 'Type',
                'count', '1', 'integer'
                ]
            
            self.assertEqual(output_file, expected_output,
                "Symbol table write method did not append to file when setting append_to_file=True")

        finally:
            # Remove file when done testing
            if os.path.isfile(filename):
                os.remove(filename)

    def test_non_identifier_err(self):
        """
        Test that symbol table raises error if user tries to insert non identifier token as identifier
        """
        # Create symbol table
        tok = Token('integer', '22')
        symbol_table = SymbolTable()

        # Insert non identifier symbol
        raised_err = False
        try:
            symbol_table.insert(tok, 'integer')
        except ValueError:
            raised_err = True
        self.assertTrue(raised_err, "Did not raise error when user inserted non identifier symbol")

    def test_get_mem_address(self):
        """
        Test that correct memory address is returned by get_mem_address method
        """
        # Setup symbol table
        id_tok = Token('identifier', 'count')
        id_type = 'integer'
        id_addr = 1
        id2_tok = Token('identifier', 'isfull')
        id2_type = 'boolean'
        id2_addr = 2
        symbol_table = SymbolTable()
        symbol_table.insert(id_tok, id_type)
        symbol_table.insert(id2_tok, id2_type)

        # Assert correct address is returned
        self.assertEqual(symbol_table.get_mem_address(id2_tok, id2_type), id2_addr)
        self.assertEqual(symbol_table.get_mem_address(id_tok, id_type), id_addr)

class TestAssemblyInstructions(unittest.TestCase):
    """Test that assembly instructions are generated correctly"""
    def test_assignment(self):
        """
        Test that correct assembly instructions are generated for assignment productions
        sum = 0;
        Should generate:
        1 PUSHI 0
        2 POPM 1
        """
        # Run parser with source code
        source = "integer sum;sum = 0;"
        l = Lexer(source)
        parser = RDP(l)
        # Run declaration_lsit first to update symbol table
        parser.declaration_list()
        # Run assign to update assembly instructions
        parser.assign()

        # Assert first instruction is: PUSHI 0
        correct_instruction = "PUSHI 0"
        actual_instruction = parser.asm_instructions[0]
        self.assertEqual(actual_instruction, correct_instruction)

        # Assert second instruction is: POPM 1
        correct_instruction = "POPM 1"
        actual_instruction = parser.asm_instructions[1]
        self.assertEqual(actual_instruction, correct_instruction)

if __name__ == "__main__":
    unittest.main()
