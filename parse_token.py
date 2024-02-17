from dataclasses import dataclass

@dataclass
class Token:
    """Class for representing tokens"""
    type: str
    value: str

    def __post_init__(self):
        # Check that token type is valid
        valid_types = set(['identifier', 'integer', 'keyword', 'operator', 'real', 'separator'])
        if self.type not in valid_types:
            raise ValueError(f"Token type {self.type} is not a valid type.")

        # Call lower() on token value to ensure that all tokens are lowercase
        self.value = self.value.lower()
