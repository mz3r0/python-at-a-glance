# This script is meant to be executed in at least version 3.8 because it uses self-documenting expressions, released in Python 3.8.
# Output shows the code and what it evalues to in the '<expression> = <result>' format.
# I recommend reading both source and output.

list_of_values = [] # Empty list
lv = list_of_values

# lv.append()
# print(list_of_values)

# TO BOOL
print('\tTO BOOL\n')

_ = '''Bool is a subclass of int. We use the built-in bool() function to evaluate objects as either True or False.\
It works like this: False is returned if:\n\t1) The object is empty, such as [], (), {}, "" or \n\t2) The object is 'False' or 'None' or \n\t\
3) The object is a zero of any numeric type such as 0, 0L (until Python 2.x), 0.0 and 0j or \n\t4) The object defines a __bool__() or __len__()\
method that returns zero.\nIn any other case True is returned. In a few words, bool() always returns True unless the object is empty, of zero\
lentgh, falsey or None. Important note: __bool__() in Python 3.x used to be named __nonzero__() in Python 2.x\n'''
print(_)

lv.append(f'{bool() = }') # False. No parameter
lv.append(f'{bool([]) = }') # False. Empty list
lv.append(f'{bool(()) = }') # False. Empty tuple
lv.append(f'{bool({}) = }') # False. Empty dict
lv.append(f'{bool(set()) = }') # False. Empty set
lv.append(f'{bool("") = }') # False. Empty string
lv.append(f"{bool('''''') = }") # False. Empty docstring
lv.append(f'{bool(False) = }') # False!
lv.append(f'{bool(None) = }') # False!
lv.append(f'{bool(0) = }') # False. Zero integer value
lv.append('bool(0L) = False [*]') # Until Python 2. Deprecated in Python 3.x
lv.append(f'{bool(0.0) = }') # False. Zero float value
lv.append(f'{bool(0j) = }') # False. Zero complex value

lv.append(f'{bool(3) = }') # True. Non-zero number
lv.append(f'{bool(" ") = }') # True. Non-empty string with one space
lv.append(f'{bool(len) = }') # True. Function object
lv.append(f'{bool([False]) = }') # True. Non-empty list with one item
lv.append(f'{bool({'bedtime drink':'warm milk'}) = }') # True. Dictionary isn't empty.

lv.append('\n[*] Until Python 2. Deprecated in Python 3.x\n')

for item in lv:
    print(item)
lv = []

# TO INT
print('\tTO INT\n')

_ = '''Explicit casting to int is done using int(). Its argument must be a string, a bytes-like object or a real number. \
Implicit casting examples will be also included. The string cannot contain non-numeric characters aside from: +, -, _ and \
whitespace around it. Since 3.6: Grouping digits with underscores as in code literals is allowed. The byteorder argument \
in the Python documentation for the int.to_bytes() and int.from_bytes() methods became optional in Python 3.11.\n'''
print(_)

# Change in 3.11: String inputs and string representations can be limited to prevent dos attacks.
# Details here https://docs.python.org/3/library/stdtypes.html#int-max-str-digits

lv.append('From various literals')
lv.append(f'{int() = }') # 0
lv.append(f'{int(-14.14) = }') # -14
lv.append(f'{int(1234) = }') # 1234. It's already an int
lv.append(f'{int( +1_2_3_4 ) = }') # 1234. Underscores, whitespace & plus sign allowed.
lv.append(f'{int(  -1234) = }') # -1234. Negative sign allowed.
lv.append(f'{int(0b1011) = }') # 11. Binary literal.
lv.append(f'{int(0o13) = }') # 11. Octal literal.
lv.append(f'{int(0xB) = }') # 11. Hexadecimal literal.

lv.append('\nFrom various strings')
lv.append(f'{int('1234') = }') # 1234. From string. Assumes base 10.
lv.append(f'{int(' +1_2_3_4 ') = }') # 1234
lv.append(f'{int('  -1234') = }') # -1234
lv.append(f'{int('1234',base=5) = }') # 194. From string. Evaluate in base 5.
lv.append(f'{int('1011',base=2) = }') # 11. From string. Evaluate in base 2.
lv.append(f'{int('0b1011',base=2) = }') # 11. From binary string.
lv.append(f'{int('0o13',base=8) = }') # 11. From octal string.
lv.append(f'{int('0xB',base=16) = }') # 11. From hexadecimal string.

