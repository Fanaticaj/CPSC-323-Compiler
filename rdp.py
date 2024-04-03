"""Recursive Descent Parser for Syntax Analysis"""

class RDP:
  def __init__(self, lexer):
    self.lexer = lexer
    
  def token_is(self, token_type):
    """Return True if next token type from next token in lexer is equal to token_type"""
    next_token = self.lexer.get_next_token()
    if next_token.type == token_type:
      return True
    
  def rat24s(self):
    """
    R1. <Rat24S> ::= $ <Opt Function Definitions> $ <Opt Declaration List> $ <Statement List> $
    """
    raise NotImplementedError
  
  def opt_function_definitions(self):
    """
    R2. <Opt Function Definitions> ::= <Function Definitions> | <Empty>
    """
    raise NotImplementedError
  
  def function_definitions(self):
    """
    R3. <Function Definitions> ::= <Function> | <Function> <Function Definitions>
    """
    raise NotImplementedError

  def function(self):
    """
    R4. <Function> ::= function <Identifier> ( <Opt Parameter List> ) <Opt Declaration List> <Body>
    """
    raise NotImplementedError
  
  def opt_parameter_list(self):
    """
    R5. <Opt Parameter List> ::= <Parameter List> | <Empty>
    """
    raise NotImplementedError
  
  def parameter_list(self):
    """
    R6. <Parameter List> ::= <Parameter> | <Parameter> , <Parameter List>
    """
    raise NotImplementedError
  
  def parameter(self):
    """
    R7. <Parameter> ::= <IDs> <Qualifier>
    """
    raise NotImplementedError
  
  def body(self):
    """
    R8. <Body> ::= { <Statement List> }
    """
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
    raise NotImplementedError
  
  def While(self):
    """
    R22. <While> ::= while ( <Condition> ) <Statement> endwhile
    """
    raise NotImplementedError
  
  def condition(self):
    """
    R23. <Condition> ::= <Expression> <Relop> <Expression>
    """
    raise NotImplementedError
  
  def relop(self):
    """
    R24. <Relop> ::= == | != | > | < | <= | =>
    """
    raise NotImplementedError
  
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