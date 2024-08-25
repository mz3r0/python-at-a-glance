# Added in Python 3, bytes objects hold arrays of bytes. Each byte can take a value in the range [0,255]
# Objects of the bytes class are immutable. There is also a mutable version of bytes called bytearray.
# Bytes is useful for encoding and decoding strings. Bytes objects can be used as lists.

message = bytes("Γειά σου κόσμε!","utf-8")   # Encode UTF-8
print(message)
decoded = message.decode()                   # Decode

# Bytes methods - They're a lot
bytes_methods = {method for method in dir(bytes) if not method.startswith('_')}
print(sorted(list(bytes_methods)),end='\n\n') # Ran in 3.12

# From 3.6 to 3.12 three methods were added: {'removeprefix', 'removesuffix', 'isascii'}
# Not surprisingly, str and bytes have many methods with the same name!

str_methods = {method for method in dir(str) if not method.startswith('_')}
methods_in_common = bytes_methods & str_methods
print(sorted(list(methods_in_common)),end='\n\n') # Brace yourself

# ['capitalize', 'center', 'count', 'endswith', 'expandtabs', 'find', 'index', 'isalnum', 'isalpha',
# 'isascii', 'isdigit', 'islower', 'isspace', 'istitle', 'isupper', 'join', 'ljust', 'lower', 'lstrip',
# 'maketrans', 'partition', 'removeprefix', 'removesuffix', 'replace', 'rfind', 'rindex', 'rjust',
# 'rpartition', 'rsplit', 'rstrip', 'split', 'splitlines', 'startswith', 'strip', 'swapcase', 'title',
# 'translate', 'upper', 'zfill']

bytes_unique = bytes_methods - methods_in_common
str_unique = str_methods - methods_in_common
print(sorted(list(bytes_unique)),end='\n\n')
# ['decode', 'fromhex', 'hex']
print(sorted(list(str_unique)),end='\n\n')
# ['casefold', 'encode', 'format', 'format_map', 'isdecimal', 'isidentifier', 'isnumeric', 'isprintable']


# Basic usage
binary_data = b'''This is a
multi-line
string!''' # Can be created from an iterable of ints, a string, bytes or buffer objects.

zeroes = bytes(5)               # b'\x00\x00\x00\x00\x00'
bytes1 = bytes([97, 98, 99])    # b'abc'
bytes2 = b'abc'                 # b'abc'
# bytes('abc')                          # TypeError: string argument without an encoding 
# bytes([300])                          # ValueError: bytes must be in range(0, 256)
bytes3 = bytes('abc', 'ascii')
bytes4 = bytes('abc', 'utf-8')
bytes3 == bytes4                        # True
bytes5 = bytes('abc', 'utf-16')         # b'\xff\xfea\x00b\x00c\x00'
bytes6 = 'abc'.encode('utf-16-le')      # b'a\x00b\x00c\x00'

# The 'utf-16' encoding specifies a generic utf-16 encoding, which includes a byte order marker of
# two bytes (0xff, 0xfe). The 'utf-16-le' encoding omits the byte order marker.

bytes7 = bytes(range(20))
morezeroes = zeroes + zeroes + zeroes
bytes7 = bytes5 + bytes6

print(zeroes, bytes1, bytes2, bytes3, bytes4, bytes5, bytes6)
