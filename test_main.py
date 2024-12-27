from lexer import LexicalAnalyzer
from tokens import print_tokens_table
from syntax_validation import SyntaxValidator, SyntaxError
from tests import test_cases
from parse_tree import ParseTreeNode
from test_cases_phase2 import test_cases_phase2

# Syncing code from other files
def main():
    cnt = 1 
    for test_case in test_cases_phase2:  # Loop over individual test cases
        print("==================")
        print(f"\033[92mTest Case {cnt}\033[0m")  # Green color
        try:
            lexer = LexicalAnalyzer()  # Instance
            tokens, symbol_table = lexer.tokenize(test_case)  # Tokenize the test case
            validator = SyntaxValidator(tokens)
            #print("Tokens:")
            #for token in tokens:
            #    print(token)
            if validator.validate():
                # Uncomment below lines if you want to see tokens and the symbol table
                print_tokens_table(tokens)
                symbol_table.print_table()
                print("\nParse Tree:")
                print(validator.parse_tree)  # Print the parse tree
        except SyntaxError as e:
            print(f"\033[91mError: {e}\033[0m")
        cnt += 1  # Increment for the next test case
        print("==================")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\033[91mError: {e}\033[0m")
