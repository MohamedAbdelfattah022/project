from lexer import LexicalAnalyzer
from tokens import print_tokens_table
from syntax_validation import SyntaxValidator, SyntaxError
from tests import test_cases

def main():
    cnt = 1
    for test_case in test_cases:
        print("==================")
        print(f"\033[92mTest Case {cnt}\033[0m")
        try:
            lexer = LexicalAnalyzer()
            tokens, symbol_table = lexer.tokenize(test_case)
            validator = SyntaxValidator(tokens)
            if validator.validate():
                print_tokens_table(tokens)
                symbol_table.print_table()
        except SyntaxError as e:
            print(f"\033[91mError: {e}\033[0m")
        cnt += 1
        print("==================")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\033[91mError: {e}\033[0m")