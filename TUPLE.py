# tuples are ordered, immutable, and heterogeneous. Duplicates aren't allowed in a set. They may contain duplicates.

tuple_methods = [method for method in dir(tuple) if not method.startswith('_')]
print(sorted(tuple_methods))
# ['count', 'index']


tup1  = (1, 'a')
tup2  = 1, 'a'                # Brackets not needed
tup3  = (1,)                  # Singleton
tup4  = 1,                    # Singleton without brackets

# Side note: A 1-tuple and a 2-tuple are commonly called a "singleton"
# and an "ordered pair", respectively.
# https://en.wikipedia.org/wiki/Tuple

tup5 = ()                     # Empty tuple
list1 = [1, 'a']
it1, it2 = tup1               # Assign items by "value unpacking"
print(tup1 == tup2)           # True
print(tup1 is tup2)           # False *
print(tup1 == list1)          # False
print(tup1 == tuple(list1))   # True
print(list(tup1) == list1)    # True
print(tup1[0])                # First member
for item in tup1: print(item) # Iteration
print((1, 2) + (3, 4))        # (1, 2, 3, 4)
print(tup1 * 2)               # (1, 'a', 1, 'a')

# * False when running interactively in both 3.6 & 3.12. True when ran as a script in 3.12
# Reason: Unknown (TODO)

tup1 += (3,)                  # Tuple and string concatenation work similarly     
print(tup1)                   # (1, 'a', 3), despite immutability **

# ** From docs: "For immutable targets such as strings, numbers, and tuples,
# the updated value is computed, but not assigned back to the input variable."

print(len(tup1))              # Length / size / item count
print(3 in tup1)              # Membership - True

tup6 = ([1,2],)
tup6[0][0]=3
print(tup6)                   # The list within a tuple is mutable

set1 = set( (1,2) )           # Can be placed into a set
#set1 = set( ([1,2], 2) )     # Error: The list within makes it unhashable

def foo():
    return 6, 9               # Return multiple values, as a tuple
r1, r2 = foo()                # Receive multiple values
print(f'r1 is {r1}, r2 is {r2}')

print(max((100, 101, 20, 40)))    # 101
print(min(('a', 'C', 'b', 'Z')))  # C
print(sum((1, 2, 3)))             # 6

# Tuples can be sorted like lists.
# See lists at a glance to get the idea.

# Tuples can be unpacked like lists
# See lists at a glance for examples



# Adapted from and published changes back to Wikibooks.
