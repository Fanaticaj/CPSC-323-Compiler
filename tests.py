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
            parser.ignore_symbol_table = True
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
            parser.ignore_symbol_table = True
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
        parser.ignore_symbol_table = True
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
        parser.ignore_symbol_table = True
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
            parser.ignore_symbol_table = True
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
        parser.ignore_symbol_table = True
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
        parser.ignore_symbol_table = True
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
            parser.ignore_symbol_table = True
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
            parser.ignore_symbol_table = True
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
            parser.ignore_symbol_table = True
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
            parser.ignore_symbol_table = True
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
            parser.ignore_symbol_table = True
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
            parser.ignore_symbol_table = True
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
            'count' : Symbol(mem_address=5000, type='integer')
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
            'is_cold' : Symbol(mem_address=5000, type='boolean')
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
            'i' : Symbol(mem_address=5000, type='integer'),
            'j' : Symbol(mem_address=5001, type='integer'),
            'k' : Symbol(mem_address=5002, type='integer'),
            'l' : Symbol(mem_address=5003, type='boolean'),
            'm' : Symbol(mem_address=5004, type='boolean'),
            'n' : Symbol(mem_address=5005, type='boolean'),
        }

        self.assertEqual(parser.symbol_table.symbols,  expected_symbols)

class TestSymbolTable(unittest.TestCase):
    """Test Symbol table methods"""
    def test_initial_mem_address(self):
        """Test that memory address starts at 5000"""
        init_mem_address = 5000
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

        self.assertTrue(symbol_table.exists_identifier(id_tok))
        self.assertFalse(symbol_table.exists_identifier(id_tok2))

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
            'count' : Symbol(mem_address=5000, type='integer')
            }
        self.assertEqual(symbol_table.symbols, expected_symbol_table)

        # Assert memory address was increased
        expected_mem_address = 5001
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
                'i', '5000', 'integer',
                'max', '5001', 'integer',
                'sum', '5002', 'integer'
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
                'count', '5000', 'integer'
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
        id_addr = 5000
        id2_tok = Token('identifier', 'isfull')
        id2_type = 'boolean'
        id2_addr = 5001
        symbol_table = SymbolTable()
        symbol_table.insert(id_tok, id_type)
        symbol_table.insert(id2_tok, id2_type)

        # Assert correct address is returned
        self.assertEqual(symbol_table.get_mem_address(id2_tok), id2_addr)
        self.assertEqual(symbol_table.get_mem_address(id_tok), id_addr)

