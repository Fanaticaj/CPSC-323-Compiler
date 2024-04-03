"""Recursive Descent Parser for Syntax Analysis"""
from lexer import Lexer

class RDP:
  def __init__(self, lexer):
    self.lexer = lexer
    
  def token_is(self, token_type, token_val=None):
    """
    Return True if next token type of next token in lexer is equal to token_type.
    Enter value for token_val if value of token matters ie. operators, separators, and keywords
    """
    next_token = self.lexer.get_next_token()
    if next_token.type == token_type and token_val == None:
      return True
    elif next_token.type == token_type and token_val == next_token.value:
      return True
    
    # Backtrack if token type not equal to token_type
    self.lexer.backtrack()
    return False
    
  def rat24s(self):
    """
    R1. <Rat24S> ::= $ <Opt Function Definitions> $ <Opt Declaration List> $ <Statement List> $
    """
    print("Token: Symbol          Lexeme: $")
    print("<Rat24S> ::= $ <Opt Function Definitions> $ <Opt Declaration List> $ <Statement List> $")
    if self.token_is('symbol', '$'):
      self.opt_function_definitions()
      if self.token_is('symbol', '$'):
        self.opt_declaration_list()
        if self.token_is('symbol', '$'):
          self.statement_list()
          if self.token_is('symbol', '$'):
            print("Parsing <Rat24S> successful.")
            return True
    print("Parsing <Rat24S> failed.")
    raise NotImplementedError
  
  def opt_function_definitions(self):
    """
    R2. <Opt Function Definitions> ::= <Function Definitions> | <Empty>
    """
    print("<Opt Function Definitions> ::= <Function Definitions> | <Empty>")
    if not self.function_definitions():  # Attempt parsing <Function Definitions>
      self.empty()  # If it fails, treat as empty
      return True

    raise NotImplementedError
  
  def function_definitions(self):
    """
    R3. <Function Definitions> ::= <Function> | <Function> <Function Definitions>
    """
    raise NotImplementedError

  def function(self):
    """
    R4. <Function> ::= function <Identifier> ( <Opt ParaI ggmeter List> ) <Opt Declaration List> <Body>
    """
    print("<Function> ::= function <Identifier> ( <Opt Parameter List> ) <Opt Declaration List> <Body>")
    if self.token_is('keyword', 'function'):
      if self.IDs():
        if self.token_is('separator', '('):
          self.opt_parameter_list()
          if self.token_is('separator', ')'):
            self.opt_declaration_list()
            self.body()
            return True
    raise NotImplementedError
  
  def opt_parameter_list(self):
    """
    R5. <Opt Parameter List> ::= <Parameter List> | <Empty>
    """
    print("<Opt Parameter List> ::= <Parameter List> | <Empty>")
    # Attempt to parse a parameter list. If successful, the parameter_list function will handle its own logging.
    if not self.parameter_list():  # If no parameter list found, treat as empty.
        self.empty()
        return True
  
    raise NotImplementedError
  
  def parameter_list(self):
    """
    R6. <Parameter List> ::= <Parameter> | <Parameter> , <Parameter List>
    """
    print("<Parameter List> ::= <Parameter> | <Parameter>, <Parameter List>")
    if self.parameter():
        # While loop for handling comma-separated parameter list.
        while True:
            current_token = self.lexer.get_next_token()
            if current_token.type == 'separator' and current_token.value == ',':
                self.lexer.get_next_token()
                print("Token: Separator          Lexeme: ,")
                if not self.parameter():
                    print("Error: Expected a parameter after ','.")
                    return False
            else:
                break
    else:
        print("Error: Expected a parameter.")
        return False
    return True
  
    raise NotImplementedError
  
  def parameter(self):
    """
    R7. <Parameter> ::= <IDs> <Qualifier>
    """
    print("<Parameter> ::= <IDs> <Qualifier>")
    if self.IDs() and self.qualifier():
        return True
    return False
    raise NotImplementedError
  
  def body(self):
    """
    R8. <Body> ::= { <Statement List> }
    """
    print("<Body> ::= { <Statement List> }")
    if self.token_is('separator', '{'):
        print("Token: Separator          Lexeme: {")
        if self.statement_list():  # Process the statement list.
            if self.token_is('separator', '}'):
                print("Token: Separator          Lexeme: }")
                return True
            else:
                print("Error: Expected '}' at the end of the body.")
        else:
            print("Error: Invalid statement list inside body.")
    else:
        print("Error: Expected '{' at the beginning of the body.")
    return False
    raise NotImplementedError
  
  def opt_declaration_list(self):
    """
    R9. <Opt Declaration List> ::= <Declaration List> | <Empty>
    """
    raise NotImplementedError
  
  def declaration_list(self):
    """
    R10. <Declaration List> := <Declaration> ; | <Declaration> ; <Declaration List>
    """
    raise NotImplementedError
  
  def declaration(self):
    """
    R11. <Declaration> ::= integer <IDs> | boolean <IDs> | real <IDs>
    """
    raise NotImplementedError
  
  def IDs(self):
    """
    R12. <IDs> ::= <Identifier> | <Identifier>, <IDs>
    """
    next_token = self.lexer.get_next_token()
    if next_token.type == 'identifier':
      print(f"Token: Identifier          Lexeme: {next_token.value}")
      return True
    self.lexer.backtrack()

    raise NotImplementedError
  
  def statement_list(self):
    """
    R13. <Statement List> ::= <Statement> | <Statement> <Statement List>
    """
    raise NotImplementedError
  
  def statement(self):
    """
    R14. <Statement> ::= <Compound> | <Assign> | <If> | <Return> | <Print> | <Scan> | <While>
    """
    raise NotImplementedError
  
  def compound(self):
    """
    R15. <Compound> ::= { <Statement List> }
    """
    raise NotImplementedError
  
  def assign(self):
    """
    R16. <Assign> ::= <Identifier> = <Expression> ;
    """
    raise NotImplementedError
  
  def If(self):
    """
    R17. <If> ::= if ( <Condition> ) <Statement> <If_prime>
    """
    raise NotImplementedError
  
  def If_prime(self):
    """
    R18. <If_prime> ::= endif | else <Statement> endif
    """
    raise NotImplementedError
  
  def Return(self):
    """
    R19. <Return> ::= return ; | return <Expression> ;
    """
    raise NotImplementedError
  
  def Print(self):
    """
    R20. <Print> ::= print ( <Expression>);
    """
    raise NotImplementedError
  
  def scan(self):
    """
    R21. <Scan> ::= scan ( <IDs> );
    """
    if self.token_is('keyword', 'scan'):
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
    raise NotImplementedError
  
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
    raise NotImplementedError
  
  def expression_prime(self):
    """
    R26. <Expression_prime> ::= + <Term> <Expression_prime> | - <Term> <Expression_prime> | <Empty>
    """
    raise NotImplementedError
  
  def term(self):
    """
    R27. <Term> ::= <Factor> <Term_prime>
    """
    raise NotImplementedError
  
  def term_prime(self):
    """
    R28. <Term_prime> ::= * <Factor> <Term_prime> | / <Factor> <Term_prime> | <Empty>
    """
    raise NotImplementedError
  
  def factor(self):
    """
    R29. <Factor> ::= - <Primary> | <Primary>
    """
    raise NotImplementedError
  
  def primary(self):
    """
    R30. <Primary> ::= <Identifier> | <Integer> | <Identifier> ( <IDs> ) | ( <Expression> ) | <Real> | true | false
    """
    raise NotImplementedError
  
  def empty(self):
    """
    R31. <Empty> ::= None
    """
    raise NotImplementedError