"""Symbol table for object code generation to keep track of identifiers"""
from dataclasses import dataclass

@dataclass(frozen=True)
class Symbol:
  """
  Class for storing name and type of symbol
  """
  name: str
  type: str

class SymbolTable:
  def __init__(self):
    # Initialize memory address at 1
    # mem_address is the memory address that will be assigned to next new symbol
    self.mem_address = 1
    # symbols dictionary to store all identifiers
    # Key: Symbol(name, type)
    # Value: memory address
    self.symbols = {}

  def exists_identifier(self, identifier_tok, type):
    """
    Returns true if an identifier exists in the symbol table, false otherwise
    """
    symbol = Symbol(identifier_tok.value, type)
    if symbol in self.symbols:
      return True
    return False

  def insert(self, identifier_tok, type):
    """
    Insert/update an identifier token equal to another token in the symbol table
    """
    # Raise error if not an identifier token
    if identifier_tok.type != 'identifier':
      raise ValueError("Can only insert identifiers to symbol table")

    # Raise ValueError if identifier already exists in table with same type
    if self.exists_identifier(identifier_tok, type):
      raise ValueError(f"{identifier_tok} already exists in table with type {type}")

    symbol = Symbol(identifier_tok.value, type)
    # Insert new symbol to symbol table
    self.symbols[symbol] = self.mem_address
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
      for symbol, mem_address in self.symbols.items():
        out_file.write(f"{symbol.name:20}")
        out_file.write(f"{str(mem_address):20}")
        out_file.write(symbol.type)
        out_file.write('\n')