class TestCompiler(unittest.TestCase):
    """
    Test compiler.py module. Mainly test argument parsing and output
    """
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
            main(filepath, False, None, False, temp_out, None, None, None,
                 supress_print=True)
        
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
                 None, None, supress_print=True)
            
            # Assert file was saved
            self.assertTrue(os.path.isfile(out_filename))

            # Open output file
            with open(out_filename) as out_txt:
                res = out_txt.read().split()
            expected_res = [
                'Identifier', 'Memory', 'Location', 'Type',
                'i', '5000', 'integer',
                'max', '5001', 'integer',
                'sum', '5002', 'integer',
                'j', '5003', 'boolean',
                'k', '5004', 'boolean',
                'l', '5005', 'boolean'
                ]

            self.assertEqual(res, expected_res)
        finally:
            # Remove test file
            os.remove(out_filename)

    def test_asm_output(self):
        """
        Test that using --output ASM_FILENAME argument writes assembly
        insturctions and symbol table to a file
        """
        testcase_file = "RAT24S_programs/add_sum.txt"
        out_filename = "asm_output.txt"

        # Raise error if testcase_file does not exist or out_filename exists
        if not os.path.isfile(testcase_file):
            raise ValueError(f"{testcase_file} not found")
        if os.path.isfile(out_filename):
            raise ValueError(f"{out_filename} already exists before testing")
        
        try:
            # Run compiler
            main(testcase_file, False, None, False, None, None, out_filename,
                 None, supress_print=True)
            
            # Assert that out_filename exists
            # No need to test for correctness, that is checked by
            # TestAssemblyInstructions.test_write_asm_instructions
            self.assertTrue(os.path.exists(out_filename),
                            "Using --output or -o argument with compiler does not output a file with assembly instructions")
        finally:
            # Remove out_filename
            if os.path.isfile(out_filename):
                os.remove(out_filename)

    def test_program_1_output(self):
        """
        Test that output of RAT24S_programs/program_1.txt is correct 
        object code and symbol table
        """
        testcase_file = "RAT24S_programs/program_1.txt"
        correct_output_file = "RAT24S_programs/res_1.txt"
        out_filename = "output_1.txt"

        # Raise error if testcase_file does not exist or out_filename exists
        if not os.path.isfile(testcase_file):
            raise ValueError(f"{testcase_file} not found")
        if os.path.isfile(out_filename):
            raise ValueError(f"{out_filename} already exists before testing")
        
        try:
            # Run compiler
            main(testcase_file, False, None, False, None, None, out_filename,
                 None, supress_print=True)
            
            # Load correct output
            with open(correct_output_file) as f:
                correct_output = f.read()
            
            with open(out_filename) as f:
                actual_output = f.read()

            self.assertEqual(actual_output, correct_output)

        finally:
            # Remove out_filename
            if os.path.isfile(out_filename):
                os.remove(out_filename)

    def test_program_2_output(self):
        """
        Test that output of RAT24S_programs/program_2.txt is correct 
        object code and symbol table
        """
        testcase_file = "RAT24S_programs/program_2.txt"
        correct_output_file = "RAT24S_programs/res_2.txt"
        out_filename = "output_2.txt"

        # Raise error if testcase_file does not exist or out_filename exists
        if not os.path.isfile(testcase_file):
            raise ValueError(f"{testcase_file} not found")
        if os.path.isfile(out_filename):
            raise ValueError(f"{out_filename} already exists before testing")
        
        try:
            # Run compiler
            main(testcase_file, False, None, False, None, None, out_filename,
                 None, supress_print=True)
            
            # Load correct output
            with open(correct_output_file) as f:
                correct_output = f.read()
            
            with open(out_filename) as f:
                actual_output = f.read()

            self.assertEqual(actual_output, correct_output)

        finally:
            # Remove out_filename
            if os.path.isfile(out_filename):
                os.remove(out_filename)

    def test_program_3_output(self):
        """
        Test that output of RAT24S_programs/program_3.txt is correct 
        object code and symbol table
        """
        testcase_file = "RAT24S_programs/program_3.txt"
        correct_output_file = "RAT24S_programs/res_3.txt"
        out_filename = "output_3.txt"

        # Raise error if testcase_file does not exist or out_filename exists
        if not os.path.isfile(testcase_file):
            raise ValueError(f"{testcase_file} not found")
        if os.path.isfile(out_filename):
            raise ValueError(f"{out_filename} already exists before testing")
        
        try:
            # Run compiler
            main(testcase_file, False, None, False, None, None, out_filename,
                 None, supress_print=True)
            
            # Load correct output
            with open(correct_output_file) as f:
                correct_output = f.read()
            
            with open(out_filename) as f:
                actual_output = f.read()

            self.assertEqual(actual_output, correct_output)

        finally:
            # Remove out_filename
            if os.path.isfile(out_filename):
                os.remove(out_filename)

