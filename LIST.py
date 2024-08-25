# Lists can be thought of as mutable versions of tuples.
# If a tuple can do it, so can a list.

list_methods = {method for method in dir(list) if not method.startswith('_')}
tuple_methods = {method for method in dir(tuple) if not method.startswith('_')}
list_methods -= tuple_methods     # Remove tuple methods
print(sorted(list(list_methods))) # ['append', 'clear', 'copy', 'extend', 'insert', 'pop', 'remove', 'reverse', 'sort']


# Basic usage
list1 = []                      # A new empty list
list2 = [1, 2, 3, "cat"]        # A new non-empty list with mixed item types
list2.append("cat")             # Add a single member, at the end of the list
list2.reverse()                 # Reverse the item order in-place
list2.count("cat")              # 2. Count how many times "cat" shows up in list1

list1.extend(["dog", "mouse"])  # Add several members
list1.insert(0, "fly")          # Insert at the beginning, or at index 0, or any other index.
list1[0:0] = ["cow", "doe"]     # Add members at the beginning
doe = list1.pop(1)              # Remove item at index. Or, use pop() to remove from the end.
if "cat" in list1:              # Membership test
    list1.remove("cat")           # Remove / delete
#list1.remove("elephant") - throws an error

for item in list1:              # Iteration AKA for each item
    print(item)

print("Item count:", len(list1))# Length / size / item count

list3 = [6, 7, 8, 9]
for i in range(0, len(list3)):  # Read-write iteration
    list3[i] += 1                 # Item access AKA element access by index

last = list3[-1]                # Last item (same for strings)
next_to_last = list3[-2]        # Next-to-last item (same for strings)

list4 = list1[:]                # A shallow list copy
print(list1 == list4)           # True: same by value
print(list1 is list4)           # False: not same by reference
list5 = list1[:]

list6 = [1, 2] + [2, 3, 4]      # Concatenation
list6 += [5, 6]                 # Concatenation
del list6[:]                    # Clear / empty / erase contents
list6.clear()                   # Clear / empty / erase contents
print(list6)
del list6                       # Delete the variable list6 itself

print(list3[1:3], list3[1:], list3[:2]) # Slices
print(max(list3), min(list3), sum(list3)) # Aggregates

print([1,2] < [2,100])          # True. List comparison uses lexicographical order
print([2,2] < [2,1])            # False
print(["a","b"] < ["b","a"])    # True


# List comprehensions (for filtering) - since version 2.0
print([x for x in range(10)])
print([x for x in range(10) if x % 2 == 1])
print([x for x in range(10) if x % 2 == 1 if x < 5])
print([x + 1 for x in range(10) if x % 2 == 1])
print([x + y for x in '123' for y in 'abc'])

# Mind the order of nested loops

some_nums = [1,2,3]
newlist1 = [n for n in some_nums for _ in range(3)]
print(newlist1)     # [1, 1, 1, 2, 2, 2, 3, 3, 3]

newlist2 = [n for _ in range(3) for n in some_nums]
print(newlist2)     # [1, 2, 3, 1, 2, 3, 1, 2, 3]


# Fancy slicing
data = list(range(10))
data[::2] = list(range(100))[24:37:3]
print(data)         # [24, 1, 27, 3, 30, 5, 33, 7, 36, 9]


# Conversion to & from set
set1 = set(["cat", "dog"])      # Initialize set from a list
from_set = list(set1)           # Get a list from a set


# Sorting lists
list1 = [2, 3, 1, 'a', 'B']     # re-using variable names list1..list4
# list1.sort()                  # TypeError: '<' not supported between instances of 'str' and 'int'
list1 = [2, 3, 1]
list1.sort()                    # list1 gets modified
list1 = ['a', 'B']
list1.sort()                    # The sort is case sensitive
list2 = sorted(list1)           # list1 is unmodified; since Python 2.4

# Side note: When sorting in place, the sort() method returns None to emphasize this side effect.

list3 = sorted(list1, key=lambda x: x.lower()) # case insensitive ; will give error as not all elements of list are strings and .lower() is not applicable
list4 = sorted(list1, reverse=True) # Reverse / descending order
print(list1, list2, list3, list4)

# Students example
students = [('Bob', 'B', 12), ('Pete', 'B', 10), ('Tom', 'A', 15)]

# Sorting by Grade (ascending)
print(sorted(students, key=lambda student: student[1])) # Grade at index 1
# Sorting first by Grade (ascending) and second by Age (descending)
print(sorted(students, key=lambda x: (x[1], -x[2]))) # Grade at ubdex 1, Age at index 2

