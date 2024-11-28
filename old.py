import re
from enum import Enum, auto
from typing import List, Dict, Tuple, Optional

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

class SymbolTable:
    def __init__(self):
        self.symbols: Dict[str, Dict] = {}
    
    def set_symbol(self, name: str, type: str, params: List[str] = None):
        self.symbols[name] = {
            'type': type,
            'parameters': params if params else []
        }
    
    def get_symbol(self, name: str) -> Optional[Dict]:
        return self.symbols.get(name)
    
    def print_table(self):
        name_width = max(len("Name"), max((len(name) for name in self.symbols.keys())))
        type_width = max(len("Type"), max((len(info['type']) for info in self.symbols.values())))
        params_width = max(len("Parameters"), max((len(', '.join(info['parameters'])) 
                                                for info in self.symbols.values())))
        
        horizontal_line = f"+{'-' * (name_width + 2)}+{'-' * (type_width + 2)}+{'-' * (params_width + 2)}+"
        
        print("\n\033[1m╔════════════════════════════════════╗")
        print("║            Symbol Table            ║")
        print("╚════════════════════════════════════╝\033[0m")


        print(horizontal_line)
        print(f"| {'Name':<{name_width}} | {'Type':<{type_width}} | {'Parameters':<{params_width}} |")
        print(horizontal_line)
        
        for name, info in self.symbols.items():
            params = ', '.join(info['parameters']) if info['parameters'] else ''
            print(f"| {name:<{name_width}} | {info['type']:<{type_width}} | {params:<{params_width}} |")
        
        print(horizontal_line)

