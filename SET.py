# sets are: unordered, mutable, heterogeneous. Set items must be hashable and therefore immutable most of the time.

set_methods = [method for method in dir(set) if not method.startswith('_')]
print(sorted(set_methods))
# ['add', 'clear', 'copy', 'difference', 'difference_update', 'discard', 'intersection', 'intersection_update',
# 'isdisjoint', 'issubset', 'issuperset', 'pop', 'remove', 'symmetric_difference', 'symmetric_difference_update',
# 'union', 'update']


# Basic usage
set1 = set()                       # A new empty set
set1.add("cat")                    # Add a single member. Similar to list.append() except sets are unordered.
set1.update(["dog", "mouse"])      # Add several members from iterable. Works in place. Similar to list.extend()
if "mouse" in set1:                # Membership test
    set1.remove("mouse")

#set1.remove("elephant")           # KeyError. There is no "elephant"
set1.discard("elephant")           # Doesn't care if it doesn't exist.
print(set1)                        # Note: set.discard() always returns None

for item in set1:                  # Iteration AKA for each item
    print(item)

print("Item count:", len(set1))    # Length / size / item count

#1stitem = set1[0]                 # TypeError: Sets aren't subscribable. No indexing.

set1 = {"cat", "dog"}              # Initialize set using braces; since Python 2.7
#set1 = {}                         # No way; this is a dict. Use set() for empty set.
set1 = set(["cat", "dog"])         # Initialize set from a list (or any iterable)
set2 = set(("dog", "mouse"))       # Initialize set from a tuple

intersection = set1 & set2                 # {'dog'}
intersection = set1.intersection(set2)     # Equivalent alternative using method
union = set1 | set2                        # {'dog', 'cat', 'mouse'}
union = set1.union(set2)                   # Returns a new object.
difference1 = set1 - set2                  # {'cat'}
difference1 = set1.difference(set2)
difference2 = set2 - set1                  # {'mouse'}. Difference is not an associative operation
difference2 = set2.difference(set1)
symmetric_diff = set1 ^ set2               # {'cat', 'mouse'} (union minus intersection)
symmetric_diff = set1.symmetric_difference(set2)
issubset = set1 <= set2                    # Is set1 a subset of set2? False
issubset = set1.issubset(set2)
issuperset = set1 >= set2                  # Is set1 a superset of set2? False
issuperset = set1.issuperset(set2)

# Methods without corresponding operators
isdisjoint = set1.isdisjoint(set2) # Disjoint test. False

# Operators without corresponding methods
ispropersubset = set1 < set2               # Is set1 a subset of set2? False
ispropersuperset = set1 > set2             # Is set1 a superset of set2? False

# Our two sets: {'dog', 'cat'} {'dog', 'mouse'}
# Nothing stops us from doing this with 3 or more sets. Example uses 2 for sake of simplicity.
print(set1, set2)

# Results
print(intersection, union, difference1, difference2, symmetric_diff)
print(issubset, issuperset, isdisjoint, ispropersubset, ispropersuperset) # All False

# True and 1 are considered the same value. Same for False and 0.
# Note that the first value read from left to right is retained.
print({True, 1, False, 0})         # {False, True}
print({1, True, False, 0})         # {False, 1}
print({True, 1, 0, False})         # {0, True}
print({1, True, 0, False})         # {0, 1}

# In Python, a tuple is immutable, but it is hashable only if all its elements are hashable
# It's the only built-in type that can be immutable and unhashable

# data = {[1,2,3],['r','g','b']}   # TypeError: unhashable type: 'list'
data = {(1,2,3),('r','g','b')}     # Use tuples instead

# Instances of user-defined classes are mutable but hashable by default (their hash is their id())
# for more details on this: https://docs.python.org/3/glossary.html#term-hashable
# and asmeurer's answer: https://stackoverflow.com/questions/11324271/what-is-the-default-hash-in-python

set1 |= set(["dog", "horse"])      # Update with several members. Similar to set.update() seen previously.
print(set1)                        # You can also do: &=. -=. ^=, or respectively:
                                   # intersection_update(), difference_update(), symmetric_difference_update()

# From the docs: Note, the non-operator versions of union(), intersection(), difference(), symmetric_difference(),
# issubset(), and issuperset() methods will accept any iterable as an argument. In contrast, their operator based
# counterparts require their arguments to be sets. This precludes error-prone constructions like
# set('abc') & 'cbs' in favor of the more readable set('abc').intersection('cbs').
print(set(['cat','parrot']).intersection(['cat','dog']))

set7 = set1.copy()                 # A shallow copy
set7.clear()                       # Clear / empty / erase contents
print(set("world").pop())          # Remove an arbitrary / a random element

set8 = {x for x in range(10) if x % 2} # Set comprehension; since Python 2.7
print(set8)

# Additional examples using type constructor
print(set("abc"))                  # {'c', 'b', 'a'}
print(set(b"abc"))                 # {97, 98, 99}
print(set({'name':'Andrei', 'nick':'mz3r0'})) # {'name', 'nick'}. Dict -> set out of list of keys

# Copying works similar to list.copy()
# See lists at a glance to get the idea.



# Sources include Wikibooks, StackOverflow.
