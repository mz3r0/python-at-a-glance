# The NoneType class is a singleton; it has only one instance. That instance has a value of None.
# Creating other NoneType variables isn't possible as NoneType is a singleton class.

# Important points
# 1) `None` is not a default value for the variable that has not yet been assigned a value.
# You can declare variables without initializing them by adding type hints since Python 3.5 (PEP 484)
# 2) `None` is not the same as `False`.
# 3) `None` is not an empty string.
# 4) `None` is not 0.

val = None
print(val)
print (type(val))

# Functions that don't return a value explicitly will return None.

# None can be used when a variable needs to be initialized to a default value representing
# the absence of any meaningful data, if desired.
