import unittest

from lexer import Lexer
from parse_token import Token
from rdp import RDP

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
            '$function oea3 ( ) {if  ( -(  false/-0.322/ - 0--6.5 /- 69* - 1*  - false /-    false /  na   )  +3.13+wf( usjn,rux, zbqpo)=> -  5 +b(jctn ) +-u ( hv7, o2 , g69q) /  -p(y7j,     dp  , hl)) return;endif  } function dc(  ) {return;}$integerdu, yg3; $return    ; $ '
        ]
        
        for program in programs:
            l = Lexer(program)
            parser = RDP(l)
            is_program = parser.rat24s()
            self.assertTrue(is_program, f"Not recognized as rat24s program: {program}")
            
    def test_opt_function_definitions(self):
        """
        R2. <Opt Function Definitions> ::= <Function Definitions> | <Empty>
        """
        tests = [
            '', # Empty
            'function myfunc() boolean b2t ;boolean m4; {x =( -y (zt)* true *29.18 / x35zeh ) + false; }',
            'function k25jl( ) boolean b2t ;booleanm4; {s8ado =( -io6n  (z92t   )* true    *29.18 / x35zeh ) + - false ;}'
        ]
        
        for t in tests:
            l = Lexer(t)
            parser = RDP(l)
            is_opt_function_definition = parser.opt_function_definitions()
            self.assertTrue(is_opt_function_definition, f"Not recognized as Opt Function Definitions: {t}")
        
    def test_function_definitions(self):
        """
        R3. <Function Definitions> ::= <Function> | <Function> <Function Definitions>
        """
        function_defs = [
            'function myfunc() boolean b2t ;boolean m4; {x =( -y (zt)* true *29.18 / x35zeh ) + false; }',
            'function myfunc() boolean b2t ;boolean m4; {x =( -y (zt)* true *29.18 / x35zeh ) + false; } function myfunc() boolean b2t; {x=29;}'
        ]
        
        for func_def in function_defs:
            l = Lexer(func_def)
            parser = RDP(l)
            is_func_def = parser.function_definitions
            self.assertTrue(is_func_def)
            
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
            self.assertTrue(is_func)
            
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
            self.assertTrue(is_opt_param_list)
            
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
            self.assertTrue(is_param_list)
            
    def test_parameter(self):
        """
         R7. <Parameter> ::= <IDs> <Qualifier>
        """
        param = 'myint integer'
        l = Lexer(param)
        parser = RDP(l)
        is_param = parser.parameter()
        self.assertTrue(is_param)
        
    def test_qualifier(self):
        """
        R8. <Qualifier> ::= integer | boolean | real
        """
        qualifiers = ['integer', 'boolean', 'real']
        for q in qualifiers:
            l = Lexer(q)
            parser = RDP(l)
            is_qualifier = parser.qualifier()
            self.assertTrue(is_qualifier)
            
    def test_body(self):
        """
        R8. <Body> ::= { <Statement List> }
        """
        body = '{ print (42); }'
        l = Lexer(body)
        parser = RDP(l)
        is_body = parser.body()
        self.assertTrue(is_body)
        
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
            self.assertTrue(is_opt_declartion_list)
            
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
            self.assertTrue(is_dec_list)
            
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
            self.assertTrue(is_dec)
            
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
            self.assertTrue(is_IDs)
            
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
            self.assertTrue(is_statement_list)
            
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
            self.assertTrue(is_statement)

    def test_compound(self):
        """
        R15. <Compound> ::= { <Statement List> }
        """
        compound = '{ print (true); }'
        l = Lexer(compound)
        parser = RDP(l)
        is_compound = parser.compound()
        self.assertTrue(is_compound)
        
    def test_assign(self):
        """
        R16. <Assign> ::= <Identifier> = <Expression> ;
        """
        assign = "pi = 3.14 ;"
        l = Lexer(assign)
        parser = RDP(l)
        is_assign = parser.assign()
        self.assertTrue(is_assign)
        
    def test_If(self):
        """
        R17. <If> ::= if ( <Condition> ) <Statement> <If_prime>
        """
        if_statement = 'if ( <Condition> ) <Statement> <If_prime>'
        l = Lexer(if_statement)
        parser = RDP(l)
        is_If = parser.If()
        self.assertTrue(is_If)
        
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
            self.assertTrue(is_If_prime)
            
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
            self.assertTrue(is_return)
            
    def test_Print(self):
        """
        R20. <Print> ::= print ( <Expression>);
        """
        print_statement = "print ( 1 + 2);"
        l = Lexer(print_statement)
        parser = RDP(l)
        is_Print = parser.Print()
        self.assertTrue(is_Print)

    def test_scan(self):
        """
        R21. <Scan> ::= scan ( <IDs> );
        """
        source = "scan (var123);"
        l = Lexer(source)
        parser = RDP(l)
        is_scan = parser.scan()
        self.assertTrue(is_scan, f"Not recognized as scan: {source}")
        
    def test_while(self):
        """
        R22. <While> ::= while ( <Condition> ) <Statement> endwhile
        """
        source = "while (3 < 1) return; endwhile"
        l = Lexer(source)
        parser = RDP(l)
        is_while = parser.While()
        self.assertTrue(is_while, f"Not recognized as while: {source}")
        
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
            
    def test_expression(self):
        """
        R25. <Expression> ::= <Term> <Expression_prime>
        """
        expressions = [
            "1",
            "1 + 2",
            "1 * 3",
            "4 / 2 + 3",
            "3 + a * -2 - 4 / b"
        ]
        for exp in expressions:
            l = Lexer(exp)
            parser = RDP(l)
            is_exp = parser.expression()
            self.assertTrue(is_exp, f"Not recognized as expression: {exp}")
            
    def test_expression_prime(self):
        """
        R26. <Expression_prime> ::= + <Term> <Expression_prime> | - <Term> <Expression_prime> | <Empty>
        """
        tests = [
            '+ 5',
            '- a',
            '+ 3 - b * 2 + (c + d)',
            '+ 2.5 - true',
            '', # Empty
            '+ func(x, y) - 10',
            '+ (x - y)'
        ]
        for t in tests:
            l = Lexer(t)
            parser = RDP(l)
            is_expression_prime = parser.expression_prime()
            self.assertTrue(is_expression_prime, f"Not recognized as expression prime: {t}")
            
    def test_term(self):
        """
        R27. <Term> ::= <Factor> <Term_prime>
        """
        terms = [
            '3',
            'x',
            '-a',
            '4 * x',
            'y / 2',
            '(3 + a) * 5',
            'b * -2 / (c + 1)',
            '2.5 * func(x)',
            'true / false'
        ]
        
        for term in terms:
            l = Lexer(term)
            parser = RDP(l)
            is_term = parser.term()
            self.assertTrue(is_term, f"Not recognized as term: {term}")
            
    def test_term_prime(self):
        """
        R28. <Term_prime> ::= * <Factor> <Term_prime> | / <Factor> <Term_prime> | <Empty>
        """
        term_primes = [
            '* 5',
            '/ a',
            '* x / 2',
            '* -3 / b * (c + 1)',
            '/ 2.5',
            '* func(x, y)',
            '',
            '* (x - y) / true'
        ]
        
        for tp in term_primes:
            l = Lexer(tp)
            parser = RDP(l)
            is_term_prime = parser.term_prime()
            self.assertTrue(is_term_prime, f"Not recognized as term prime: {tp}")
            
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
            
    def test_primary(self):
        """
        R30. <Primary> ::= <Identifier> | <Integer> | <Identifier> ( <IDs> ) |
        ( <Expression> ) | <Real> | true | false        
        """
        primaries = [
            'x',
            '123',
            'func(x, y)',
            '45.67',
            'true',
            'false',
            '(a + b)',
        ]
        
        for p in primaries:
            l = Lexer(p)
            parser = RDP(l)
            is_primary = parser.primary()
            self.assertTrue(is_primary, f"Not recognized as primary: {p}")

if __name__ == "__main__":
    unittest.main()
