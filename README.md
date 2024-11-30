# Mini Compiler for Scripting Language

## Project Overview
This project implements a mini compiler for a custom scripting language, focusing on lexical analysis, syntax analysis, and basic semantic analysis. The compiler processes source code written in a case-insensitive scripting language that supports various programming constructs including variable declarations, control structures, functions, and list operations.

## Language Features

### Core Characteristics
- Case-insensitive syntax
- Reserved keywords
- Optional parentheses for parameter-less function calls
- Flexible comment system using braces {}

### Supported Operations
- **Arithmetic Operators**: +, -, *, /
- **Relational Operators**: =, >, <, !=
- **Logical Operators**: AND, OR, NOT
- **Compound Assignment**: +=, -=, *=, /=
- **Increment/Decrement**: ++, --

### Programming Constructs
- Variable declaration and assignment using LET
- Conditional statements (IF-THEN-ELSE)
- Multiple loop structures:
  - WHILE loops
  - FOR loops with STEP
  - DO-WHILE loops
  - Range-based FOR loops
  - REPEAT-UNTIL loops
- Function definitions and calls
- List operations and indexing
