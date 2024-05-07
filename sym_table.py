"""Symbol table for object code generation to keep track of identifiers"""
from dataclasses import dataclass

from parse_token import Token

@dataclass
class Symbol:
  """
  Class for storing symbol memory address, and token that identifer points to
  """
  mem_address: int
  token: Token

class SymbolTable:
  def __init__(self):
    # Initialize memory address at 1
    # mem_address is the memory address that will be assigned to next new symbol
    self.mem_address = 1
    # symbols dictionary to store all identifiers
    # Key: identifier token
    # Value: Symbol object
    self.symbols = {}

  def exists_identifier(self, identifier_tok):
    """
    Returns true if an identifier exists in the symbol table, false otherwise
    """
    if identifier_tok in self.symbols:
      return True
    return False

  def insert(self, identifier_tok, val_tok):
    """
    Insert/update an identifier token equal to another token in the symbol table
    """
    # Update value of symbol if it already exists; Leave memory address the same
    if self.exists_identifier(identifier_tok):
      # Raise error if val_token type is different from current token type
      curr_tok = self.symbols[identifier_tok]
      if curr_tok.type != val_tok.type:
        raise ValueError(f"{identifier_tok.value} is {curr_tok.type} type. Cannot be assigned a different type")
    else:
      # Create symbol for val_tok
      symbol = Symbol(self.mem_address, val_tok)
      # Insert new symbol to symbol table
      self.symbols[identifier_tok] = symbol
      # Increment memory address for next symbol
      self.mem_address += 1

  def write(self, filename):
    """
    Prints/writes the symbol table to a file
    """
    raise NotImplementedError