class LexicalAnalyzer:
    def __init__(self):
        self.keywords = {
            'LET': TokenType.LET,
            'IF': TokenType.IF,
            'THEN': TokenType.THEN,
            'ELSE': TokenType.ELSE,
            'ENDIF': TokenType.ENDIF,
            'WHILE': TokenType.WHILE,
            'DO': TokenType.DO,
            'ENDWHILE': TokenType.ENDWHILE,
            'FOR': TokenType.FOR,
            'TO': TokenType.TO,
            'STEP': TokenType.STEP,
            'ENDFOR': TokenType.ENDFOR,
            'IN': TokenType.IN,
            'REPEAT': TokenType.REPEAT,
            'UNTIL': TokenType.UNTIL,
            'FUNC': TokenType.FUNC,
            'BEGIN': TokenType.BEGIN,
            'RETURN': TokenType.RETURN,
            'END': TokenType.END,
            'CALL': TokenType.CALL,
            'AND': TokenType.AND,
            'OR': TokenType.OR,
            'NOT': TokenType.NOT
        }
        
        self.operators = {
            '+': TokenType.PLUS,
            '-': TokenType.MINUS,
            '*': TokenType.MULTIPLY,
            '/': TokenType.DIVIDE,
            '=': TokenType.EQUAL,
            '>': TokenType.GREATER,
            '<': TokenType.LESS,
            '!=': TokenType.NOT_EQUAL,
            '+=': TokenType.PLUS_EQUAL,
            '-=': TokenType.MINUS_EQUAL,
            '*=': TokenType.MULTIPLY_EQUAL,
            '/=': TokenType.DIVIDE_EQUAL,
            '++': TokenType.INCREMENT,
            '--': TokenType.DECREMENT
        }
        
        self.source_code = ""
        self.tokens: List[Token] = []
        self.current_pos = 0
        self.line = 1
        self.position = 1
        self.symbol_table = SymbolTable()

    def tokenize(self, source_code: str) -> Tuple[List[Token], SymbolTable]:
        self.source_code = source_code.strip()
        self.current_pos = 0
        self.tokens = []
        
        while self.current_pos < len(self.source_code):
            self._skip_whitespace()
            if self.current_pos >= len(self.source_code):
                break
            
            char = self.source_code[self.current_pos]
            
            if char == '{':
                self._handle_comment()
                continue
            
            if char.isdigit():
                self._handle_number()
                continue
            
            if char.isalpha() or char == '_':
                self._handle_identifier()
                continue
            
            if char in '+-*/><=!':
                self._handle_operator()
                continue
            
            if char == '(':
                self.tokens.append(Token(TokenType.LEFT_PAREN, '(', self.line, self.position))
            elif char == ')':
                self.tokens.append(Token(TokenType.RIGHT_PAREN, ')', self.line, self.position))
            elif char == '[':
                self.tokens.append(Token(TokenType.LEFT_BRACKET, '[', self.line, self.position))
            elif char == ']':
                self.tokens.append(Token(TokenType.RIGHT_BRACKET, ']', self.line, self.position))
            elif char == ',':
                self.tokens.append(Token(TokenType.COMMA, ',', self.line, self.position))
            
            self.current_pos += 1
            self.position += 1
        
        self.tokens.append(Token(TokenType.EOF, "", self.line, self.position))
        return self.tokens, self.symbol_table

    def _skip_whitespace(self):
        while (self.current_pos < len(self.source_code) and 
               self.source_code[self.current_pos].isspace()):
            if self.source_code[self.current_pos] == '\n':
                self.line += 1
                self.position = 1
            else:
                self.position += 1
            self.current_pos += 1

    def _handle_comment(self):
        self.current_pos += 1
        self.position += 1
        
        while (self.current_pos < len(self.source_code) and self.source_code[self.current_pos] != '}'):
            if self.source_code[self.current_pos] == '\n':
                self.line += 1
                self.position = 1
            else:
                self.position += 1
            self.current_pos += 1
        
        if self.current_pos >= len(self.source_code):
            raise SyntaxError(f"Unclosed comment starting at line {self.line}")
        
        self.current_pos += 1
        self.position += 1

    def _handle_number(self):
        start_pos = self.current_pos
        while (self.current_pos < len(self.source_code) and self.source_code[self.current_pos].isdigit()):
            self.current_pos += 1
            self.position += 1
        
        number = self.source_code[start_pos:self.current_pos]
        self.tokens.append(Token(TokenType.NUMBER, number, self.line, self.position - len(number)))
        self.symbol_table.set_symbol(number, 'integer')

    def _handle_identifier(self):
        start_pos = self.current_pos
        while (self.current_pos < len(self.source_code) and (self.source_code[self.current_pos].isalnum() or 
                self.source_code[self.current_pos] == '_')):
            self.current_pos += 1
            self.position += 1
        
        lexeme = self.source_code[start_pos:self.current_pos]
        upper_lexeme = lexeme.upper() 
        
        if upper_lexeme in self.keywords:
            self.tokens.append(Token(self.keywords[upper_lexeme], lexeme, self.line, self.position - len(lexeme)))
        else:
            self.tokens.append(Token(TokenType.IDENTIFIER, lexeme, self.line, self.position - len(lexeme)))
            
            if (len(self.tokens) >= 2 and self.tokens[-2].type == TokenType.LET):
                self.symbol_table.set_symbol(lexeme, 'integer')
            elif (len(self.tokens) >= 2 and self.tokens[-2].type == TokenType.FUNC):
                self.symbol_table.set_symbol(lexeme, 'function')

    def _handle_operator(self):
        current_char = self.source_code[self.current_pos]
        next_char = (self.source_code[self.current_pos + 1] if self.current_pos + 1 < len(self.source_code) else '')
        
        if current_char + next_char in self.operators:
            operator = current_char + next_char
            self.tokens.append(Token(self.operators[operator], operator, self.line, self.position))
            self.current_pos += 2
            self.position += 2
            
        elif current_char in self.operators:
            self.tokens.append(Token(self.operators[current_char], current_char, self.line, self.position))
            self.current_pos += 1
            self.position += 1
        else:
            raise SyntaxError(f"Invalid operator at line {self.line}, position {self.position}")



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



def main():
    test_code = """
    LET a = 5
    LET b = 10
    IF a < b
    THEN
        LET c = a + b
        LET d = c * 2
    ELSE
        LET e = a - b
    ENDIF
    CALL myFunction(a, b)
    """
    
    lexer = LexicalAnalyzer()
    try:
        tokens, symbol_table = lexer.tokenize(test_code)
        print_tokens_table(tokens)
        symbol_table.set_symbol('myFunction', 'function', ['a', 'b'])
        symbol_table.print_table()
    except SyntaxError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

