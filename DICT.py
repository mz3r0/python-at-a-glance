# A dictionary maps keys to values. They're based on the hash table data structure.
# The key must be of any immutable type and the value can by anything.
# More correctly, keys must be hashable. Immutable is used as a synonym for hashable, or vice versa.
# A rule of thumb: immutable types are hashable and mutable types are not. More details below.

# Immutable types: tuple, frozenset, string, bytes, numeric (int, float, complex).
# Mutable types: list, dictionary, set, user-defined classes
# Exceptions are tuples with mutable types and user-defined classes.
# An immutable tuple is not hashable when it contains a (mutable) list.
# A user-defined class is hashable by default as the hash is based on id().
# Any other scenario pertains to advanced cases with custom classes.
# An object being mutable defeats the purpose of a hash table because it's based on the object's
# hash value and usually, the hash value changes with even the smallest change made on the object.

dict_methods = [method for method in dir(dict) if not method.startswith('_')]
print(sorted(dict_methods))
# ['clear', 'copy', 'fromkeys', 'get', 'items', 'keys', 'pop', 'popitem', 'setdefault', 'update', 'values']


# Basic usage
emptydict = {}                 # Create an empty dictionary
dict1 = dict()                 # Create an empty dictionary 2
dict1 = {'y': 34, 'x': 56}     # Create a non-empty dictionary
dict2 = dict([('y', 34), ('x', 56)])      # Create from a list of tuples
dict3 = dict.fromkeys(['y', 'x'])    # Create from any iterable of keys. All values default to None.
dict3 = dict.fromkeys(['y', 'x'], 30)     # Create from list of keys. All values will be 30.
dict3 = dict(y=34, x=56)       # Initialize using constructor

# Side note: The fromkeys method can be used on the class type (as seen above), but also on instances.

dict1['temperature'] = 32      # Assign value to a key, since key doesn't exist
dict1['temperature'] = 21      # Change value of a key, since key exists now
if 'temperature' in dict1:     # Membership test of a key / key exists
  del dict1['temperature']     # Delete / remove
print(dict1 == dict2)          # True. Their values are equal.
print(dict2 == dict3)          # True. Their values are equal.

print(dict1['y'])              # Access via key
print(dict1.get('y'))          # Access using get method
print(dict1.get('z'))          # Will get the key or return None if not found
print(dict1.get('z',6))        # Choose a default value to return if key isn't found
#print(dict1["z"])             # KeyError.

itemcount = len(dict2)         # 2. Length / size / item count
isempty = len(dict2) == 0      # False. Emptiness test

for key in dict2:              # Iterate on keys
  print(key, dict2[key])       # Print key and its associated value
  dict2[key] += 10             # Update the value for each key by +10

for key in sorted(dict2):      # Sorted returns dict2's keys as a sorted list
  print(key, dict2[key])       # Now the keys are iterated in sorted fashion

for value in dict2.values():   # Iterate on values
  print(value)

for key, value in dict2.items(): # Iterate via pairs
  print(key, value)

dict4 = {'red': 255, 'green': 0, 'blue': 0}
poppedvalue = dict4.pop('green') # Remove key 'green', returning its value, 0
poppedpair = dict4.popitem()     # returns a random pair as a tuple and removes it. Takes no arguments
print (emptydict, dict1, dict2, dict3, dict4, itemcount, isempty, poppedvalue, poppedpair)
dict4.clear()                    # Clear / empty / erase contents


# Dict comprehensions (for filtering) - since Python 2.7 and 3.0
houses = {1: 'Gryffindor', 2: 'Slytherin', 3: 'Hufflepuff', 4: 'Ravenclaw'}
new_houses = {n**2: house + "!" for (n, house) in houses.items()}
print(houses)
print(new_houses)

rgb1 = {'red': 0, 'green': 0, 'blue': 255}
rgb2 = {key: 100 for key in rgb1}  # Set RGB values to 100
rgb3 = {key: min(rgb1[key] + 100, 255) for key in rgb1}  # Set RGB values to 100 more than the ones in rgb1
# without exceeding 255
colors = ['red', 'green', 'blue']
values = [20, 30, 40]
rgb4 = {c:v for c in colors for v in values}   # Don't do this. Wrong result
rgb5 = {colors[i]:values[i] for i in range(len(colors))}  # Don't do this. Too complex
rgb6 = dict(zip(colors, values))               # Do this instead
len(colors) == len(values)                     # Must be true when doing this
print(rgb1, rgb2, rgb3, rgb4, rgb5, rgb6)


# Copying
original = {'onelist':[1,2,3]}
copy1 = original.copy()             # A shallow copy
copy1['onelist'].append(4)          # Modify the shallow copy
print(original)                     # original was modified!
from copy import deepcopy
copy2 = deepcopy(original)          # A deep copy
copy2['onelist'].append(5)          # Modify the deep copy
print(original)                     # original stayed the same
# For more details check out copying part in lists at a glance.
# Use deepcopy when the values are mutable objects and when you want completely separate copies.


# Update a dictionary. Overwrite existing keys.
temperatures = dict()
temperatures.update({'17':13, '18':12})      # Update from dictionary
temperatures.update([('19',11), ('20',11)])  # Update from list of key/value pairs
print(temperatures)


# Using setdefault method.
# If key exists, return its value, otherwise insert key with a chosen default value and return the value.
person = {'name':'Andy', 'occupation':'programming'}
occupation = person.setdefault('occupation','art')  # Occupation exists. Will equal 'programming'
nickname = person.setdefault('nickname','mz3r0')    # Nickname doesn't exist. Adds it. Will equal 'mz3r0'
print(occupation, nickname)
print(person)


# Merging dictionaries
d1 = {'Diamond':'hardest', 'Ruby':'hard'};
d2 = {'Talk':'soft', 'Diamond':'HARDEST'}

    # Method 1 - Iterate on key/value pairs
merged1 = d1.copy()
for key, value in d2.items():
    merged1[key] = value

    # Method 2 - update()
merged2 = d1.copy()
merged2.update(d2)                 # Uses O(1) space!

# Side note: Don't do this, merged will become None. Update works in place. Assignment is redundant!
# merged = dict_to_merge.update(other_dict)

    # Method 3 - Unpacking (since Python 3.5 * )
merged3 = {**d1, **d2}
# {**dict1, **dict2, **dict3}      # Can do this too!

# * Didn't verify source.

    # Method 4 - Pipe operator (Since Python 3.9)
merged4 = d1 | d2
# In place merging can also be done using the update operator (|=)

    # Method 5 - Using the constructor, with a caveat
merged5 = dict(d1, **d2)
# This method only works if the keys of the second dictionary are strings since it's based on dict(mapping, **kwargs).
# When d2 is unpacked, the keys must follow the same rules as when naming variables / parameters.
# Try and see, the following will produce a TypeError: keywords must be strings.
# dict({1:'a'}, **{1:'v'})

    # Method 6 - Using ChainMap
from collections import ChainMap
chain6 = ChainMap(d1, d2)    # chain6 can be used as a dictionary. The difference is with duplicate keys.
chain6['Diamond']            # hardest. When the same key exists in two or more dictionaries, it prefers the value of the first.
# c = ChainMap({1:2}, {1:3}, {1:4}); print(c[1]) # Will print 2

print(merged1 == merged2 == merged3 == merged4 == merged5)
print(merged1)
print(chain6)
# Conclusion. Use update and pipe depending on version. ChainMap has its own uses.



# Sources: Wikibooks
