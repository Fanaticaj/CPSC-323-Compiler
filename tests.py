import unittest

from lexer import Lexer

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
        raise NotImplementedError

    def test_keywords(self):
        """Test that keywords are tokenized as keywords"""
        raise NotImplementedError

    def test_separators(self):
        """Test that separators are tokenized as separators"""
        raise NotImplementedError

    def test_operators(self):
        """Test that operators are tokenized as operators"""
        raise NotImplementedError

    def test_identifiers(self):
        """Test that identifiers are tokenized as identifiers"""
        raise NotImplementedError

    def test_integers(self):
        """Test that integers are tokenized as integers"""
        raise NotImplementedError

    def test_reals(self):
        """Test that reals are tokenized as reals"""
        raise NotImplementedError

if __name__ == "__main__":
    unittest.main()
