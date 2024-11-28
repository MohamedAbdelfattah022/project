from typing import List, Optional
from enum import Enum
from tokens import Token, TokenType

class SyntaxError(Exception):
    def __init__(self, message: str, line: int, position: int):
        super().__init__(f"Syntax Error at line {line}, position {position}: {message}")
        self.message = message
        self.line = line
        self.position = position


class SyntaxValidator:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.current = 0
        self.scope_stack = []
        self.in_function = False
        self.had_return = False

    def validate(self) -> bool:
        while not self._is_at_end():
            self._validate_statement()

        if self.scope_stack:
            unclosed_scope = self.scope_stack.pop()
            raise SyntaxError(
                f"Unclosed {unclosed_scope} statement",
                self._peek().line,
                self._peek().position
            )
        return True

    # ----------------------------------------
    # Main Statement Validation
    # ----------------------------------------

    def _validate_statement(self):
        token = self._peek()

        if token.type == TokenType.IDENTIFIER and (
            self._check_next(TokenType.INCREMENT) or 
            self._check_next(TokenType.DECREMENT)
        ):
            self._validate_increment_decrement()
            return

        validation_map = {
            TokenType.LET: self._validate_let_statement,
            TokenType.IF: self._validate_if_statement,
            TokenType.WHILE: self._validate_while_statement,
            TokenType.FOR: self._validate_for_statement,
            TokenType.DO: self._validate_do_while_statement,
            TokenType.REPEAT: self._validate_repeat_until_statement,
            TokenType.FUNC: self._validate_function_definition,
            TokenType.CALL: self._validate_function_call,
            TokenType.RETURN: self._validate_return_statement, 
        }

        if token.type in validation_map:
            validation_map[token.type]()
        elif self._is_compound_assignment_ahead():
            self._validate_compound_assignment()
        else:
            raise SyntaxError(
                f"Unexpected token: {token.lexeme}",
                token.line,
                token.position
            )    

    # ----------------------------------------
    # Specific Statement Handlers
    # ----------------------------------------

    def _validate_let_statement(self):
        """Validate a LET statement."""
        self._consume(TokenType.LET, "Expected 'LET'")
        self._consume(TokenType.IDENTIFIER, "Expected identifier after 'LET'")
        
        # array indexing in assignment
        while self._match(TokenType.LEFT_BRACKET):
            self._validate_expression()
            self._consume(TokenType.RIGHT_BRACKET, "Expected ']' after index")
        
        self._consume(TokenType.EQUAL, "Expected '=' after identifier")
        self._validate_expression()

    def _validate_if_statement(self):
        """Validate an IF statement."""
        self._consume(TokenType.IF, "Expected 'IF'")
        self._validate_condition() 
        self._consume(TokenType.THEN, "Expected 'THEN' after condition")
        self.scope_stack.append("IF")

        self._validate_block(TokenType.ENDIF, TokenType.ELSE)

        self.scope_stack.pop()


    def _validate_while_statement(self):
        self._consume(TokenType.WHILE, "Expected 'WHILE'")
        self._validate_condition()
        self._consume(TokenType.DO, "Expected 'DO' after condition")
        self.scope_stack.append("WHILE")

        self._validate_block(TokenType.ENDWHILE)

        self.scope_stack.pop()

    def _validate_for_statement(self):
        self._consume(TokenType.FOR, "Expected 'FOR'")
        self._consume(TokenType.IDENTIFIER, "Expected identifier after 'FOR'")
        
        if self._check(TokenType.IN):
            self._advance()
            self._consume(TokenType.IDENTIFIER, "Expected Range function")
            self._consume(TokenType.LEFT_PAREN, "Expected '(' after Range")
            self._validate_expression()
            self._consume(TokenType.COMMA, "Expected ',' after start value")
            self._validate_expression()
            self._consume(TokenType.COMMA, "Expected ',' after end value")
            self._validate_expression()
            self._consume(TokenType.RIGHT_PAREN, "Expected ')' after Range parameters")
        else:
            self._consume(TokenType.EQUAL, "Expected '=' after identifier")
            self._validate_expression()
            self._consume(TokenType.TO, "Expected 'TO'")
            self._validate_expression()
            if self._match(TokenType.STEP):
                self._validate_expression()

        self._consume(TokenType.DO, "Expected 'DO'")
        self.scope_stack.append("FOR")
        self._validate_block(TokenType.ENDFOR)
        self.scope_stack.pop()

    def _validate_do_while_statement(self):
        self._consume(TokenType.DO, "Expected 'DO'")
        self.scope_stack.append("DO")

        while not self._check(TokenType.WHILE):
            self._validate_statement()

        self._consume(TokenType.WHILE, "Expected 'WHILE'")
        self._validate_condition()
        self.scope_stack.pop()

    def _validate_repeat_until_statement(self):
        self._consume(TokenType.REPEAT, "Expected 'REPEAT'")
        self.scope_stack.append("REPEAT")

        while not self._check(TokenType.UNTIL):
            self._validate_statement()

        self._consume(TokenType.UNTIL, "Expected 'UNTIL'")
        self._validate_condition()
        self.scope_stack.pop()

    def _validate_function_definition(self):
        self._consume(TokenType.FUNC, "Expected 'FUNC'")
        self._consume(TokenType.IDENTIFIER, "Expected function name")
        self._consume(TokenType.LEFT_PAREN, "Expected '(' after function name")
        self._validate_parameter_list()

        self._consume(TokenType.RIGHT_PAREN, "Expected ')' after parameters")
        self._consume(TokenType.BEGIN, "Expected 'BEGIN'")
        self.scope_stack.append("FUNC")

        self.in_function = True
        self.had_return = False
        
        self._validate_block(TokenType.END)

        if not self.had_return:
            raise SyntaxError(
                "Function must have a RETURN statement",
                self._peek().line,
                self._peek().position
            )

        self.scope_stack.pop()
        self.in_function = False
        self.had_return = False

    def _validate_return_statement(self):
        self._consume(TokenType.RETURN, "Expected 'RETURN'")
        if not self._check(TokenType.END):
            self._validate_expression()
        self.had_return = True

    def _validate_function_call(self):
        self._consume(TokenType.CALL, "Expected 'CALL'")
        self._consume(TokenType.IDENTIFIER, "Expected function name")

        if self._match(TokenType.LEFT_PAREN):
            if not self._check(TokenType.RIGHT_PAREN):
                self._validate_parameter_list()
            self._consume(TokenType.RIGHT_PAREN, "Expected ')' after parameters")

    # ----------------------------------------
    # Utility Functions
    # ----------------------------------------

    def _validate_block(self, end_token: TokenType, optional_mid_token: Optional[TokenType] = None):
        """
        Validate a block of statements until an end token.
        Args:
            end_token (TokenType): the end token of the block.
            optional_mid_token (Optional[TokenType]): optional token that can appear within the block.
        """
        while not self._check(end_token) and (optional_mid_token is None or not self._check(optional_mid_token)):
            self._validate_statement()

        if optional_mid_token and self._match(optional_mid_token):
            while not self._check(end_token):
                self._validate_statement()

        self._consume(end_token, f"Expected '{end_token.name}'")

    def _validate_condition(self):
        self._validate_expression()

        while self._peek().type in {TokenType.EQUAL, TokenType.NOT_EQUAL, TokenType.GREATER, TokenType.LESS,
                                    TokenType.GREATER_EQUAL, TokenType.SMALLER_EQUAL, TokenType.AND, TokenType.OR, TokenType.NOT}:
            self._advance()
            self._validate_expression()


    def _validate_expression(self):
        self._validate_term()
        while self._is_arithmetic_operator():
            self._advance()
            self._validate_term()

    def _validate_term(self):
        if self._match(TokenType.NUMBER) or self._match(TokenType.STRING):
            return
        
        if self._match(TokenType.LEFT_BRACKET):
            if not self._check(TokenType.RIGHT_BRACKET):
                self._validate_expression()
                while self._match(TokenType.COMMA):
                    self._validate_expression()
            self._consume(TokenType.RIGHT_BRACKET, "Expected ']' after array elements")
            return
        
        # array access: arr[index] or arr[row][col]
        if self._match(TokenType.IDENTIFIER):
            while self._match(TokenType.LEFT_BRACKET):
                self._validate_expression()
                self._consume(TokenType.RIGHT_BRACKET, "Expected ']' after index")
            return
        
        if self._match(TokenType.LEFT_PAREN):
            self._validate_expression()
            self._consume(TokenType.RIGHT_PAREN, "Expected ')' after expression")
            return
        
        if self._match(TokenType.CALL):
            self._consume(TokenType.IDENTIFIER, "Expected function name")
            if self._match(TokenType.LEFT_PAREN):
                self._validate_expression()
                while self._match(TokenType.COMMA):
                    self._validate_expression()
                self._consume(TokenType.RIGHT_PAREN, "Expected ')' after parameters")
            return
        
        raise SyntaxError("Expected a valid term", self._peek().line, self._peek().position) 
    
    def _advance(self) -> Token:
        if not self._is_at_end():
            self.current += 1
        return self.tokens[self.current - 1]

    def _peek(self) -> Token:
        return self.tokens[self.current]

    def _check(self, token_type: TokenType) -> bool:
        return not self._is_at_end() and self._peek().type == token_type

    def _match(self, token_type: TokenType) -> bool:
        if self._check(token_type):
            self._advance()
            return True
        return False

    def _consume(self, token_type: TokenType, error_message: str) -> Token:
        if self._check(token_type):
            return self._advance()
        raise SyntaxError(error_message, self._peek().line, self._peek().position)

    def _is_at_end(self) -> bool:
        return self._peek().type == TokenType.EOF

    def _is_arithmetic_operator(self) -> bool:
        return self._peek().type in {TokenType.PLUS, TokenType.MINUS, TokenType.MULTIPLY, TokenType.DIVIDE}

    def _is_compound_assignment_ahead(self) -> bool:
        if self.current + 1 >= len(self.tokens):
            return False
        return self.tokens[self.current + 1].type in {
            TokenType.PLUS_EQUAL,
            TokenType.MINUS_EQUAL,
            TokenType.MULTIPLY_EQUAL,
            TokenType.DIVIDE_EQUAL,
        }

    def _is_increment_decrement(self) -> bool:
        return self._peek().type in {TokenType.INCREMENT, TokenType.DECREMENT}

    def _validate_increment_decrement(self):
        self._consume(TokenType.IDENTIFIER, "Expected identifier before increment/decrement")
        if not self._match(TokenType.INCREMENT) and not self._match(TokenType.DECREMENT):
            raise SyntaxError(
                "Expected '++' or '--'",
                self._peek().line,
                self._peek().position
            )

    def _check_next(self, token_type: TokenType) -> bool:
        """Check if the next token without consuming it."""
        if self.current + 1 >= len(self.tokens):
            return False
        return self.tokens[self.current + 1].type == token_type

    def _validate_parameter_list(self):
        if self._match(TokenType.IDENTIFIER):
            while self._match(TokenType.COMMA):
                self._consume(TokenType.IDENTIFIER, "Expected parameter name after ','")

    def _validate_compound_assignment(self):
        """Validate compound assignment statements like +=, -=, *=, /="""
        self._consume(TokenType.IDENTIFIER, "Expected identifier before compound assignment")
        if not self._match(TokenType.PLUS_EQUAL) and \
        not self._match(TokenType.MINUS_EQUAL) and \
        not self._match(TokenType.MULTIPLY_EQUAL) and \
        not self._match(TokenType.DIVIDE_EQUAL):
            raise SyntaxError(
                "Expected '+=', '-=', '*=' or '/='",
                self._peek().line,
                self._peek().position
            )
        self._validate_expression()
