from enum import Enum, auto
from typing import List

class TokenType(Enum):
    LET = auto()
    IF = auto()
    THEN = auto()
    ELSE = auto()
    ENDIF = auto()
    WHILE = auto()
    DO = auto()
    ENDWHILE = auto()
    FOR = auto()
    TO = auto()
    STEP = auto()
    ENDFOR = auto()
    IN = auto()
    REPEAT = auto()
    UNTIL = auto()
    FUNC = auto()
    BEGIN = auto()
    RETURN = auto()
    END = auto()
    CALL = auto()
    
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    EQUAL = auto()
    GREATER = auto()
    LESS = auto()
    NOT_EQUAL = auto()
    AND = auto()
    OR = auto()
    NOT = auto()
    
    PLUS_EQUAL = auto()
    MINUS_EQUAL = auto()
    MULTIPLY_EQUAL = auto()
    DIVIDE_EQUAL = auto()
    GREATER_EQUAL = auto()
    SMALLER_EQUAL = auto()
    EQUAL_EQUAL = auto()
    
    INCREMENT = auto()
    DECREMENT = auto()
    
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    LEFT_BRACKET = auto()
    RIGHT_BRACKET = auto()

    COMMA = auto()
    
    IDENTIFIER = auto()
    NUMBER = auto()
    STRING = auto()
    COMMENT = auto()
    EOF = auto()

class Token:
    def __init__(self, type: TokenType, lexeme: str, line: int, position: int):
        self.type = type
        self.lexeme = lexeme
        self.line = line
        self.position = position
    
    def __str__(self):
        return f"Token: {self.type.name.lower()}, Lexeme: {self.lexeme}"


def print_tokens_table(tokens: List['Token']):
    type_width = max(len("Type"), max(len(token.type.name) for token in tokens))
    lexeme_width = max(len("Lexeme"), max(len(token.lexeme) for token in tokens))
    line_width = max(len("Line"), max(len(str(token.line)) for token in tokens))
    pos_width = max(len("Position"), max(len(str(token.position)) for token in tokens))
    
    border = f"+{'-' * (type_width + 2)}+{'-' * (lexeme_width + 2)}+{'-' * (line_width + 2)}+{'-' * (pos_width + 2)}+"
    
    print("\n\033[1m╔════════════════════════════════════════════╗")
    print("║                 Token Table                ║")
    print("╚════════════════════════════════════════════╝\033[0m")
    
    print(border)
    print(f"| {'Type':<{type_width}} | {'Lexeme':<{lexeme_width}} | {'Line':<{line_width}} | {'Position':<{pos_width}} |")
    print(border)
    
    for token in tokens:
        if token.type != TokenType.EOF:
            print(f"| {token.type.name:<{type_width}} | {token.lexeme:<{lexeme_width}} | {token.line:<{line_width}} | {token.position:<{pos_width}} |")
    
    print(border)