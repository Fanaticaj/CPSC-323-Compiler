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
    
    def test_scan(self):
        """
        R21. <Scan> ::= scan ( <IDs> );
        """
        source = "scan (var123);"
        l = Lexer(source)
        parser = RDP(l)
        is_scan = parser.scan()
        self.assertTrue(is_scan)
        
    def test_while(self):
        """
        R22. <While> ::= while ( <Condition> ) <Statement> endwhile
        """
        source = "while (3 < 1) return; endwhile"
        l = Lexer(source)
        parser = RDP(l)
        is_while = parser.While()
        self.assertTrue(is_while)
        
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
            self.assertTrue(is_condition)
            
    
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
            self.assertTrue(is_relop)
            
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
            self.assertTrue(is_exp)
            
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
            self.assertTrue(is_expression_prime)
            
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
            self.assertTrue(is_term)
            
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
            self.assertTrue(is_term_prime)
            
    def test_factor(self):
        """
        R29. <Factor> ::= - <Primary> | <Primary>
        """
        factors = [
            '42',
            '-24',
            'x',
            '3.14',
            'true',
            '(a + b)',
            'func(a, b)',
            '-2.718',
            '-(x * 2)',
            '-func(x)'
        ]
        
        for f in factors:
            l = Lexer(f)
            parser = RDP(l)
            is_factor = parser.factor()
            self.assertTrue(is_factor)
            
    def test_primary(self):
        """
        R30. <Primary> ::= <Identifier> | <Integer> | <Identifier> ( <IDs> ) |
        ( <Expression> ) | <Real> | true | false        
        """
        primaries = [
            'x',
            '123',
            '45.67',
            'true',
            'false',
            '(a + b)',
            'func(x, y)',
            'compute(5, 3.14, true)',
            '((x + 2) * 3)',
            '(-(x + y))'
        ]
        
        for p in primaries:
            l = Lexer(p)
            parser = RDP(l)
            is_primary = parser.primary()
            self.assertTrue(is_primary, f"Not recognized as primary: {p}")

if __name__ == "__main__":
    unittest.main()
