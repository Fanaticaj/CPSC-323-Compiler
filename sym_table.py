"""Symbol table for object code generation to keep track of identifiers"""
from dataclasses import dataclass

@dataclass(frozen=True)
class Symbol:
  """
  Class for storing name and type of symbol
  """
  mem_address: int
  type: str

class SymbolTable:
  def __init__(self):
    # Initialize memory address at 1
    # mem_address is the memory address that will be assigned to next new symbol
    self.mem_address = 5000
    # symbols dictionary to store all identifiers
    # Key: Symbol(name, type)
    # Value: memory address
    self.symbols = {}

  def exists_identifier(self, identifier_tok):
    """
    Returns true if an identifier exists in the symbol table, false otherwise
    """
    if identifier_tok.value in self.symbols:
      return True
    return False
  
  def get_mem_address(self, id_tok):
    """
    Return memory address of an identifier
    """
    # Raise error if symbol does not exist
    if not self.exists_identifier(id_tok):
      raise ValueError(f"{id_tok} does not exist in symbol table")
    # Get symbol memory address
    mem_address = self.symbols[id_tok.value].mem_address
    return mem_address

  def insert(self, identifier_tok, type):
    """
    Insert/update an identifier token equal to another token in the symbol table
    """
    # Raise error if not an identifier token
    if identifier_tok.type != 'identifier':
      raise ValueError("Can only insert identifiers to symbol table")

    # Raise ValueError if identifier already exists in table
    if self.exists_identifier(identifier_tok):
      raise ValueError(f"{identifier_tok} already exists in table")

    # Create symbol
    symbol = Symbol(self.mem_address, type)
    # Insert new symbol to symbol table
    id_name = identifier_tok.value
    self.symbols[id_name] = symbol
    # Increment memory address for next symbol
    self.mem_address += 1

    # Replace all previous symbols with type of None with same type as this symbol
    # Needed for declaration list identifiers
    if type:
      # Get list of all ids with symbols of type None
      none_type_ids = [id_name for id_name, symbol in self.symbols.items() if symbol.type == None]
      for id in none_type_ids:
        # Create new symbol with updated type
        symbol = self.symbols[id]
        curr_mem_address = symbol.mem_address
        new_symbol = Symbol(curr_mem_address, type)
        # Insert updated symbol to dictionary
        self.symbols[id] = new_symbol

  def write(self, filename, *, append_to_file=False):
    """
    Prints/writes the symbol table to a file
    """
    # Write headers to file
    write_mode = 'w'
    if append_to_file:
      write_mode = 'a'
    with open(filename, write_mode) as out_file:
      out_file.write(f"{'Identifier':20}")
      out_file.write(f"{'Memory Location':20}")
      out_file.write("Type")
      out_file.write('\n')

    with open(filename, 'a') as out_file:
      sorted_symbols = sorted(self.symbols.items(), key=lambda item: item[1].mem_address)
      for id_name, symbol in sorted_symbols:
        out_file.write(f"{id_name:20}")
        out_file.write(f"{str(symbol.mem_address):20}")
        out_file.write(symbol.type)
        out_file.write('\n')