lv.append('\nFrom string literals using base 0')
lv.append(f'{int('0b1010', 0) = }') # 10
lv.append(f'{int('0o12', 0) = }') # 10
lv.append(f'{int('0x1A', 0) = }') # 26
lv.append(f'{int('-0b000010', 0) = }') # -2
lv.append(f'{int('+0b10', 0) = }') # 2
lv.append(f'{int('-0b010', 0) = }') # -2
lv.append(f'{int('-0x010', 0) = }') # -16

lv.append('\nFrom various byte-like objects')
lv.append(f'     {int.from_bytes(b'\x01\xFF') = }' + ' [*]') # 511. Argument byteorder is big by default since 3.11
lv.append("Raw: int.from_bytes(b'\\x01\\xFF') = 511")
lv.append(f'     {int.from_bytes(b'\x01\xFF',byteorder='big') = }') # 511
lv.append("Raw: int.from_bytes(b'\\x01\\xFF',byteorder='big') = 511")
lv.append(f'     {int.from_bytes(b'\xFF\x01',byteorder='little') = }') # 511
lv.append("Raw: int.from_bytes(b'\\xFF\\x01',byteorder='little') = 511")
lv.append(f'     {int.from_bytes(b'\xAA\xFF',signed=True) = }') # -21761
lv.append("Raw: int.from_bytes(b'\\xAA\\xFF',signed=True) = -21761")
lv.append(f'     {int.from_bytes(b'\xAA\xFF') = }') # 43775
lv.append("Raw: int.from_bytes(b'\\xAA\\xFF') = 43775")

lv.append('\nImplicit conversion to int')
lv.append(f'{4 + True = }') # 5. Because bool is implicitly converted to int
lv.append(f'{int(True) = }') # 1
lv.append(f'{int(False) = }') # 0

lv.append('\nThe following will NOT work')
lv.append("int('010', 0)") # ValueError. Invalid literal. Needs either prefix of: 0b, 0o, 0x.
lv.append('int(3j)') # TypeError
lv.append("int(b'\xFF\x00')") # ValueError. Doesn't work with base 0 either.
lv.append('int(- 1234)') # -1234. ValueError. Invalid literal.
lv.append('int(0x1A, 0)') # TypeError. Can't convert non-string. Doesn't even make sense.
lv.append('"4" + 1') # TypeError. Python expects a string to concatenate but int is given. Use str() or int() accordingly.
lv.append('0001 [**]') # SyntaxError. Since Python 3, leading zeros in decimal integer literals are not permitted.

lv.append('\n[*]\tArgument byteorder is big by default since 3.11')
lv.append('[**]\tSince Python 3, leading zeros in decimal integer literals are not permitted. See PEP 3127\n')

for item in lv:
    print(item)
lv = []

# TO FLOAT
print('\tTO FLOAT\n')

_ = '''Casting to float is done using float().\n'''
print(_)

lv.append('From various literals')
lv.append(f'{float() = }') # 0.0
lv.append(f'{float(14.14) = }') # 14.14. It's already a float
lv.append(f'{float(1234) = }') # 1234.0
lv.append(f'{float(0b1011) = }') # 11.0 Binary literal.
lv.append(f'{float(0o13) = }') # 11.0 Octal literal.
lv.append(f'{float(0xB) = }') # 11.0 Hexadecimal literal.

lv.append('\nFrom various strings')
lv.append(f'{float("infinity") = }') # inf.
lv.append(f'{float("inFINIty") = }') # inf. Case insensitive
lv.append(f'{float("inf") = }') # inf
lv.append(f'{float("-inf") = }') # -inf
lv.append(f'{float("nan") = }') # nan. It is of type float
lv.append(f'{float("-.23") = }') # -0.23
lv.append(f'{float("   -12345") = }') # -12345.0
lv.append(f'{float("1e-003") = }') # 0.001
lv.append(f'{float("2.7E-2") = }') # 0.027. Both e and E can be used.

lv.append('\nImplicit conversion to float')
lv.append(f'{5 + 4.5 = }') # 9.5. Adding an integer and a float causes an int to float implicit cast.
lv.append(f'{4.0 + True = }') # 5.0
lv.append(f'{float(True) = }') # 1.0
lv.append(f'{float(False) = }') # 0.0

lv.append('\nThe following will NOT work')
lv.append('float(3j)') # TypeError

for item in lv:
    print(item)
lv.clear()

# TO COMPLEX

# TO LIST OR TUPLE

# TO SET OR FROZENSET

# TO STR

# TO BYTEARRAY OR BYTES

# TO DICT


# NEXT DOCUMENT:
# TO *common data types from built-in modules*
