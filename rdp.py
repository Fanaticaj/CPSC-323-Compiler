"""Recursive Descent Parser for Syntax Analysis"""
from lexer import Lexer

class RDP:
  def __init__(self, lexer, print_to_console=True, write_to_file=True):
    self.lexer = lexer
    self.print_to_console = print_to_console
    self.write_to_file = write_to_file
    self.print_buffer = []  # Used to print tokens after printing production
    # Store left-hand side of production until right-hand side is determined
    self.print_production_buffer = []
    
  def token_is(self, token_type, token_val=None):
    """
    Return True if next token type of next token in lexer is equal to token_type.
    Enter value for token_val if value of token matters ie. operators, separators, and keywords
    """
    next_token = self.lexer.get_next_token()
    if next_token is None:
      return False
    if next_token.type == token_type and token_val == None:
      last_token = self.lexer.get_prev_token()
      self.print_token(last_token)
      self.push_to_print_buffer(last_token)
      return True
    elif next_token.type == token_type and token_val == next_token.value:
      last_token = self.lexer.get_prev_token()
      self.print_token(last_token)
      self.push_to_print_buffer(last_token)
      return True
    
    # Backtrack if token type not equal to token_type
    self.lexer.backtrack()
    return False
  
  def print_production(self, production, *, to_be_continued=False):
    """Print and append to file the current production"""
    if self.print_to_console:
      if to_be_continued:
        self.print_production_buffer.append(production)
      else:
        print(f"{'':2}{production}")
        
  def finish_production_print(self, production):
    """Print the right hand side of a production that was started but not finished"""
    left_hand_side = ' '.join(self.print_production_buffer)
    self.print_production_buffer.clear()
    print(f"{'':2}{left_hand_side} {production}")


  def print_token(self, token):
    """Print token and append to file a token"""
    if self.print_to_console:
      print(f"Token: {token.type:15} Lexeme: {token.value}")
      
  def push_to_print_buffer(self, token):
    """Push token to print buffer to be printed later"""
    self.print_buffer.append(token)
    
  def clear_print_buffer(self):
    """Clear print buffer once all tokens have been printed"""
    self.print_buffer.clear()
    
  def print_token_buffer(self):
    """Print all tokens in print buffer and clear buffer"""
    for token in self.print_buffer:
      self.print_token(token)
    self.clear_print_buffer()
          
  def rat24s(self):
      """
      R1. <Rat24S> ::= $ <Opt Function Definitions> $ <Opt Declaration List> $ <Statement List> $
      """
      self.print_production("<Rat24S> --> $ <Opt Function Definitions> $ <Opt Declaration List> $ <Statement List> $")
      # Check for the first $ symbol.
      if not self.token_is('separator', '$'):
          print("Error: Expected '$' at the beginning of the program.")
          return False

      # Optionally parse function definitions.
      if not self.opt_function_definitions():
          print("Error: Issue parsing optional function definitions.")
          return False

      # Check for the $ symbol after optional function definitions.
      if not self.token_is('separator', '$'):
          print("Error: Expected '$' after optional function definitions.")
          return False

      # Optionally parse declaration list.
      if not self.opt_declaration_list():
          print("Error: Issue parsing optional declaration list.")
          return False

      # Check for the $ symbol after optional declaration list.
      if not self.token_is('separator', '$'):
          print("Error: Expected '$' after optional declaration list.")
          return False

      # Parse statement list.
      if not self.statement_list():
          print("Error: Issue parsing statement list.")
          return False

      # Check for the final $ symbol indicating the end of the program.
      if not self.token_is('separator', '$'):
          print("Error: Expected final '$' at the end of the program.")
          return False
      return True

  def opt_function_definitions(self):
    """
    R2. <Opt Function Definitions> ::= <Function Definitions> | <Empty>
    """
    if self.function_definitions():
      self.print_production("<Opt Function Definitions> --> <Function Definitions>")
      return True
    elif self.empty():
      self.print_production("<Opt Function Definitions> --> <Empty>")
      return True
    return False
  
  def function_definitions(self):
    """
    R3. <Function Definitions> ::= <Function> | <Function> <Function Definitions>
    """
    if self.function():
      if self.function_definitions():
        return True
      return True
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
                                  print("Error: Invalid function body.")
                          else:
                              print("Error: Issue within optional declaration list.")
                      else:
                          print("Error: Expected ')' after parameters.")
                  else:
                      print("Error: Issue within optional parameter list.")
              else:
                  print("Error: Expected '(' after function name.")
          else:
              print("Error: Expected identifier after 'function' keyword.")
      return False

  
  def opt_parameter_list(self):
    """
    R5. <Opt Parameter List> ::= <Parameter List> | <Empty>
    """
    # Attempt to parse a parameter list. If successful, the parameter_list function will handle its own logging.
    if self.parameter_list():  # If no parameter list found, treat as empty.
        return True
    else:
      self.empty()
      return True
  
  def parameter_list(self):
      """
      R6. <Parameter List> ::= <Parameter> | <Parameter>, <Parameter List>
      """
      if self.parameter():
          # While loop for handling comma-separated parameter list.
          while True:
              # Utilize token_is for checking the comma separator.
              if self.token_is('separator', ','):
                  print("Token: Separator          Lexeme: ,")
                  if not self.parameter():
                      print("Error: Expected a parameter after ','.")
                      return False
              else:
                  # If token_is returned False, it means the next token is not a comma,
                  # and the lexer's position has been reset by backtrack in token_is.
                  # This means we are ready to exit the loop.
                  break
      else:
          return False
      return True
  
  def parameter(self):
    """
    R7. <Parameter> ::= <IDs> <Qualifier>
    """
    if self.IDs() and self.qualifier():
        return True
    return False
    
  def qualifier(self):
    """
    R8. <Qualifier> ::= integer | boolean | real
    """
    if self.token_is('keyword', 'integer'):
      return True
    elif self.token_is('keyword', 'boolean'):
      return True
    elif self.token_is('keyword', 'real'):
      return True
    return False
  
  def body(self):
    """
    R8. <Body> ::= { <Statement List> }
    """
    if self.token_is('separator', '{'):
        if self.statement_list():  # Process the statement list.
            if self.token_is('separator', '}'):
                return True
            else:
                print("Error: Expected '}' at the end of the body.")
        else:
            print("Error: Invalid statement list inside body.")
    else:
        print("Error: Expected '{' at the beginning of the body.")
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
          if self.declaration_list():
              return True
          else:
              return False
      else:
          # If the next token does not indicate the start of a declaration list or if we're at the end of input, treat this as an empty list.
          self.empty()
          return True  # Return True because the declaration list is optional and absence of a declaration list is not an error.
  
  def declaration_list(self):
      """
      R10. <Declaration List> := <Declaration> ; | <Declaration> ; <Declaration List>
      """
      # Attempt the first declaration.
      if not self.declaration():
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
      
      return True
  
  def declaration(self):
    """
    R11. <Declaration> ::= integer <IDs> | boolean <IDs> | real <IDs>
    """
    # Use token_is to check for and consume the type keyword in one step.
    if self.token_is('keyword', 'integer') or self.token_is('keyword', 'boolean') or self.token_is('keyword', 'real'):
        # Proceed to parse the IDs.
        if not self.IDs():
            print("Error: Expected identifier list after type keyword.")
            return False

        # If we successfully parse the IDs after the type keyword, the declaration is successful.
        return True
    else:
        # If the next token is not a type keyword, it's not a declaration.
        return False

  def IDs(self):
      """
      R12. <IDs> ::= <Identifier> | <Identifier>, <IDs>
      """
      # Attempt to parse the first identifier.
      if self.token_is('identifier'):
          # Successfully parsed an identifier, now look for a comma indicating more identifiers.
          while self.token_is('separator', ','):
              if not self.token_is('identifier'):
                  print("Error: Expected an identifier after ','.")
                  return False
          return True
      else:
          return False

  def statement_list(self):
    """
    R13. <Statement List> ::= <Statement> | <Statement> <Statement List>
    """
    if self.statement():
      if self.statement_list():
        return True
      return True
    return False
  
  def statement(self):
    """
    R14. <Statement> ::= <Compound> | <Assign> | <If> | <Return> | <Print> | <Scan> | <While>
    """
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
      if self.token_is('operator', '='):
        if self.expression():
          if self.token_is('separator', ';'):
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
      return True
    elif self.token_is('keyword','else'):
      if self.token_is('separator','{'):
        if self.statement():
           if self.token_is('separator','}'):
              if self.token_is('keyword','endif'):
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
  
  def Return(self):
    """
    R19. <Return> ::= return ; | return <Expression> ;
    """
    if self.token_is('keyword', 'return'):
      self.finish_production_print("<Return>")
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
    if self.token_is('keyword', 'print'):
      self.finish_production_print("<Print>")
      if self.token_is('separator', '('):
        if self.expression():
          if self.token_is('separator', ')'):
            if self.token_is('separator', ';'):
              return True
            else:
              return False
        else:
          return False
      else:
        return False
    else:
      return False
  
  def scan(self):
    """
    R21. <Scan> ::= scan ( <IDs> );
    """
    if self.token_is('keyword', 'scan'):
      self.finish_production_print("<Scan>")
      if self.token_is('separator', '('):
        if self.IDs():
          if self.token_is('separator', ')'):
            if self.token_is('separator', ';'):
              return True
            else:
              return False
        else:
          return False
      else:
        return False
    else:
      return False
      
  def While(self):
    """
    R22. <While> ::= while ( <Condition> ) <Statement> endwhile
    """
    if self.token_is('keyword', 'while'):
      self.finish_production_print("<While>")
      if self.token_is('separator', '('):
        if self.condition():
          if self.token_is('separator', ')'):
            if self.statement():
              if self.token_is('keyword', 'endwhile'):
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
      
  def condition(self):
    """
    R23. <Condition> ::= <Expression> <Relop> <Expression>
    """
    if self.expression():
      if self.relop():
        if self.expression():
          return True
        else:
          return False
      else:
        return False
    else:
      return False
  
  def relop(self):
    """
    R24. <Relop> ::= == | != | > | < | <= | =>
    """
    operators = set(['==', '!=', '>', '<', '<=', '=>'])
    next_token = self.lexer.get_next_token()
    if next_token.type == 'operator' and next_token.value in operators:
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
      else:
        return False
    else:
      return False
  
  def expression_prime(self):
    """
    R26. <Expression_prime> ::= + <Term> <Expression_prime> | - <Term> <Expression_prime> | <Empty>
    """
    if self.token_is('operator', '+'):
      self.print_production("<Expression_prime> --> + <Term> <Expression_prime>")
      if self.term():
        if self.expression_prime():
          return True
        else:
          return False
      else:
        return False
    elif self.token_is('operator', '-'):
      self.print_production("<Expression_prime> --> - <Term> <Expression_prime>")
      if self.term():
        if self.expression_prime():
          return True
        else:
          return False
      else:
        return False
    elif self.empty():
      self.print_production("<Expression_prime> --> <Empty>")
      return True
    else:
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
      if self.factor():
        if self.term_prime():
          return True
        else:
          return False
      else:
        return False
    elif self.token_is('operator', '/'):
      self.print_production('<Term_prime> --> / <Factor> <Term_prime>')
      if self.factor():
        if self.term_prime():
          return True
        else:
          return False
      else:
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
          else:
            return False
        else:
          return False
      else:      
        self.print_production('<Primary> --> <Identifier>')
        return True
    elif self.token_is('integer'):
      self.print_production('<Primary> --> <Integer>')
      return True
    elif self.token_is('separator', '('):
      self.print_production('<Primary> --> ( <Expression> )')
      if self.expression():
        if self.token_is('separator', ')'):
          return True
        else:
          return False
      else:
        return False
    elif self.token_is('real'):
      self.print_production('<Primary> --> <Real>')
      return True
    elif self.token_is('keyword', 'true'):
      self.print_production('<Primary> --> true')
      return True
    elif self.token_is('keyword', 'false'):
      self.print_production('<Primary> --> false')
      return True
    
    return False
  
  def empty(self):
    """
    R31. <Empty> ::= None
    """
    return True
