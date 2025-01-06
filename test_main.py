from lexer import LexicalAnalyzer
from tokens import print_tokens_table
from syntax_validation import SyntaxValidator, SyntaxError
from parse_tree import ParseTreeNode
from test_cases_phase2 import test_cases_phase2

# Syncing code from other files
def main():
    cnt = 1 
    with open("parse_trees_output.txt", "w") as output_file:  # Open a file for writing
        for test_case in test_cases_phase2:  # Loop over individual test cases
            output_file.write("==================\n")
            output_file.write(f"Test Case {cnt}\n")
            print("==================")
            print(f"\033[92mTest Case {cnt}\033[0m")  # Green color
            try:
                lexer = LexicalAnalyzer()  # Instance
                tokens, symbol_table = lexer.tokenize(test_case)  # Tokenize the test case
                validator = SyntaxValidator(tokens)
                
                if validator.validate():
                    # Uncomment below lines if you want to see tokens and the symbol table
                    # print_tokens_table(tokens)
                    # symbol_table.print_table()
                    print("\nParse Tree:")
                    print(validator.parse_tree)  # Print the parse tree

                    # Write the parse tree to the file
                    output_file.write("Parse Tree:\n")
                    output_file.write(str(validator.parse_tree) + "\n")
            except SyntaxError as e:
                error_message = f"Error: {e}\n"
                print(f"\033[91m{error_message}\033[0m")
                output_file.write(error_message)  # Write the error message to the file
            cnt += 1  # Increment for the next test case
            output_file.write("==================\n")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\033[91mError: {e}\033[0m")