class TestAssemblyInstructions(unittest.TestCase):
    """Test that assembly instructions are generated correctly"""
    def test_write_asm_instructions(self):
        """
        Test that write_asm_instructions method correctly saves assembly
        instructions to a file
        """
        out_filename = "myasm.txt"
        if os.path.isfile(out_filename):
            raise ValueError(f"{out_filename} already exists before running test")

        try:
            # Setup parser with instructions
            source = "integer sum;sum = 0;"
            l = Lexer(source)
            parser = RDP(l)
            # Run declaration_lsit first to update symbol table
            parser.declaration_list()
            # Run assign to update assembly instructions
            parser.assign()

            # Run write_asm_instructions method
            parser.write_asm_instructions(out_filename)

            # Assert out_filename exists
            self.assertTrue(os.path.isfile(out_filename),
                            f"{out_filename} not created by write_asm_instructions method")
            
            # Assert correct output
            expected_output = [
                '1    PUSHI 0',
                '2    POPM 5000',
                '',
                'Identifier          Memory Location     Type',
                'sum                 5000                integer',
                ''
                ]

            with open(out_filename) as f:
                actual_output = f.read().split('\n')
            self.assertEqual(actual_output, expected_output)
        finally:
            # Remove test file when done testing
            if os.path.isfile(out_filename):
                os.remove(out_filename)

    def test_assignment(self):
        """
        Test that correct assembly instructions are generated for assignment productions
        sum = 0;
        Should generate:
        5000 PUSHI 0
        5000 POPM 1
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
        correct_instruction = "POPM 5000"
        actual_instruction = parser.asm_instructions[1]
        self.assertEqual(actual_instruction, correct_instruction)

    def test_multiple_assignment(self):
        """
        Test correct assembly instructions with multiple assignment statements
        """
        # Setup parser
        source = "$$integer i,j,k;$i=0;k=2;j=23;$"
        l = Lexer(source)
        parser = RDP(l)
        parser.rat24s()

        # Assert correct instructions length
        correct_length = 6
        actual_length = len(parser.asm_instructions)
        self.assertEqual(actual_length, correct_length)

        # Assert correct instructions
        correct_instructions = [
            "PUSHI 0",
            "POPM 5000",
            "PUSHI 2",
            "POPM 5002",
            "PUSHI 23",
            "POPM 5001"
        ]
        actual_instructions = parser.asm_instructions
        self.assertEqual(actual_instructions, correct_instructions)

    def test_scan(self):
        """
        Test that scan statements generate correct assembly code.
        scan (max);

        SIN
        POPM 5001
        """
        # Setup parser
        source = "integer max;scan (max);"
        l = Lexer(source)
        parser = RDP(l)
        parser.declaration_list()
        parser.scan()

        # Assert correct instructions
        expected_instructions = [
            'SIN',
            'POPM 5000'
        ]

        actual_instructions = parser.asm_instructions
        self.assertEqual(actual_instructions, expected_instructions)

    def test_scan_rat24s(self):
        """Test that scan works with actual RAT24S program"""
        # Setup parser
        source = "$$integer i,j;$scan(i);scan(j);$"
        l = Lexer(source)
        parser = RDP(l)
        parser.rat24s()

        # Assert correct instructions
        expected_instructions = [
            'SIN',
            'POPM 5000',
            'SIN',
            'POPM 5001'
        ]

        actual_instructions = parser.asm_instructions
        self.assertEqual(actual_instructions, expected_instructions)

    def test_while_label(self):
        """
        Test that while statements generate LABEL instruction
        """
        # Setup Parser
        source = "while ( 3 < 1 ) { scan (myvar); } endwhile"
        l = Lexer(source)
        parser = RDP(l)
        parser.ignore_symbol_table = True
        parser.While()

        # Assert correct instructions
        expected_instructions = ['LABEL']
        # Only get first instruction
        actual_instructions = parser.asm_instructions[:1]
        self.assertEqual(actual_instructions, expected_instructions)

    def test_while_jump0(self):
        """
        Test that while loops generate JUMP0 instuction with correct
        line number
        """
        # Setup parser
        source = "$$integer i;$while(i < 0){return;}endwhile\ni=0;"
        l = Lexer(source)
        parser = RDP(l)
        #parser.print_to_console = True
        parser.rat24s()

        # Assert correct instructions
        expected_instructions = [
            'LABEL',
            'PUSHM 5000',
            'PUSHI 0',
            'LES',
            'JUMP0 7',
            'JUMP 1',
            'PUSHI 0',
            'POPM 5000'
        ]

        actual_instructions = parser.asm_instructions
        self.assertEqual(actual_instructions, expected_instructions)

    def test_less_than(self):
        """
        Test that less than conditions generate correct instructions
        i < max

        PUSHM 5000
        PUSHM 5001
        LES
        """
        # Setup parser
        source = "integer i, max;i < max"
        l = Lexer(source)
        parser = RDP(l)
        parser.declaration_list()
        parser.condition()

        # Assert correct instructions
        expected_instructions = [
            'PUSHM 5000',
            'PUSHM 5001',
            'LES',
            'JUMP0 UNDEFINED'
        ]

        actual_instructions = parser.asm_instructions
        self.assertEqual(actual_instructions, expected_instructions)

    def test_greater_than(self):
        """
        Test that greater than conditions generate correct instructions
        """
        # Setup parser
        source = "$$integer i, max;$while(i > max) {return;}endwhile\nprint(1);$"
        l = Lexer(source)
        parser = RDP(l)
        parser.rat24s()

        # Assert correct instructions
        expected_instructions = [
            'LABEL',
            'PUSHM 5000',
            'PUSHM 5001',
            'GRT',
            'JUMP0 7',
            'JUMP 1',
            'PUSHI 1',
            'SOUT'
        ]

        actual_instructions = parser.asm_instructions
        self.assertEqual(actual_instructions, expected_instructions)

    def test_equal_to(self):
        """
        Test that equal to conditions generate correct instructions
        """
        # Setup parser
        source = "$$integer i, max;$while(i == max) {return;}endwhile\nprint(1);$"
        l = Lexer(source)
        parser = RDP(l)
        parser.rat24s()

        # Assert correct instructions
        expected_instructions = [
            'LABEL',
            'PUSHM 5000',
            'PUSHM 5001',
            'EQU',
            'JUMP0 7',
            'JUMP 1',
            'PUSHI 1',
            'SOUT'
        ]

        actual_instructions = parser.asm_instructions
        self.assertEqual(actual_instructions, expected_instructions)

    def test_not_equal_to(self):
        """
        Test that not equal to conditions generate correct instructions
        """
        # Setup parser
        source = "$$integer i, max;$while(i != max) {return;}endwhile\nprint(1);$"
        l = Lexer(source)
        parser = RDP(l)
        parser.rat24s()

        # Assert correct instructions
        expected_instructions = [
            'LABEL',
            'PUSHM 5000',
            'PUSHM 5001',
            'NEQ',
            'JUMP0 7',
            'JUMP 1',
            'PUSHI 1',
            'SOUT'
        ]

        actual_instructions = parser.asm_instructions
        self.assertEqual(actual_instructions, expected_instructions)

    def test_greater_equal_to(self):
        """
        Test that => conditions generate correct instructions
        """
        # Setup parser
        source = "$$integer i, max;$while(i => max) {return;}endwhile\nprint(1);$"
        l = Lexer(source)
        parser = RDP(l)
        parser.rat24s()

        # Assert correct instructions
        expected_instructions = [
            'LABEL',
            'PUSHM 5000',
            'PUSHM 5001',
            'GEQ',
            'JUMP0 7',
            'JUMP 1',
            'PUSHI 1',
            'SOUT'
        ]

        actual_instructions = parser.asm_instructions
        self.assertEqual(actual_instructions, expected_instructions)

    def test_less_equal_to(self):
        """
        Test that <= conditions generate correct instructions
        """
        # Setup parser
        source = "$$integer i, max;$while(i <= max) {return;}endwhile\nprint(1);$"
        l = Lexer(source)
        parser = RDP(l)
        parser.rat24s()

        # Assert correct instructions
        expected_instructions = [
            'LABEL',
            'PUSHM 5000',
            'PUSHM 5001',
            'LEQ',
            'JUMP0 7',
            'JUMP 1',
            'PUSHI 1',
            'SOUT'
        ]

        actual_instructions = parser.asm_instructions
        self.assertEqual(actual_instructions, expected_instructions)

    def test_addition(self):
        """
        Test that correct instructions are generated for addition
        i = i + 1
        PUSHM 5000
        PUSHI 1
        A
        POPM 5000
        """
        # Setup parser
        source = "$$integer i;$i=i+1;$"
        l = Lexer(source)
        parser = RDP (l)
        parser.rat24s()

        # Assert correct instruction generated
        expected_instructions = [
            'PUSHM 5000',
            'PUSHI 1',
            'A',
            'POPM 5000'
        ]

        actual_instructions = parser.asm_instructions
        self.assertEqual(actual_instructions, expected_instructions)

    def test_addition_two_id(self):
        """
        Test addition with two identifiers
        sum = sum + i;

        PUSHM 5000
        PUSHM 5001
        A
        POPM 5000
        """
        # Setup parser
        source = "$$integer sum,i;$sum=sum+i;$"
        l = Lexer(source)
        parser = RDP(l)
        parser.rat24s()

        # Assert correct instructions
        expected_instructions = [
            'PUSHM 5000',
            'PUSHM 5001',
            'A',
            'POPM 5000'
        ]

        actual_instructions = parser.asm_instructions
        self.assertEqual(actual_instructions, expected_instructions)

    def test_addition_two_int(self):
        """
        Test addition with two integers
        sum = 1 + 2;

        PUSHI 1
        PUSHI 2
        A
        POPM 5000
        """
        # Setup parser
        source = "$$integer sum;$sum = 1 + 2;$"
        l = Lexer(source)
        parser = RDP(l)
        parser.rat24s()

        # Assert correct instructions
        expected_instructions = [
            'PUSHI 1',
            'PUSHI 2',
            'A',
            'POPM 5000'
        ]

        actual_instructions = parser.asm_instructions
        self.assertEqual(actual_instructions, expected_instructions)

    def test_print(self):
        """
        Test that print statements correctly generate SOUT instructions
        print

        SOUT
        """
        # Setup parser
        source = "$$integer sum,max;$print(sum+max);$"
        l = Lexer(source)
        parser = RDP(l)
        parser.rat24s()

        # Assert correct instructions
        expected_instructions = [
            'PUSHM 5000',
            'PUSHM 5001',
            'A',
            'SOUT'
        ]

        actual_instructions = parser.asm_instructions
        self.assertEqual(actual_instructions, expected_instructions)

    def test_subtract(self):
        """Test that subtract expressions generate correct instructions"""
        # Setup parser
        source = "$$integer diff;$diff = diff - 5;$"
        l = Lexer(source)
        parser = RDP(l)
        parser.rat24s()

        # Assert correct instructions generated
        expected_instructions = [
            'PUSHM 5000',
            'PUSHI 5',
            'S',
            'POPM 5000'
        ]

        actual_instructions = parser.asm_instructions
        self.assertEqual(actual_instructions, expected_instructions)

    def test_subtract_integers(self):
        """
        Test that subtract expressions with integers generate the correct
        instructions
        diff = 10 - 5;

        PUSHI 10
        PUSHI 5
        S
        POPM 5000
        """
        # Setup parser
        source = "$$integer diff;$diff = 10 - 5;$"
        l = Lexer(source)
        parser = RDP(l)
        parser.rat24s()

        # Assert correct instructions generated
        expected_instructions = [
            'PUSHI 10',
            'PUSHI 5',
            'S',
            'POPM 5000'
        ]

        actual_instructions = parser.asm_instructions
        self.assertEqual(actual_instructions, expected_instructions)

    def test_subtract_ids(self):
        """
        Test that subtract expressions with identifers generate
        the correct instructions
        diff = i - j;

        PUSHM 5001
        PUSHM 5002
        S
        POPM 5000
        """
        # Setup parser
        source = "$$integer diff,i,j;$diff = i - j;$"
        l = Lexer(source)
        parser = RDP(l)
        parser.rat24s()

        # Assert correct instructions generated
        expected_instructions = [
            'PUSHM 5001',
            'PUSHM 5002',
            'S',
            'POPM 5000'
        ]

        actual_instructions = parser.asm_instructions
        self.assertEqual(actual_instructions, expected_instructions)

    def test_multiplication(self):
        """
        Test that multiplication generates correct instructions
        """
        # Setup parser
        source = "$$integer prod,i;$prod = 4 * i;$"
        l = Lexer(source)
        parser = RDP(l)
        parser.rat24s()

        # Assert correct instructions generated
        expected_instructions = [
            'PUSHI 4',
            'PUSHM 5001',
            'M',
            'POPM 5000'
        ]

        actual_instructions = parser.asm_instructions
        self.assertEqual(actual_instructions, expected_instructions)

    def test_multiplication_integers(self):
        """
        Test that multiplication of integers generates correct instructions
        """
        # Setup parser
        source = "$$integer prod;$prod = 2 * 3;$"
        l = Lexer(source)
        parser = RDP(l)
        parser.rat24s()

        # Assert correct instructions generated
        expected_instructions = [
            'PUSHI 2',
            'PUSHI 3',
            'M',
            'POPM 5000'
        ]

        actual_instructions = parser.asm_instructions
        self.assertEqual(actual_instructions, expected_instructions)

    def test_multiplication_ids(self):
        """
        Test that multiplication of identifiers generates correct instructions
        """
        # Setup parser
        source = "$$integer prod,i,j;$prod = i * j;$"
        l = Lexer(source)
        parser = RDP(l)
        parser.rat24s()

        # Assert correct instructions generated
        expected_instructions = [
            'PUSHM 5001',
            'PUSHM 5002',
            'M',
            'POPM 5000'
        ]

        actual_instructions = parser.asm_instructions
        self.assertEqual(actual_instructions, expected_instructions)

    def test_division(self):
        """
        Test that division generates correct instructions
        """
        # Setup parser
        source = "$$integer prod,i;$prod = i / 100;$"
        l = Lexer(source)
        parser = RDP(l)
        parser.rat24s()

        # Assert correct instructions generated
        expected_instructions = [
            'PUSHM 5001',
            'PUSHI 100',
            'D',
            'POPM 5000'
        ]

        actual_instructions = parser.asm_instructions
        self.assertEqual(actual_instructions, expected_instructions)

    def test_division_integers(self):
        """
        Test that division of integers generates correct instructions
        """
        # Setup parser
        source = "$$integer prod;$prod = 2 / 3;$"
        l = Lexer(source)
        parser = RDP(l)
        parser.rat24s()

        # Assert correct instructions generated
        expected_instructions = [
            'PUSHI 2',
            'PUSHI 3',
            'D',
            'POPM 5000'
        ]

        actual_instructions = parser.asm_instructions
        self.assertEqual(actual_instructions, expected_instructions)

    def test_division_ids(self):
        """
        Test that division of identifiers generates correct instructions
        """
        # Setup parser
        source = "$$integer prod,i,j;$prod = i / j;$"
        l = Lexer(source)
        parser = RDP(l)
        parser.rat24s()

        # Assert correct instructions generated
        expected_instructions = [
            'PUSHM 5001',
            'PUSHM 5002',
            'D',
            'POPM 5000'
        ]

        actual_instructions = parser.asm_instructions
        self.assertEqual(actual_instructions, expected_instructions)

if __name__ == "__main__":
    unittest.main()
