test_cases_phase2 = [
    # Test Case 1: Simple Variable Declarations and Operations with control flow and loops
    """
    LET a = 5
    LET b = 10
    IF a < b THEN
        LET c = a + b
        LET d = c * 2
    ELSE
        LET e = a - b
    ENDIF

    LET counter = 1
    WHILE counter <= 5 DO
        LET square = counter * counter
        counter = counter + 1
    ENDWHILE

    FOR i = 0 TO 10 STEP 2 DO
        LET squared = i * i
    ENDFOR

    LET result = 0
    REPEAT
        LET result = result + 1
    UNTIL result >= 5

    LET value = 10
    DO
        LET value = value - 2
    WHILE value > 0

    LET sum = 20
    sum += 5

    LET factor = 3
    factor *= 2
    """
]
