This is a software library that accepts 2 version string as input and 
returns whether one is greater than, equal, or less than the other. 
As an example: "1.2" is greater than "1.1". 

REQUIREMENTS: PYTHON 3. and above

usage:

    from compare_string_version import compareVersion
    print(compareVersion(a,b))
    
expected return

when

    a==b:

        a is equal to b

    a>b:

        a is greater than b

    a<b: 

        a is less than b

Exceptions:

either a is null and/or b is null:
    Value(s) can not be null: Both values must be string    
either a and/or b are/is not a string:
    Both must be string

assumptions:

    a and b are string
    
    a and b are not null (None)
    
    both version strings only contain numbers (0...9) and this char '.':

        123.456.789.012

        'A..Z','a..z' and any other chars like "! @ # $ % * [ } ] { ^ ç ? ; : . > , < | " will be removed from the comparison:
            some adjustment would be applied after char removal:
            '..' will be replaced by '.'
            string ending in '.' will be shorted by 1

    this '..' will not be accepted as it is '.' duplicated:
            '10..12..13..14' will become '10.12.13.14'

    the comparison would be from the group split by the char '.':
            10.12.13.14 would be treated as 10 12 13 14
            01.10.100.001 would be treated as 1 10 100 1

    all the comparison would check the integer part of the version:
            '10.0' is equal to '010.0.0.0.0.0.0.0' because int('10.0') is equal to int ('010')

    whoever version number has the higher far left group would be named as greater:
            10.0.0.0.0.1 is greater then 9.9.9.9.9.9.9
            0.1.0.0.0.0.1 is greater than 0.0.9
            the same "int" rule will be applied for any other group in the string

    all '0's from the left will be disregarded if its value is '0':
            1.0.0.0 is equal to 1.0 and it is equal to 1
            
            
the following .py were used in order to test data

test997.py has generated output5.txt

test996.py has generated output4.txt

test995.py has generated output1.txt and output2.txt

test994.py has generated output3.txt