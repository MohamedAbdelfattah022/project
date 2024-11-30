test_cases = [
"""
LET x = 10
LET y = 20
LET sum = x + y
LET product = x * y
LET difference = y - x
LET quotient = y / x
""",

"""
LET age = 18
IF age >= 18 THEN
    LET status = "adult"
ELSE
    LET status = "minor"
ENDIF

LET score = 85
IF score >= 90 THEN
    LET grade = "A"
ELSE
    IF score >= 80 THEN
        LET grade = "B"
    ELSE
        LET grade = "C"
    ENDIF
ENDIF
""",

"""
{ While loop example }
LET counter = 1
WHILE counter <= 5 DO
    LET result = counter * 2
    counter++
ENDWHILE
""",
"""
{ For loop with STEP }
FOR i = 0 TO 10 STEP 2 DO
    LET squared = i * i
ENDFOR
""",

"""
{ Range-based for loop }
FOR x IN Range(1, 5, 1) DO
    LET cube = x * x * x
ENDFOR
""",

"""
{ Repeat-Until loop }
LET num = 1
REPEAT
    LET num = num * 2
UNTIL num > 100
""",

"""
{ Do-While loop }
LET value = 1
DO
    LET value = value + 2
WHILE value < 10
""",

"""
FUNC calculateArea(length, width) BEGIN
    LET area = length * width
    RETURN area
END
""",

"""
FUNC factorial(n) BEGIN
    IF n <= 1 THEN
        RETURN 1
    ELSE
        RETURN n * CALL factorial(n - 1)
    ENDIF
END
""",

"""
{ Function calls }
LET rectArea = CALL calculateArea(5, 3)
LET fact5 = CALL factorial(5)
""",

"""
{ Function call without parentheses when no args }
FUNC printMessage() BEGIN
    LET msg = "Hello"
    RETURN msg
END
CALL printMessage
""",

"""
LET numbers = [1, 2, 3, 4, 5]
LET firstNum = numbers[0]
LET lastNum = numbers[4]

LET matrix = [[1, 2], [3, 4]]
LET element = matrix[1][0]  { Should be 3 }

LET fruits = ["apple", "banana", "orange"]
LET fruit = fruits[1]
""",

"""
LET sum = 10
sum += 5        { sum is now 15 }

LET value = 20
value -= 8      { value is now 12 }

LET factor = 3
factor *= 4     { factor is now 12 }

LET quotient = 100
quotient /= 2   { quotient is now 50 }
""",

"""
LET counter = 1
counter++       { counter is now 2 }

LET index = 5
index--        { index is now 4 }

{ In loop context }
FOR i = 0 TO 5 DO
    LET j = i
    j++
ENDFOR
""",


'''
LET my@variable = 5
LET $price = 100
''',

'''
LET y *** 3
'''
,
'''Let x = 5
If x > 10 THen
    CALL printValue
ENDif
'''

,
'''
CALL myFunction(,)
CALL (x, y)
CALL
'''
,
'''
LET list = [1,,2]
'''
,
'''
LET array = [1, 2,]
'''
,
'''
LET empty = [],,
'''
,
'''
LET x = ++ 5
''',
'''
LET y = -- 10
''',

'''
LET z = 15++--
'''
,

'''
FOR i IN Range(1,,10) DO
    CALL print
ENDFOR
'''
,
'''
LET y =+ 10
''',

'''
LET y += 10
'''
,
'''
LET 1variable = 10
LET 123name = "John"
''',

'''
LET x = 10
{ This is an unclosed comment
LET y = 20
'''
]





