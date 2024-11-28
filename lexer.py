import re
from enum import Enum, auto
from typing import List, Dict, Tuple, Optional
from tokens import Token, TokenType, print_tokens_table
from symbols import SymbolTable

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
            '--': TokenType.DECREMENT,
            '==': TokenType.EQUAL_EQUAL,
            '>=': TokenType.GREATER_EQUAL,
            '<=': TokenType.SMALLER_EQUAL,
        }
        
        self.source_code = ""
        self.tokens: List[Token] = []
        self.current_pos = 0
        self.line = 1
        self.position = 1
        self.symbol_table = SymbolTable()
        
        self.patterns = {
            'number': r'[0-9]+',
            'identifier': r'[a-zA-Z_][a-zA-Z0-9_]*',
            'operator': r'[+\-]{2}|[+\-*/=<>!]=?',
            'delimiter': r'[\(\)\[\],]',
            'whitespace': r'\s+',
            'comment': r'\{[^}]*\}'
        }
        
        self.compiled_patterns = {
            name: re.compile(pattern) 
            for name, pattern in self.patterns.items()
        }
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
        match = self.compiled_patterns['whitespace'].match(
            self.source_code[self.current_pos:]
        )
        if match:
            whitespace = match.group()
            newlines = whitespace.count('\n')
            if newlines > 0:
                self.line += newlines
                self.position = len(whitespace) - whitespace.rindex('\n') if '\n' in whitespace else 1
            else:
                self.position += len(whitespace)
            self.current_pos += len(whitespace)

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
        match = self.compiled_patterns['number'].match(
            self.source_code[self.current_pos:]
        )
        if match:
            number = match.group()
            self.tokens.append(Token(TokenType.NUMBER, number, self.line, self.position))
            self.current_pos += len(number)
            self.position += len(number)

    def _handle_identifier(self):
        match = self.compiled_patterns['identifier'].match(
            self.source_code[self.current_pos:]
        )
        if match:
            lexeme = match.group()
            upper_lexeme = lexeme.upper()
            
            if upper_lexeme in self.keywords:
                token_type = self.keywords[upper_lexeme]
                
                if token_type == TokenType.CALL:
                    next_pos = self.current_pos + len(lexeme)
                    while next_pos < len(self.source_code) and self.source_code[next_pos].isspace():
                        next_pos += 1
                    
                    func_match = self.compiled_patterns['identifier'].match(
                        self.source_code[next_pos:]
                    )
                    if func_match:
                        func_name = func_match.group()
                        params = []
                        
                        next_pos += len(func_name)
                        if next_pos < len(self.source_code) and self.source_code[next_pos] == '(':
                            param_start = next_pos + 1
                            param_end = self.source_code.find(')', param_start)
                            if param_end != -1:
                                param_str = self.source_code[param_start:param_end]
                                params = [p.strip() for p in param_str.split(',') if p.strip()]
                        
                        self.symbol_table.set_symbol(func_name, 'function', params)

            else:
                token_type = TokenType.IDENTIFIER
                
            self.tokens.append(Token(token_type, lexeme, self.line, self.position))
            self.current_pos += len(lexeme)
            self.position += len(lexeme)
            
            if (len(self.tokens) >= 2 and self.tokens[-2].type == TokenType.LET):
                self.symbol_table.set_symbol(lexeme, 'integer')
            elif (len(self.tokens) >= 2 and self.tokens[-2].type == TokenType.FUNC):
                self.symbol_table.set_symbol(lexeme, 'function') 

    def _handle_operator(self):
        match = self.compiled_patterns['operator'].match(
            self.source_code[self.current_pos:]
        )
        if match:
            operator = match.group()
            if operator in self.operators:
                # self.tokens.append(Token(self.operators[operator], operator, self.line, self.position))
                token = Token(self.operators[operator], operator, self.line, self.position)
                self.tokens.append(token)
                # print(f"Debug: Generated token {token}")
                self.current_pos += len(operator)
                self.position += len(operator)
            else:
                raise SyntaxError(f"Invalid operator at line {self.line}, position {self.position}")