# Unchanged values -> ascending sort
# Inverting values -> descending sort


# Copying
fruit = ['apple', 'cherry', 'banana']
students = [{'name':'Yu'}, {'name':'Mi'}, {'name':'Lee'}]

fruit2 = fruit          # (Shallow) Copy by assignment
fruit3 = fruit[:]       # (Shallow) Copy by slicing
fruit4 = list(fruit)    # (Shallow) Copy using type constructor

fruit == fruit2 == fruit3 == fruit4     # True. They all have euqal value.
fruit is fruit2                         # True. fruit and fruit2 are the same object.
id(fruit) == id(fruit2)                 # True. This check is done by is operator.

fruit is fruit3                         # False. fruit and fruit3 are different objects.
fruit is fruit4                         # False. fruit and fruit3 are different objects.

# Side note: Slicing and constructor return new objects.

students2 = students          # Shallow Copy. Same object.
students3 = students[:]       # Shallow Copy. Different object, sort of.
students4 = list(students)    # Shallow Copy. Different object, sort of.

students[2]['name'] = 'Leeeeee'   # Change the original.
print(students2[2])               # {'name': 'Leeeeee'}. As expected.
print(students3[2])               # {'name': 'Leeeeee'}. Uh oh!
print(students4[2])               # {'name': 'Leeeeee'}. Uh oh!

# students might be a different object than students3 (or 4) but they both have
# references to the same 3 students, Yu, Mi, Lee. Check it yourself:

id(students[2]) == id(students2[2]) == id(students3[2]) == id(students4[2]) # True

# A change in either list will reflect in all other list variables created
# by shallow copying. This is why it's called "shallow copying".

fruit[2] = "banananana"
print(fruit2[2])                  # banananana. As expected (same object)
print(fruit3[2])                  # banana. Also as expected.
print(fruit4[2])                  # banana. Also as expected.

# As we saw earlier, mutable objects inside a list aren't re-created from scratch.
# The fruit list behaves as expected because the strings inside of it are immutable.
# That is, new strings are created in fruit3 and fruit4. Check it yourself:

id(fruit[2]) == id(fruit2[2]) == id(fruit3[2]) == id(fruit4[2]) # False

# Solution: copy.deepcopy() - Completely copy objects
from copy import deepcopy
students5 = deepcopy(students)
students[2]['name'] = "Lee"       # Change students back
print(students5[2])               # {'name': 'Leeeeee'}. No reflected change. Awesome!

# Use deepcopy when using collection objects like list, dict, set, etc. which contain
# mutable objects. If these only contain immutable objects, avoid deepcopy and save
# some memory. For example, python saves space by creating a single 'apple' string
# which is referenced from all fruit lists. Check it yourself:

id(fruit[0]) == id(fruit2[0]) == id(fruit3[0]) == id(fruit4[0]) # True

# Again, shallow copying is enough because updating a fruit string always creates
# a new string while updading a student dictionary doesn't.


# Initializing lists
zeros = [0]*5

# When building a new list by multiplying, Python copies each item by reference.
# This poses a problem for mutable items, for instance in a multidimensional array
# where each element is itself a list. You'd guess that the easy way to generate
# a two dimensional array would be:

listoflists=[ [0] * 3 ] * 4         # Which works, but in an unexpected way.
print(listoflists)                  # [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
listoflists[0][2] = 1               # Oh no.
print(listoflists)                  # [[0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1]]

listoflists=[[0]*4 for i in range(5)]  # The better approach


# Unpacking lists
places_to_see = ['Fiji', 'Seychelles', 'Maldives', 'Philippines']
fav1, fav2, *other = places_to_see     # Useful when unpacking more values than our variables can hold.
print(fav1, fav2, other)               # The 'other' variable 'eats up' the remaining list items.

l1 = [10, 90]; l2 = [90, 10]
def add_em(a, b, c, d):
    return a + b + c + d


print(add_em(*l1, *l2))


# Clearing list inside a function

def workingClear(ilist):
    del ilist[:]


def brokenClear(ilist):
    ilist = [] # Lets ilist point to a new list, losing the reference to the argument list


list1=[1, 2]; workingClear(list1); print(list1)
list1=[1, 2]; brokenClear(list1); print(list1)
# Using clear() method is more clear. Prefer deleting slices when the slice isn't the whole list!


# Sources include: Wikibooks, Docs, Other.
