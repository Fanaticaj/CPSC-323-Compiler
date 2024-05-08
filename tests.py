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
        main(filepath, False, None, False, temp_out)
        
        # Open temp_out file
        with open(temp_out) as txt:
            res = txt.read().strip().split('\n')
        self.assertEqual(res, exprected_res)

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
            Token(type='identifier', value='count'): Symbol(mem_address=1, type='integer')
            }
        self.assertEqual(parser.symbol_table.symbols, expected_symbols)

class TestSymbolTable(unittest.TestCase):
    """Test Symbol table methods"""
    def test_initial_mem_address(self):
        """Test that memory address starts at 1"""
        init_mem_address = 1
        symbol_table = SymbolTable()
        self.assertEqual(symbol_table.mem_address, init_mem_address)

    def test_insert_symbol(self):
        """Test inserting a symbol to the symbol table"""
        # Identifier token
        id_tok = Token('identifier', 'count')

        # Insert symbol to table
        symbol_table = SymbolTable()
        symbol_table.insert(id_tok, 'integer')

        # Assett symbol as added to symbol table
        expected_symbol_table = {
            Token(type='identifier', value='count'): Symbol(mem_address=1, type='integer')
            }
        self.assertEqual(symbol_table.symbols, expected_symbol_table)

        # Assert memory address was increased
        expected_mem_address = 2
        self.assertEqual(symbol_table.mem_address, expected_mem_address)

    def test_update_symbol(self):
        """
        Test that inserting an existing symbol will only update the value and 
        not increase the memory address
        """
        # Identifier token
        id_tok = Token('identifier', 'count')

        # Insert symbol to table first time
        symbol_table = SymbolTable()
        symbol_type = 'integer'
        symbol_table.insert(id_tok, symbol_type)

        # Update count identifer
        symbol_table.insert(id_tok, symbol_type)

        # Check that memory address of identifier is still 1
        intial_mem_address = 1
        mem_address = symbol_table.symbols[id_tok].mem_address
        self.assertEqual(mem_address, intial_mem_address)

    def test_update_wront_type_err(self):
        """
        Test that symbol table will raise error is user tries to update a 
        symbol with a value of different type than what the corrent value is
        """
        # Identifier token
        id_tok = Token('identifier', 'count')
        symbol_type = 'integer'
        second_type = 'identifier'

        # Insert symbol to table first time
        symbol_table = SymbolTable()
        symbol_table.insert(id_tok, symbol_type)

        # Assert that error is raised
        err_was_raised = False
        try:
            symbol_table.insert(id_tok, second_type)
        except ValueError as err:
            err_was_raised = True
        self.assertTrue(err_was_raised, "Error not raised when assigning symbol a different type")

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

if __name__ == "__main__":
    unittest.main()
