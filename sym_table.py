"""Symbol table for object code generation to keep track of identifiers"""
from dataclasses import dataclass

from parse_token import Token

@dataclass
class Symbol:
  """
  Class for storing symbol memory address, and token that identifer points to
  """
  mem_address: int
  type: str

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

  def insert(self, identifier_tok, type):
    """
    Insert/update an identifier token equal to another token in the symbol table
    """
    # Update value of symbol if it already exists; Leave memory address the same
    if self.exists_identifier(identifier_tok):
      # Raise error if val_token type is different from current token type
      curr_type = self.symbols[identifier_tok].type
      if curr_type != type:
        raise ValueError(f"{identifier_tok.value} is {curr_type} type. Cannot be assigned a different type")
    else:
      # Create symbol for val_tok
      symbol = Symbol(self.mem_address, type)
      # Insert new symbol to symbol table
      self.symbols[identifier_tok] = symbol
      # Increment memory address for next symbol
      self.mem_address += 1

  def write(self, filename):
    """
    Prints/writes the symbol table to a file
    """
    # Write headers to file
    with open(filename, 'w') as out_file:
      out_file.write(f"{'Identifier':20}")
      out_file.write(f"{'Memory Location':20}")
      out_file.write("Type")
      out_file.write('\n')

    with open(filename, 'a') as out_file:
      for id_tok, symbol in self.symbols.items():
        out_file.write(f"{id_tok.value:20}")
        out_file.write(f"{str(symbol.mem_address):20}")
        out_file.write(symbol.type)
        out_file.write('\n')
