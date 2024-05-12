"""Recursive Descent Parser for Syntax Analysis"""
from sym_table import SymbolTable

class RDP:
  def __init__(self, lexer, *, print_to_console=False, out_filename=None):
    self.lexer = lexer
    self.print_to_console = print_to_console
    self.out_filename = out_filename
    self.print_buffer = []  # Used to print tokens after printing production
    # Store left-hand side of production until right-hand side is determined
    self.print_production_buffer = []
    self.asm_instructions = []
    self.symbol_table = SymbolTable()
    # Stores which functions are checking for recursive functions
    self.checking_recursive = {
      'is_function_definitions_recursive': False,
      'is_parameter_list_recursive' : False,
      'is_IDs_recursive' : False,
      'is_statement_list_recursive' : False
    }
    # For use when testing a single production rule
    self.ignore_symbol_table = False
    self.in_declaration_list = False
    self.in_scan = False
    self.in_print = False
    
    # Clear out file if it is set
    if self.out_filename:
        with open(self.out_filename, 'w') as out_txt:
          out_txt.write("")
    
  def token_is(self, token_type, token_val=None):
    """
    Return True if next token type of next token in lexer is equal recursive descent parserto token_type.
    Enter value for token_val if value of token matters ie. operators, separators, and keywords
    """
    next_token = self.lexer.get_next_token()
    if next_token is None:
      return False
    if next_token.type == token_type and token_val == None:
      last_token = self.lexer.get_prev_token()
      self.print_token(last_token)
      return True
    elif next_token.type == token_type and token_val == next_token.value:
      last_token = self.lexer.get_prev_token()
      self.print_token(last_token)
      return True
    
    # Backtrack if token type not equal to token_type
    self.lexer.backtrack()
    return False
  
  def print_production(self, production, *, to_be_continued=False):
    """Print and append to file the current production"""
    if self.is_checking_recursive():
      return

    prod = f"{'':2}{production}"
    if to_be_continued:
      self.print_production_buffer.append(prod)
    elif self.print_to_console:
      print(prod)
        
    if self.out_filename:
      # Append to outfile here
      if not to_be_continued:
        self.append_to_file(prod)
        
  def finish_production_print(self, production):
    """Print the right hand side of a production that was started but not finished"""
    if self.is_checking_recursive():
      return

    left_hand_side = ' '.join(self.print_production_buffer)
    self.print_production_buffer.clear()
    prod = f"{left_hand_side} {production}"
    if self.print_to_console:
      print(prod)
    
    if self.out_filename:
      self.append_to_file(prod)

  def print_token(self, token):
    """Print token and append to file a token"""
    if self.is_checking_recursive():
      return

    tok = f"Token: {token.type:15} Lexeme: {token.value}"
    if self.print_to_console:
      print(tok)
      
    if self.out_filename:
      self.append_to_file(f"{tok}")
      
  def append_to_file(self, txt):
    """Append txt to output file"""
    with open(self.out_filename, 'a') as out_txt:
      out_txt.write(f"{txt}\n")

  def write_symbol_table(self, filename):
    """Write symbol table to a file"""
    self.symbol_table.write(filename)

  def write_asm_instructions(self, filename):
    """
    Write assembly instructions and symbol table to a file
    """
    # Write assembly instructions
    with open(filename, 'w') as out_file:
      for line_num, instruction in enumerate(self.asm_instructions):
        out_file.write(f"{line_num + 1:<5}{instruction}\n")

      # Newline to separate instructions and symbol table
      out_file.write('\n')

    # Append symbol table
    self.symbol_table.write(filename, append_to_file=True)

  def is_checking_recursive(self):
    """
    Returns True if any function is checking for recursive functions, False otherwise
    """
    for func_name, bool in self.checking_recursive.items():
      if bool == True:
        return True
    return False
  
  def swap_last_two_instructions(self):
    """Swap the last two instructions in self.asm_instructions"""
    # Check that there are at least two instructions
    if self.ignore_symbol_table or self.is_checking_recursive():
      return

    if len(self.asm_instructions) < 2:
      raise ValueError("Cannot swap instructions because there less than 2")

    last = self.asm_instructions[-1]
    second = self.asm_instructions[-2]
    self.asm_instructions[-1] = second
    self.asm_instructions[-2] = last

  def insert_PUSHM(self):
    """Insert PUSHM instruction"""
    if not self.is_checking_recursive() and not self.ignore_symbol_table:
      prev_tok = self.lexer.get_prev_token()
      if not self.symbol_table.exists_identifier(prev_tok):
        err_msg = f"Error: Identifier {prev_tok.value} was not declared"
        self.print_production(err_msg)
        self.asm_instructions.append(err_msg)
        return False
      mem_address = self.symbol_table.get_mem_address(prev_tok)
      self.asm_instructions.append(f"PUSHM {mem_address}")

  def rat24s(self):
      """
      R1. <Rat24S> ::= $ <Opt Function Definitions> $ <Opt Declaration List> $ <Statement List> $
      """
      # Check for the first $ symbol.
      if not self.token_is('separator', '$'):
          self.print_production("Error: Expected '$' at the beginning of the program.")
          return False
      else:
        self.print_production("<Rat24S> --> $ <Opt Function Definitions> $ <Opt Declaration List> $ <Statement List> $")
        
      # Optionally parse function definitions.
      if not self.opt_function_definitions():
          self.print_production("Error: Issue parsing optional function definitions.")
          return False

      # Check for the $ symbol after optional function definitions.
      if not self.token_is('separator', '$'):
          self.print_production("Error: Expected '$' after optional function definitions.")
          return False

      # Optionally parse declaration list.
      if not self.opt_declaration_list():
          self.print_production("Error: Issue parsing optional declaration list.")
          return False

      # Check for the $ symbol after optional declaration list.
      if not self.token_is('separator', '$'):
          self.print_production("Error: Expected '$' after optional declaration list.")
          return False

      # Parse statement list.
      if not self.statement_list():
          self.print_production("Error: Issue parsing statement list.")
          return False

      # Check for the final $ symbol indicating the end of the program.
      if not self.token_is('separator', '$'):
          self.print_production("Error: Expected final '$' at the end of the program.")
          return False
      return True

  def opt_function_definitions(self):
    """
    R2. <Opt Function Definitions> ::= <Function Definitions> | <Empty>
    """
    first_function_definitions_terminal = 'function'
    next_token_val = self.lexer.get_next_token_val()
    if next_token_val  == first_function_definitions_terminal:
      self.print_production("<Opt Function Definitions> --> <Function Definitions>")
      if self.function_definitions():
        return True
    elif self.empty():
      self.print_production("<Opt Function Definitions> --> <Empty>")
      return True
    return False
  
  def is_function_definitions_recursive(self):
    """Return True if function definitions includes more than one function, False otherwise"""
    self.checking_recursive['is_function_definitions_recursive'] = True
    curr = self.lexer.curr_token
    # Read first function
    self.function()
    is_recursive = self.function()
    self.lexer.curr_token = curr
    self.checking_recursive['is_function_definitions_recursive'] = False
    return is_recursive
  
  def function_definitions(self):
    """
    R3. <Function Definitions> ::= <Function> | <Function> <Function Definitions>
    """
    #self.print_production("<Function Definitions> --> <Function> | <Function> <Function Definitions>")
    is_recursive = self.is_function_definitions_recursive()
    # Check function and function definitions if program contains more than one function
    if is_recursive:
      self.print_production("<Function Definitions> --> <Function> <Function Definitions>")
      if self.function():
        if self.function_definitions():
          return True
        return True
      return False
    else:  # Check only function if program contains only one function
      self.print_production("<Function Definitions> --> <Function>")
      if self.function():
        return True
      else:
        return False

  def function(self):
      """
      R4. <Function> ::= function <Identifier> ( <Opt Parameter List> ) <Opt Declaration List> <Body>
      """
      if self.token_is('keyword', 'function'):
          # Expecting a single identifier for the function name.
          if self.token_is('identifier'):  # Adjusted from IDs() to expect a single identifier.
              if self.token_is('separator', '('):
                  if self.opt_parameter_list():  # Parse optional parameter list.
                      if self.token_is('separator', ')'):
                          if self.opt_declaration_list():  # Parse optional declaration list.
                              if self.body():  # Parse the function body.
                                  return True
                              else:
                                  self.print_production("Error: Invalid function body.")
                          else:
                              self.print_production("Error: Issue within optional declaration list.")
                      else:
                          self.print_production("Error: Expected ')' after parameters.")
                  else:
                      self.print_production("Error: Issue within optional parameter list.")
              else:
                  self.print_production("Error: Expected '(' after function name.")
          else:
              self.print_production("Error: Expected identifier after 'function' keyword.")
      return False

  
  def opt_parameter_list(self):
    """
    R5. <Opt Parameter List> ::= <Parameter List> | <Empty>
    """
    first_terminal_type = 'identifier'
    next_terminal = self.lexer.peek_next_token()
    if next_terminal is None:
      next_terminal_type = ''
    else:
      next_terminal_type = next_terminal.type
    if next_terminal_type == first_terminal_type:
      self.print_production("<Opt Parameter List> --> <Parameter List>")
    # Attempt to parse a parameter list. If successful, the parameter_list function will handle its own logging.
      if self.parameter_list():  # If no parameter list found, treat as empty.
          return True
    self.print_production("<Opt Parameter List> --> <Empty>")
    return True
  
  def is_parameter_list_recursive(self):
    """Return True if <Parameter occurs more than once, False otherwise"""
    self.checking_recursive['is_parameter_list_recursive'] = True
    curr = self.lexer.curr_token
    # Read first function
    self.parameter()
    next_tok = self.lexer.peek_next_token()
    if next_tok and next_tok.value == ',':
      is_recursive = True
    else:
      is_recursive = False
    self.lexer.curr_token = curr
    self.checking_recursive['is_parameter_list_recursive'] = False
    return is_recursive
  
  def parameter_list(self):
      """
      R6. <Parameter List> ::= <Parameter> | <Parameter>, <Parameter List>
      """
      is_recursive = self.is_parameter_list_recursive()
      
      if is_recursive:
        self.print_production("<Parameter List> --> <Parameter>, <Parameter List>")
        if self.parameter():
          if self.token_is('separator', ','):
            if self.parameter_list():
              return True
            else:
              return False
          else:
            return False
        else:
          return False
      else:
        self.print_production("<Parameter List> --> <Parameter>")
        if self.parameter():
          return True
        return False
  
  def parameter(self):
    """
    R7. <Parameter> ::= <IDs> <Qualifier>
    """
    self.print_production("<Parameter> --> <IDs> <Qualifier>")
    if self.IDs() and self.qualifier():
        return True
    return False
    
  def qualifier(self):
    """
    R8. <Qualifier> ::= integer | boolean | real
    """
    if self.token_is('keyword', 'integer'):
      self.print_production("<Qualifier> --> integer")
      return True
    elif self.token_is('keyword', 'boolean'):
      self.print_production("<Qualifier> --> boolean")
      return True
    elif self.token_is('keyword', 'real'):
      self.print_production("<Qualifier> --> real")
      return True
    return False
  
  def body(self):
    """
    R8. <Body> ::= { <Statement List> }
    """
    if self.token_is('separator', '{'):
      self.print_production("<Body> --> { <Statement List> }")
      if self.statement_list():  # Process the statement list.
        if self.token_is('separator', '}'):
          return True
        else:
          self.print_production("Error: Expected '}' at the end of the body.")
      else:
        self.print_production("Error: Invalid statement list inside body.")
    else:
        self.print_production("Error: Expected '{' at the beginning of the body.")
    return False
  
  def opt_declaration_list(self):
      """
      R9. <Opt Declaration List> ::= <Declaration List> | <Empty>
      """
      # Peek at the next token without consuming it.
      lookahead_token = self.lexer.peek_next_token()
      # Ensure lookahead_token is not None before accessing its attributes.
      if lookahead_token is not None and lookahead_token.type == 'keyword' and lookahead_token.value in ['integer', 'boolean', 'real']:
          # If the lookahead token could start a declaration, attempt to parse the declaration list.
          self.print_production("<Opt Declaration List> --> <Declaration List>")
          if self.declaration_list():
              return True
          else:
              return False
      elif self.empty():
          # If the next token does not indicate the start of a declaration list or if we're at the end of input, treat this as an empty list.
          self.print_production("<Opt Declaration List> --> <Empty>")
          return True  # Return True because the declaration list is optional and absence of a declaration list is not an error.
  
  def declaration_list(self):
      """
      R10. <Declaration List> := <Declaration> ; | <Declaration> ; <Declaration List>
      """
      self.in_declaration_list = True
      FIRST = set(['integer', 'boolean', 'real'])
      next_token = self.lexer.peek_next_token()
      if next_token and next_token.value in FIRST:
        self.print_production("<Declaration List> := <Declaration> ; | <Declaration> ; <Declaration List>")
      # Attempt the first declaration.
      if not self.declaration():
          self.in_declaration_list = False
          return False

      # After a successful declaration, expect a semicolon.
      while True:
          if self.token_is('separator', ';'):
              # Attempt to parse another declaration directly.
              if not self.declaration():
                  # If False, we've reached the end of valid declarations or hit an improperly formatted declaration.
                  break
          else:
              # If the next token isn't a semicolon, we've exited the declaration list properly.
              break
      self.in_declaration_list = False
      return True
  
  def declaration(self):
    """
    R11. <Declaration> ::= integer <IDs> | boolean <IDs> | real <IDs>
    """
    # Interger declaration
    if self.token_is('keyword', 'integer'):
      self.print_production("<Declaration> --> integer <IDs>")
      if self.IDs():
        # Insert integer token to symbol table
        int_tok = self.lexer.get_prev_token()
        self.symbol_table.insert(int_tok, 'integer')
        return True
      return False
    # Boolean declaration
    elif self.token_is('keyword', 'boolean'):
      self.print_production('<Declaration> --> boolean <IDs>')
      if self.IDs():
        bool_tok = self.lexer.get_prev_token()
        self.symbol_table.insert(bool_tok, 'boolean')
        return True
      return False
    # Real declaration
    elif self.token_is('keyword', 'real'):
      self.print_production("<Declaration> --> real <IDs>")
      if self.IDs():
        return True
      return False
    return False
  
  def is_IDs_recursive(self):
    """Return True if there is more than one IDs, False otherwise"""
    self.checking_recursive['is_IDs_recursive'] = True
    curr = self.lexer.curr_token
    self.token_is('identifier')
    next_token = self.lexer.peek_next_token()
    if next_token and next_token.value == ',':
      is_recursive = True
    else:
      is_recursive = False
    self.lexer.curr_token = curr
    self.checking_recursive['is_IDs_recursive'] = False
    return is_recursive

  def IDs(self):
      """
      R12. <IDs> ::= <Identifier> | <Identifier>, <IDs>
      """
      is_recursive = self.is_IDs_recursive()
      
      if is_recursive:
        self.print_production("<IDs> --> <Identifier>, <IDs>")
        if self.token_is('identifier'):
          # Insert to symbol table with type None (will be updated with last 
          # symbol in declaration list)
          if not self.is_checking_recursive() and not self.ignore_symbol_table and self.in_scan:
            id_tok = self.lexer.get_prev_token()
            if not self.symbol_table.exists_identifier(id_tok):
              err_msg = f"Error: Identifier {id_tok.value} was not declared"
              self.print_production(err_msg)
              self.asm_instructions.append(err_msg)
              return False
            id_mem_address = self.symbol_table.get_mem_address(id_tok)
            self.asm_instructions.append('SIN')
            self.asm_instructions.append(f"POPM {id_mem_address}")

          if self.in_declaration_list:
            prev_tok = self.lexer.get_prev_token()
            self.symbol_table.insert(prev_tok, None)
          if self.token_is('separator', ','):
            if self.IDs():
              return True
            else:
              return False
          else:
            return False
        else:
          return False
      else:
        self.print_production("<IDs> --> <Identifier>")
        if self.token_is('identifier'):
          return True
        else:
          return False
        
  def is_statement_list_recursive(self):
    """Return True if statement occurs more than once, false otherwise"""
    curr = self.lexer.curr_token
    self.checking_recursive[f'is_statement_list_recursive{curr}'] = True
    self.statement()
    is_recursive = self.statement()
    self.lexer.curr_token = curr
    self.checking_recursive[f'is_statement_list_recursive{curr}'] = False
    return is_recursive

  def statement_list(self):
    """
    R13. <Statement List> ::= <Statement> | <Statement> <Statement List>
    """
    is_recursive = self.is_statement_list_recursive()
    if is_recursive:
      self.print_production("<Statement List> --> <Statement> <Statement List>")
      if self.statement():
        if self.statement_list():
          return True
        return True
      return False
    else:
      self.print_production("<Statement List> --> <Statement>")
      if self.statement():
        return True
      return False
  
  def statement(self):
    """
    R14. <Statement> ::= <Compound> | <Assign> | <If> | <Return> | <Print> | <Scan> | <While>
    """
    if not self.is_checking_recursive():
      self.print_production("<Statement> -->", to_be_continued=True)
    if self.compound():
      return True
    elif self.assign():
      return True
    elif self.If():
       return True
    elif self.Return():
       return True
    elif self.Print():
       return True
    elif self.scan():
       return True
    elif self.While():
       return True
    else:
       return False
  
  def compound(self):
    """
    R15. <Compound> ::= { <Statement List> }
    """
    if self.token_is('separator', '{'):
        self.finish_production_print("<Compound>")
        self.print_production("<Compound> --> { <Statement List> }")
        if self.statement_list(): 
            if self.token_is('separator', '}'):
                return True
            else:
                return False
        else:
            return False
    else:
        return False
  
  def assign(self):
    """
    R16. <Assign> ::= <Identifier> = <Expression> ;
    """
    if self.token_is('identifier'):
      self.finish_production_print("<Assign>")
      self.print_production("<Assign> --> <Identifier> = <Expression> ;")
      id_tok = self.lexer.get_prev_token()
      if self.token_is('operator', '='):
        if self.expression():
          assign_tok = self.lexer.get_prev_token()
          assign_type = assign_tok.type
          if self.token_is('separator', ';'):
            # Add POPM instruction to asm_instructions
            # Get mem address of identifer
            if not self.is_checking_recursive() and not self.ignore_symbol_table:
              if assign_type == 'integer' or id_tok.type == 'identifier':
                if not self.symbol_table.exists_identifier(id_tok):
                  err_msg = f"Error: Identifier {id_tok.value} was not declared"
                  self.print_production(err_msg)
                  self.asm_instructions.append(err_msg)
                  return False
                mem_address = self.symbol_table.get_mem_address(id_tok)
                self.asm_instructions.append(f"POPM {mem_address}")
            return True
          else:
            return False
        else:
           return False
      else:
        return False
    else:
       return False

  def If(self):
    """
    R17. <If> ::= if ( <Condition> ) <Statement> <If_prime>
    """
    if self.token_is('keyword', 'if'):
      self.finish_production_print("<If>")
      self.print_production("<If> --> if ( <Condition> ) <Statement> <If_prime>")
      if self.token_is('separator', '('):
        if self.condition():
          if self.token_is('separator', ')'):
            if self.statement():
              if self.If_prime():
                 return True
              else:
                  return False
            else:
              return False
          else:
            return False
        else:
          return False
      else:
          return False
    else:
          return False
  
  def If_prime(self):
    """
    R18. <If_prime> ::= endif | else <Statement> endif
    """
    if self.token_is('keyword','endif'):
      self.print_production("<If_prime> --> endif")
      return True
    elif self.token_is('keyword','else'):
      self.print_production("<If_prime> --> else <Statement> endif")
      if self.statement():
          if self.token_is('keyword','endif'):
              return True
          else:
            return False
      else:
          return False
    else:
       return False
  
  def Return(self):
    """
    R19. <Return> ::= return ; | return <Expression> ;
    """
    if self.token_is('keyword', 'return'):
      self.finish_production_print("<Return>")
      self.print_production("<Return> --> return ; | return <Expression> ;")
      if self.token_is('separator', ';'):
        return True
      elif self.expression():
        if self.token_is('separator', ';'):
          return True
        else:
          return False
      else:
        return False
    
    return False
  
  def Print(self):
    """
    R20. <Print> ::= print ( <Expression>);
    """
    self.in_print = True
    if self.token_is('keyword', 'print'):
      self.finish_production_print("<Print>")
      self.print_production("<Print> --> print ( <Expression>);")
      if self.token_is('separator', '('):
        if self.expression():
          if self.token_is('separator', ')'):
            if self.token_is('separator', ';'):
              if not self.is_checking_recursive():
                self.asm_instructions.append('SOUT')
              self.in_print = False
              return True
    self.in_print = False
    return False
  
  def scan(self):
    """
    R21. <Scan> ::= scan ( <IDs> );
    """
    self.in_scan = True
    if self.token_is('keyword', 'scan'):
      self.finish_production_print("<Scan>")
      self.print_production("<Scan> --> scan ( <IDs> );")
      if self.token_is('separator', '('):
        if self.IDs():
          if not self.is_checking_recursive() and not self.ignore_symbol_table:
            self.asm_instructions.append("SIN")
            id_tok = self.lexer.get_prev_token()
            if not self.symbol_table.exists_identifier(id_tok):
              err_msg = f"Error: Identifier {id_tok.value} was not declared"
              self.print_production(err_msg)
              self.asm_instructions.append(err_msg)
              self.in_scan = False
              return False
            id_mem_address = self.symbol_table.get_mem_address(id_tok)
            self.asm_instructions.append(f"POPM {id_mem_address}")
          if self.token_is('separator', ')'):
            if self.token_is('separator', ';'):
              self.in_scan = False
              return True
    self.in_scan = False
    return False
  
  def get_prev_label_line_num(self):
    """
    Return line number of the most recent label in instructions list
    """
    line_count = len(self.asm_instructions)
    last_label = None
    for instruction in self.asm_instructions[::-1]:
      if instruction == 'LABEL':
        last_label = line_count
        break
      line_count -= 1
    return last_label
  
  def update_prev_JUMP0_line_num(self):
    """
    Update the previous JUMP0 instruction so that it points to the next line number
    """
    # Update last JUMP0 line number to next line number
    next_line_num = len(self.asm_instructions) + 1
    line_count = len(self.asm_instructions) - 1
    while line_count >= 0:
      curr_instruction = self.asm_instructions[line_count]
      if curr_instruction == "JUMP0 UNDEFINED":
        self.asm_instructions[line_count] = f"JUMP0 {next_line_num}"
        break
      line_count -= 1

  
  def While(self):
    """
    R22. <While> ::= while ( <Condition> ) <Statement> endwhile
    """
    if self.token_is('keyword', 'while'):
      if not self.is_checking_recursive():
        self.finish_production_print("<While>")
        self.print_production("<While> --> while ( <Condition> ) <Statement> endwhile")
        self.asm_instructions.append('LABEL')
      if self.token_is('separator', '('):
        if self.condition():
          if self.token_is('separator', ')'):
            if self.statement():
              if self.token_is('keyword', 'endwhile'):
                # Generate instruction to jump back to start of while loop
                if not self.is_checking_recursive():
                  label_line_num = self.get_prev_label_line_num()
                  self.asm_instructions.append(f"JUMP {label_line_num}")
                  # Update JUMP0 line number
                  self.update_prev_JUMP0_line_num()
                return True
    return False

  def condition(self):
    """
    R23. <Condition> ::= <Expression> <Relop> <Expression>
    """
    # FIRST set for <Expression>
    FIRST = set(['-', '(', 'true', 'false'])
    FIRST_TYPES = set(['identifier', 'integer', 'real'])
    next_token = self.lexer.peek_next_token()
    # Check if next token type and value are in FIRST  sets
    # Print production rule if True
    if next_token:
      if next_token.type in FIRST_TYPES or next_token.value in FIRST:
        self.print_production("<Condition> --> <Expression> <Relop> <Expression>")

    # Parse tokens
    if self.expression():
      tok = self.lexer.get_prev_token()
      if tok.type == 'identifier':
        if not self.symbol_table.exists_identifier(tok):
          err_msg = f"Error: Identifier {tok.value} was not declared"
          self.print_production(err_msg)
          self.asm_instructions.append(err_msg)
          return False
        self.insert_PUSHM()
      if self.relop():
        if self.expression():
          tok = self.lexer.get_prev_token()
          if tok.type == 'identifier':
            if not self.symbol_table.exists_identifier(tok):
              err_msg = f"Error: Identifier {tok.value} was not declared"
              self.print_production(err_msg)
              self.asm_instructions.append(err_msg)
              return False
            self.insert_PUSHM()
          self.swap_last_two_instructions()
          if not self.is_checking_recursive():
            self.asm_instructions.append('JUMP0 UNDEFINED')
          return True
    return False

  def relop(self):
    """
    R24. <Relop> ::= == | != | > | < | <= | =>
    """
    operators = set(['==', '!=', '>', '<', '<=', '=>'])
    next_token = self.lexer.peek_next_token()
    if self.token_is('operator') and next_token.value in operators:
      self.print_production(f"<Relop> --> {next_token.value}")
      if not self.is_checking_recursive():
        # Get operator value
        op = self.lexer.get_prev_token().value

        # Insert LES instruction for < operator
        if op == '<':
          self.asm_instructions.append('LES')
        elif op == '>':
          self.asm_instructions.append('GRT')
        elif op == '==':
          self.asm_instructions.append('EQU')
        elif op == '!=':
          self.asm_instructions.append('NEQ')
        elif op == '=>':
          self.asm_instructions.append('GEQ')
        elif op == '<=':
          self.asm_instructions.append('LEQ')
      return True
    else:
      self.lexer.backtrack()
      return False

  def expression(self):
    """
    R25. <Expression> ::= <Term> <Expression_prime>
    """
    self.print_production("<Expression> --> <Term> <Expression_prime>")
    if self.term():
      if self.expression_prime():
        return True
    return False
  
  def insert_id_pushm_second(self):
    """
    Insert a PUSHM instruction for identifiers when the identifier is
    the first of two primaries
    """
    if self.in_print:
      return
    tok = self.lexer.tokens[self.lexer.curr_token - 2]
    if tok and tok.type == 'identifier':
      if not self.symbol_table.exists_identifier(tok):
        err_msg = f"Error: Identifier {tok.value} was not declared"
        self.print_production(err_msg)
        self.asm_instructions.append(err_msg)
        return False
      mem_address = self.symbol_table.get_mem_address(tok)
      self.asm_instructions.append(f"PUSHM {mem_address}")

  def insert_id_pushm_first(self):
    """
    Insert PUSHM instruction when identifier is previous token
    """
    if self.in_print:
      return
    tok = self.lexer.get_prev_token()
    if tok and tok.type == 'identifier':
      if not self.symbol_table.exists_identifier(tok):
        err_msg = f"Error: Identifier {tok.value} was not declared"
        self.print_production(err_msg)
        self.asm_instructions.append(err_msg)
        return False
      mem_address = self.symbol_table.get_mem_address(tok)
      self.asm_instructions.append(f'PUSHM {mem_address}')

  def expression_prime(self):
    """
    R26. <Expression_prime> ::= + <Term> <Expression_prime> | - <Term> <Expression_prime> | <Empty>
    """
    if self.token_is('operator', '+'):
      self.print_production("<Expression_prime> --> + <Term> <Expression_prime>")
      if not self.is_checking_recursive() and not self.ignore_symbol_table:
        self.insert_id_pushm_second()
        self.asm_instructions.append('A')
      if self.term():
        if not self.is_checking_recursive() and not self.ignore_symbol_table:
          self.insert_id_pushm_first()
          self.swap_last_two_instructions()
        if self.expression_prime():
          return True
      return False
    elif self.token_is('operator', '-'):
      self.print_production("<Expression_prime> --> - <Term> <Expression_prime>")
      if not self.is_checking_recursive() and not self.ignore_symbol_table:
        self.insert_id_pushm_second()
      if self.term():
        if not self.is_checking_recursive() and not self.ignore_symbol_table:
          self.insert_id_pushm_first()
        if self.expression_prime():
          if not self.is_checking_recursive() and not self.ignore_symbol_table:
            self.asm_instructions.append('S')
          return True
      return False
    elif self.empty():
      self.print_production("<Expression_prime> --> <Empty>")
      return True
    return False
  
  def term(self):
    """
    R27. <Term> ::= <Factor> <Term_prime>
    """
    self.print_production("<Term> --> <Factor> <Term_prime>")
    if self.factor():
      if self.term_prime():
        return True
    return False
  
  def term_prime(self):
    """
    R28. <Term_prime> ::= * <Factor> <Term_prime> | / <Factor> <Term_prime> | <Empty>
    """
    if self.token_is('operator', '*'):
      self.print_production("<Term_prime> --> * <Factor> <Term_prime>")
      if not self.is_checking_recursive() and not self.ignore_symbol_table:
        self.insert_id_pushm_second()
      if self.factor():
        if self.term_prime():
          if not self.is_checking_recursive() and not self.ignore_symbol_table:
            self.insert_id_pushm_first()
            self.asm_instructions.append('M')
          return True
      return False
    elif self.token_is('operator', '/'):
      self.print_production('<Term_prime> --> / <Factor> <Term_prime>')
      if not self.is_checking_recursive() and not self.ignore_symbol_table:
        self.insert_id_pushm_second()
      if self.factor():
        if self.term_prime():
          if not self.is_checking_recursive() and not self.ignore_symbol_table:
            self.insert_id_pushm_first()
            self.asm_instructions.append('D')
          return True
      return False
    elif self.empty():
      self.print_production('<Term_prime> --> <Empty>')
      return True
    return False
  
  def factor(self):
    """
    R29. <Factor> ::= - <Primary> | <Primary>
    """
    if self.token_is('operator', '-'):
      self.print_production('<Factor> --> - <Primary>')
      if self.primary():
        return True
    else:
      self.print_production('<Factor> --> <Primary>')
      if self.primary():
        return True
    return False
  
  def primary(self):
    """
    R30. <Primary> ::= <Identifier> | <Integer> | <Identifier> ( <IDs> ) |
    ( <Expression> ) | <Real> | true | false
    """
    if self.token_is('identifier'):
      if self.token_is('separator', '('):
        self.print_production('<Primary> --> <Identifier> ( <IDs> )')
        if self.IDs():
          if self.token_is('separator', ')'):
            return True
        return False
      else:      
        self.print_production('<Primary> --> <Identifier>')
        if not self.is_checking_recursive() and not self.ignore_symbol_table and self.in_print:
          prev_tok = self.lexer.get_prev_token()
          if not self.symbol_table.exists_identifier(prev_tok):
            err_msg = f"Error: Identifier {prev_tok.value} was not declared"
            self.print_production(err_msg)
            self.asm_instructions.append(err_msg)
            return False
          mem_address = self.symbol_table.get_mem_address(prev_tok)
          self.asm_instructions.append(f"PUSHM {mem_address}")
        return True
    elif self.token_is('integer'):
      self.print_production('<Primary> --> <Integer>')
      int_tok = self.lexer.get_prev_token()
      if int_tok and not self.is_checking_recursive():
        int_val = int_tok.value
        self.asm_instructions.append(f"PUSHI {int_val}")
      return True
    elif self.token_is('separator', '('):
      self.print_production('<Primary> --> ( <Expression> )')
      if self.expression():
        if self.token_is('separator', ')'):
          return True
      return False
    elif self.token_is('real'):
      self.print_production('<Primary> --> <Real>')
      return True
    elif self.token_is('keyword', 'true'):
      self.print_production('<Primary> --> true')
      if not self.is_checking_recursive():
        self.asm_instructions.append('PUSHI 1')
      return True
    elif self.token_is('keyword', 'false'):
      self.print_production('<Primary> --> false')
      if not self.is_checking_recursive():
        self.asm_instructions.append("PUSHI 0")
      return True
    return False
  
  def empty(self):
    """
    R31. <Empty> ::= None
    """
    # Empty alwasys returns True
    return True
