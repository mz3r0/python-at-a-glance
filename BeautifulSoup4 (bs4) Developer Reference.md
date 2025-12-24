## Installation & Parsers

**Install**: `pip install beautifulsoup4` (Win) or `apt-get install python3-bs4` (Linux)

**Available parsers**: `html.parser` (default, batteries included), `lxml` (fast, XML support), `html5lib` (lenient, browser-like, slow)

> From the docs (as bonus): Desirable features of the parser to be used. This may be the name of a specific parser ("lxml", "lxml-xml", "html.parser", or "html5lib") or it may be the type of markup to be used ("html", "html5", "xml"). It's recommended that you name a specific parser, so that Beautiful Soup gives you the same results across platforms and virtual environments.

**Installing `lxml` parser**:
- (Win): `pip install lxml`
- (Linux): `apt-get install python-lxml`

**Installing `html5lib` parser**:
- (Win): `pip install html5lib`
- (Linux): `apt-get install python-html5lib`

| Parser      | Pros                                | Cons                           |
| ----------- | ----------------------------------- | ------------------------------ |
| html.parser | Included, decent speed              | Slower than lxml, less lenient |
| lxml        | Very fast, sole XML parser          | Requires external dependencies |
| html5lib    | Valid HTML5, browser-like & lenient | Extremely slow, external deps  |

**Older parsers**: `SGMLParser` used in bs3.

> Each parser yields a different tree. [Source](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#differences-between-parsers)

## Parsing details

When using BeautifulSoup (often imported as `bs4`), attribute-value handling depends on two factors: whether the document is parsed as HTML or XML, and whether the attribute is defined by the HTML standard as “multi-valued”.

**What counts as a multi-valued attribute**

According to the documentation, HTML 4 defined a handful of attributes that could hold multiple whitespace-separated values. HTML5 removes some of those and adds a few others. Typical examples include `class`, and others such as `rel`, `rev`, `accept-charset`, `headers`, and `accesskey`.

When BeautifulSoup parses HTML, attributes listed as “multi-valued” by the builder registry are stored as Python lists.

```python
soup = BeautifulSoup('<p class="body strikeout"></p>', 'html.parser')
soup.p['class']  # -> ['body', 'strikeout'] :contentReference[oaicite:2]{index=2}
```

If an attribute appears to have multiple values (whitespace-separated) but is _not_ defined in the registry as multi-valued (see `bs4.builder.builder_registry`), it is kept as a single string.

**Behaviour when parsing as XML**

If you parse markup using an XML parser (e.g., `BeautifulSoup(markup, 'xml')`), then by default _no_ attributes are treated as multi-valued. That means even `class="a b"` will yield a string: `'a b'`.

You _can_ override this by supplying a custom `multi_valued_attributes` mapping when calling the constructor (for example to mark `class` as multi-valued even in XML mode). [Source](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#multi-valued-attributes)

### Parsing details (TLDR)

HTML4 defines some multi-value attributes, and HTML5 removes some while adding a couple more. The `class` attribute is the most common example. Attributes that aren't multi-value as defined by any HTML standard, bs4 stores it as a simple string, otherwise it's stored as a list.

To always get a string, pass `multi_valued_attributes=None` to the constructor.
To always get a list, use the right methods:

```python
tag.p['id'] # Instead of this
tag.p.get_attribute_list('id') # Do this, which wraps the value in a list
```

Side note: Parsing as XML yields no multi-valued attributes.

> Side note to the side note: but it's possible to change this in some uncommon situations.

## Basic Usage

Text version:

Accessing any tag from the HTML tree structure can be done using `soup.tag_name` or `soup.find('tag_name')`. In one case we access the tag using python object attribute, while in the other case we call the find function. The latter is the implementation of the first, so they're equivalent. For example: `soup.title` or `soup.find('title')`. Naturally, the find function gives us more search options. It also finds the first occurrence. For all occurrences use `find_all()` which returns a list of tags. We can access further nested tags too by doing `soup.p.a`. Generally, if no built-in attribute has the same name, a `tag.member` lookup is equivalent to find.

The object representing an HTML / XML tag is of type `Tag`. All such objects have a `.name` attribute with the name of the tag. If there is text sandwiched between the opening and closing tags, it will be available in `.string`. When this is not the case, `.string` will be `None`.

Code version:

```python
soup = BeautifulSoup(html, 'html.parser')

# Access tags - these are equivalent
soup.tag_name          # Returns first match or None
soup.find('tag_name')  # More search options

soup.find_all('tag')   # Returns list (empty if no matches)
soup('tag')            # Shorthand for find_all

soup.p.a               # Nested access (first <a> in first <p>)

# Read attributes
tag.name               # Tag name
tag.string             # Text if single child, else None
tag.attrs              # Dictionary of all attributes
tag.get('attr')        # Get attribute safely
tag['attr']            # Access/modify attribute
del tag['attr']        # Delete attribute
tag.get_text()         # Extracts all text (children included)

# Text extraction
soup.get_text()        # All text (no script/style/template)                        
soup.get_text(separator='\n', strip=True)  # With separator and stripping

# Modify
tag.name = 'blockquote'
tag['class'] = 'myclass'
tag.string = 'new text'
tag.clear()                              # Remove all contents
```

> We always specify the parser, even when using the default html.parser because bs4 shows a warning otherwise.

> The html can be provided either as a string or as a file handle.

> Changes reflect in the whole tree / soup object.

Simple navigation:

```python
for child in tag:
	print(child.name)
```

This will include `NavigableString`, not just `Tag` objects. Those don’t have `.name`, `.get_text()`, or `.attrs`!

On `get_text()`: If you only want the human-readable text inside a document or tag (so, not script, style or template content), you can use the `get_text()` method. It returns all the text in a document or beneath a tag, as a single Unicode string. [Source](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#get-text)

From the docs:

> As of Beautiful Soup version 4.10.0, you can call get_text(), .strings, or .stripped_strings on a NavigableString object. It will either return the object itself, or nothing, so the only reason to do this is when you're iterating over a mixed list.

## Navigation & Properties

Text version:

For recursive iteration of all of a tag's children, use `.descendants`. If a tag contains 1 child and it's a nav-string, then the child is made available as `.string`, otherwise this property returns `None`. Iterate a tag's strings recursively using `.strings` and `.stripped_strings`. The parent element is accessible through `.parent`. The parent of a top-level tag like html is the BeautifulSoup object itself, and `soup.parent` is None. Iterate upwards in the hierarchy of parents using `.parents`.

Accessing siblings is done with `.next_sibling` & `previous_sibling`. If they don't exist, `None` is returned. They can return a tag or nav-string, usually. The siblings of a nav-string are usually `None`, but not always. For example, **when there's text mixed with elements, the text/strings will count as siblings at the same level**. Iterating siblings is done with the generators: `.next_siblings` & `previous_siblings`.

When navigating using document parse order, we get different results. `.next_element` and `.previous_element` are similar to the siblings versions, but different. Navigating to siblings is like running BFS on the parse tree. Navigating to the next element is like running DFS on the parse tree.

Code version:

```python
tag.contents           # Direct children (list, strings included)
tag.children           # Direct children (generator, strings included)
tag.descendants        # Recursive iterator, all descendants

tag.string             # Child text when only one, else None
tag.strings            # All descendant strings (generator)
tag.stripped_strings   # Same as .strings but stripped of whitespace

tag.parent             # Parent tag (BeautifulSoup for root)
tag.parents            # Iterator upward

tag.next_sibling, tag.previous_sibling    # Adjacent siblings (None if missing)
tag.next_siblings, tag.previous_siblings  # Iterators

tag.next_element, tag.previous_element    # Document order (DFS)
tag.next_elements, tag.previous_elements  # Iterators
```

Iterate the direct children using `.children`:

```python
for c in t.children:
	print(c)
	
# Which is the same as
for c in t:
	print(c)
```

> Never modify the `.contents` directly.

## Finding & Filtering

**Common filters**: strings, regex (`re.compile(pattern)`), functions returning bool, `True` (match all), lists

```python
# Basic find
soup.find('a')                           # First <a>
soup.find_all('a', limit=2)              # First 2 <a> tags

# Filter by attributes
soup.find_all(id=True)                   # Has id attribute
soup.find_all(id='main')                 # id="main"
soup.find_all(attrs={'data-x': 'y'})     # For attributes with special chars
soup.find_all(class_='highlight')        # CSS class (v4.1.2+)

# Filter by string content
soup.find_all(string='exact text')       # Exact match
soup.find_all(string=re.compile(r'text'))  # Regex match

# Search options
soup.find_all('a', recursive=False)      # Only direct children
soup.find(name='a', attrs={...}, string='x', limit=n)  # Ellipsis is a placeholder
soup.find(id='my_id')                    # Custom attributes
soup.find_all('a', limit=2)              # Limit like in SQL

# CSS selectors
soup.select('div.container > p')         # CSS syntax
soup.select_one('p.intro')               # First match only
```

**Ancestor/sibling searching**:
```python
tag.find_parent('div')                   # First parent <div>
tag.find_parents('div')                  # All parent <div>s
tag.find_next_sibling('p')               # Next sibling <p>
tag.find_next_siblings('p')              # All next sibling <p>s
tag.find_next('p')                       # Next <p> in document order
tag.find_all_next('p')                   # All <p> after this tag
# (also find_previous_sibling(s) and find_all_previous)
```

Function signature for `find_all`: `name, attrs, recursive, string, limit, kwargs`.
- By default, `find_all` is recursive. To search only direct children use `recursive=False`.
Function signature for `find`: `name, attrs, recursive, string, kwargs`.

Both `find` and `find_all` functions take multiple types of filters:
- strings
- functions (accepts one value and returns `True` or `False`)
- regex object (`re.complile`)
- `True` -> matches regardless of value
- List (objects can be of type other than `Tag` (CONFIRM))

1. `attrs` is a dictionary used when the attribute name can't be given as an argument, either because another argument uses that name (e.g. `tag.name`) or because it's not valid Python (e.g. `data-*` attributes in HTML 5). Example: `{'name':'red'}`.
2. Any keyword argument that isn't recognized (and thus will be passed through `kwargs`) will be turned into a filter that matches tags by their attributes.
3. As of BS4 version 4.1.2, you can search by CSS class using the keyword argument `class_`. It works with all aforementioned filter types, as with any keyword argument.

Important difference: `find` returns one object or `None`, while `find_all` returns a list of objects or an empty list. Therefore, the following are NOT equivalent:

```python
soup.find('title') # Returns the object
soup.find_all('title', limit=1) # Returns the object in a list
```

For convenience, calling a BS4 object or Tag as a function is equivalent to calling `find_all()` as long as you're not calling a Python built-in or other predefined function object:

```python
soup.find_all('a')
soup('a')
# or even
soup('a',recursive=False)
```

Also note: Passing `recursive=False` into `find_parents()` (or similar) doesn't do anything.

## Modifying & Building

```python
# Manipulate tree
tag.append(new_tag)                      # Add child at end
tag.insert(0, new_tag)                   # Insert at position
tag.extend([tag1, tag2])                 # Add multiple children
tag.insert_before(new_tag)               # Insert as previous sibling
tag.insert_after(new_tag)                # Insert as next sibling
tag.replace_with(new_tag)                # Replace with another tag/string
tag.extract()                            # Remove and return tag
tag.wrap(new_tag)                        # Wrap in another tag
tag.unwrap()                             # Remove wrapper, keep contents

# The methods `replace_with` and `unwrap` return a new object.

# Create tags
soup.new_tag('div', id='main', class_='container')

# String replacement
tag.string.replace_with('new text')      # Or replace with tags
```

## BS4 Classes I - Core Classes

The `Tag` class doesn't need an introduction. Key methods:

```
append(), extend(), insert(), insert_before(), insert_after(), clear(), extract(), decompose(), replace_with(), wrap(), unwrap(), prettify(), encode(), decode(), get_text(), find(), find_all(), select(), select_one().
```

> See the [documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) for more.

Core classes:
- `NavigableString` - Wrapper class for the text between the opening & closing tags
	- They're like Python Unicode strings, but with extra features (i.e. tree navigation).
	- Nav-strings don't have `.find()`, `.string` or `.contents`. They should be passed to `unicode()` before externally using them.
- `BeautifulSoup` - Holds the parse tree. For most purposes can be treated as a tag
	- Combine two trees: `soup.find(text='insert here').replace_with(footer)`. Works with nav-strings, tags and bs4 objects.
	- `soup.name` is `'[document]'` of type string.
- `Comment` - A subtype of `NavigableString`
- (BS 4.9.0+) Other nav-string subclases for various HTML elements include:
	- `Stylesheet` for style elements: `type(soup.style.string)`
	- `Script` for script elements: `type(soup.script.string)`
	- `Template` for template elements: `type(soup.template.string)`

> `PageElement`: Abstract base class for `Tag` and `NavigableString`. Provides common methods like `extract()`, `replace_with()`, etc.

Example for `Comment`:

```python
from bs4 import BeautifulSoup

markup = "<b><!--Hey, buddy. Want to buy a used parser?--></b>"
soup = BeautifulSoup(markup, 'html.parser')
comment = soup.b.string

type(comment)  # <class 'bs4.element.Comment'>
print(comment)  # Hey, buddy. Want to buy a used parser?
print(soup.b.prettify())  # Shows <!-- --> formatting
```

Special String Classes (XML Documents):
- `Declaration` - Represents the XML declaration at the beginning of an XML document.
- `Doctype` - Represents the document type declaration in an XML document.
- `CData` - Represents a CDATA section in XML, which preserves all content exactly as-is.
- `ProcessingInstruction` - Represents XML processing instructions.

### Code Examples

For `Declaration`:

```python
from bs4 import BeautifulSoup
xml = '<?xml version="1.0"?><root></root>'
soup = BeautifulSoup(xml, 'xml')
```

For `Doctype`:

```python
from bs4 import BeautifulSoup
xml = '<!DOCTYPE html><root></root>'
soup = BeautifulSoup(xml, 'xml')
```

For `CData`:

```python
from bs4.element import CData
soup = BeautifulSoup("<a></a>", 'html.parser')
soup.a.string = CData("one < three")
# Output: <a><![CDATA[one < three]]></a>
```

For `ProcessingInstruction`:

```python
from bs4 import BeautifulSoup
xml = '<?xml-stylesheet type="text/xsl" href="style.xsl"?>'
soup = BeautifulSoup(xml, 'xml')
```

### Bonus I

**Key Attributes of `NavigableString`:**
- `.parent` — Parent tag containing string
- `.next_sibling`, `.previous_sibling` — Adjacent strings/tags
- `.next_element`, `.previous_element` — Following/preceding parsed elements

It cannot use: `.contents`, `.string`, `find()` methods

### Bonus II

**Instantiation of `BeautifulSoup`:** `BeautifulSoup(markup, parser, from_encoding=None, exclude_encodings=None, parse_only=None, multi_valued_attributes=None, on_duplicate_attribute=None, element_classes=None, store_line_numbers=True)`

**Key Attributes:**
- `.name` — Returns `'[document]'`
- `.original_encoding` — Original encoding detected (or `None` if already Unicode)
- `.contains_replacement_characters` — Boolean flag indicating replacement characters used

## Output & Formatting

```python
str(soup)                                # HTML string
soup.prettify()                          # Pretty-printed with indentation
soup.encode(formatter='html')            # HTML entity encoding
soup.decode(formatter='html')

# Formatter options: 'minimal' (default), 'html', 'html5', None
# Custom formatters available via subclassing HTMLFormatter/XMLFormatter
```

## Formatter Configuration

**Formatter options**:
- `formatter="minimal"` - Default, minimal escaping
- `formatter="html"` - Convert to HTML entities
- `formatter="html5"` - HTML5 format (void tags)
- `formatter=None` - No formatting

The formatter argument can be found on these three methods: `encode`,  `decode`,  `prettify`

Basic formatter example:

```python
from bs4.formatter import HTMLFormatter
def uppercase(str):
    return str.upper()

formatter = HTMLFormatter(uppercase)

print(soup.prettify(formatter=formatter))
# <p>
#  IL A DIT <<SACRÉ BLEU!>>
# </p>

print(link_soup.a.prettify(formatter=formatter))
# <a href="HTTP://EXAMPLE.COM/?FOO=VAL1&BAR=VAL2">
#  A LINK
# </a>
```

## BS4 Classes II - Formatter Classes

Formatter classes:
- `HTMLFormatter` - Customizes formatting rules for HTML output.
	- **Constructor:** `HTMLFormatter(formatter_function=None, indent=None)`
	- **Key Methods:** `.attributes(tag)`: Override to control the output attributes & their order
- `XMLFormatter` - Customizes formatting rules for XML output.

Subclassing `HTMLFormatter` or `XMLFormatter` will give you even more control over the output. For example, the attributes are sorted per tag by default. To turn this off, you can subclass the `Formatter.attributes()` method, which controls which attributes are output and in what order.

For instance, to remove the attribute `unwanted` whenever it appears:
```python
class UnsortedAttributes(HTMLFormatter):
    def attributes(self, tag):
        for k, v in tag.attrs.items():
            if k == 'unwanted':
                continue
            yield k, v
```

### Code examples

Control how HTML is formatted when outputting to string: 
```python
from bs4.formatter import HTMLFormatter

# Custom formatter with function
def uppercase(string):
    return string.upper()

formatter = HTMLFormatter(uppercase)
soup.prettify(formatter=formatter)

# Formatter with custom indentation
formatter = HTMLFormatter(indent=8)
soup.prettify(formatter=formatter)
```

Control how XML is formatted when outputting to string:
```python
from bs4.formatter import XMLFormatter

formatter = XMLFormatter()
soup.prettify(formatter=formatter)
```

## BS4 Classes III - Specialized Classes

Specialized classes:
- `SoupStrainer` - Selectively parses only specific parts of a document for better performance.
- `ElementFilter` - Low-level interface for custom element filtering and iteration.
- `UnicodeDammit` - Automatically detects and converts document encoding to Unicode.

### Code Examples (with notes)

Parse only relevant portions of large documents instead of parsing everything:
```python
from bs4 import BeautifulSoup, SoupStrainer

# Create strainers with search criteria
only_a_tags = SoupStrainer("a")
only_links = SoupStrainer(id="link2")

def is_short_string(string):
    return string is not None and len(string) < 10

only_short = SoupStrainer(string=is_short_string)

# Use strainer when parsing
soup = BeautifulSoup(html_doc, "html.parser", parse_only=only_a_tags)
```
- Pass to `parse_only` parameter in `BeautifulSoup` constructor.
- **Constructor:** `SoupStrainer(name=None, attrs=None, string=None, **kwargs)` — same filter arguments as search methods
- **Behavior:** Matching tags parse automatically with all children; non-matching tags' children are still checked.
- **Note**: Works with `html.parser` and `lxml`, but not `html5lib` [Source](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#parsing-only-part-of-a-document)

Create completely custom matching behaviors for searching the parse tree:
```python
from bs4 import Tag, NavigableString
from bs4.filter import ElementFilter

# Define custom filter function
def non_whitespace_element_func(tag_or_string):
    return (
        isinstance(tag_or_string, Tag) or
        (isinstance(tag_or_string, NavigableString) and
         tag_or_string.strip() != "")
    )

# Create filter
non_whitespace_filter = ElementFilter(non_whitespace_element_func)

# Use in searches
soup.find_all(non_whitespace_filter)
soup.find_next(non_whitespace_filter)

# Custom iteration
def random_walk(starting_location):
    location = starting_location
    while location is not None:
        yield location
        location = location.next_element

results = list(non_whitespace_filter.filter(random_walk(soup.b)))
```
- Define matching function and iterate over `PageElement` objects.
- **Constructor:** `ElementFilter(matching_function)` where function returns `True`/`False`
- **Key Methods:** `.filter(generator)`: Using custom generator of `PageElement` objects
- **Use Cases:** Combine custom matching logic with search methods; complete customization

Handle documents in unknown encodings and convert them to Unicode:
```python
from bs4 import UnicodeDammit

# Auto-detect encoding
dammit = UnicodeDammit(b"\xc2\xabSacr\xc3\xa9 bleu!\xc2\xbb")
print(dammit.unicode_markup)  # «Sacré bleu!»
print(dammit.original_encoding)  # 'utf-8'

# Provide encoding hints
dammit = UnicodeDammit("Sacr\xe9 bleu!", ["latin-1", "iso-8859-1"])
print(dammit.original_encoding)  # 'latin-1'

# Convert smart quotes
markup = b"<p>I just \x93love\x94 Word\x92s quotes</p>"
result = UnicodeDammit(markup, ["windows-1252"], smart_quotes_to="html")

# Handle mixed encodings
new_doc = UnicodeDammit.detwingle(mixed_doc)
```
- **Constructor:** `UnicodeDammit(data, encodings=None, is_html=False, exclude_encodings=None, smart_quotes_to=None)`
- **Key Methods:** `.detwingle(data)` — Convert mixed UTF-8/Windows-1252 to pure UTF-8. (BS 4.1.0+)
- **Key Attributes:**
	- `.unicode_markup` — Detected/converted Unicode string
	- `.original_encoding` — Detected encoding name

## Utility Functions/Methods

`diagnose()` - Analyzes a document and reports how different parsers handle it.

Troubleshoot parsing issues and determine which parser to use:
```python
from bs4.diagnose import diagnose

with open("bad.html") as fp:
    data = fp.read()

diagnose(data)
# Outputs detailed diagnostic information about parsing
```

`has_attr(key)` - Check if tag has specified attribute.

`__call__(name, attrs, string, limit, **kwargs)`
- Calling tag/soup directly is equivalent to `find_all()`.

## Comparison

### `==` operator
Tags/strings are equal if they represent identical markup (attributes order doesn't matter).

## Filter by CSS selector syntax

BS4 objects also have a `.css` property. The actual selector implementation is handled by the [Soup Sieve](https://facelessuser.github.io/soupsieve/) package, available on PyPI as `soupsieve`. If you installed Beautiful Soup through `pip`, Soup Sieve was installed at the same time.

To select using CSS syntax, use the `select()` and `select_one()` methods on the `.css` property.

The Soup Sieve documentation lists [all the currently supported CSS selectors](https://facelessuser.github.io/soupsieve/selectors/), but here are some of the basics.

The examples can be found here: https://www.crummy.com/software/BeautifulSoup/bs4/doc/#css-selectors-through-the-css-property

For convenience, BeautifulSoup allows calling `select()` and `select_one()` directly by omitting the `.css` property.

From the docs:

> If CSS selectors are all you need, you should skip Beautiful Soup altogether and parse the document with `lxml`: it's a lot faster. But Soup Sieve lets you _combine_ CSS selectors with the Beautiful Soup API.

Additional `.css` selectors:
- `css.iselect(selector)` - `select()` but returns a generator instead of a list. (BS 4.12.0+)
- `css.closest(selector)` - Returns nearest parent matching CSS selector (or `None`).
- `css.match(selector)` - Returns boolean whether tag matches CSS selector.
- `css.filter(selector)` - Returns list of tag's direct children matching CSS selector.
- `css.escape(identifier)` - Escapes CSS identifiers with invalid characters.

## Quick Reference: Searching Methods

All these methods work on BeautifulSoup and Tag objects and accept similar filters:
- `find()` - Returns first match or None
- `find_all()` - Returns list of all matches
- `find_parent()` - Returns first parent match
- `find_parents()` - Returns all parent matches
- `find_next_sibling()` - Returns next matching sibling
- `find_next_siblings()` - Returns all next matching siblings
- `find_previous_sibling()` - Returns previous matching sibling
- `find_previous_siblings()` - Returns all previous matching siblings
- `find_next()` - Returns next matching element
- `find_all_next()` - Returns all next matching elements
- `find_previous()` - Returns previous matching element
- `find_all_previous()` - Returns all previous matching elements
- `select()` - CSS selector (returns list)
- `select_one()` - CSS selector (returns first match or None)

**Their Arguments:**
- `name` — String, regex, function, `True`, or list of these
- `attrs` — Dictionary for complex attribute searches (e.g., data-* attributes)
- `string` — Filter text content (same filter types as `name`)
- `recursive` — Set `False` to search only direct children
- `limit` — Maximum results to return
- `**kwargs` — Attribute filters (use `class_` for CSS class)

**Filter Types (for search methods):**
- **String:** Exact tag/attribute name match
- **Regex:** `re.compile('pattern')` for pattern matching
- **Function:** Function returning `True`/`False` for single argument
- **True:** Matches every tag (or every attribute if used with keyword)
- **List:** Match against any item in list (string, regex, function, or True)

## Quick Reference: Tag objects

**Key Attributes:**
- `.name` — Tag name (read/write)
- `.attrs` — Dictionary of all attributes
- `.string` — Direct string content (if tag contains only one string)
- `.contents` — List of tag's direct children
- `.children` — Generator of direct children
- `.parent` — Direct parent tag
- `.parents` — Generator of all parents up the tree
- `.previous_sibling` — Previous sibling tag/string
- `.next_sibling` — Next sibling tag/string
- `.previous_siblings` — Generator of all previous siblings
- `.next_siblings` — Generator of all following siblings
- `.next_element` — Next parsed element in document order
- `.previous_element` — Previous parsed element in document order
- `.next_elements` — Generator of all following elements
- `.previous_elements` — Generator of all preceding elements
- `.sourceline` — Line number in source (html.parser/html5lib only)
- `.sourcepos` — Position within line (html.parser/html5lib only)
- `.decomposed` — Boolean flag indicating if tag is decomposed (BS 4.9.0+)

**Dictionary-like Access:**
- `tag['attr']` — Get attribute value
- `tag['attr'] = value` — Set attribute value
- `del tag['attr']` — Delete attribute
- `tag.get('attr', default)` — Safe attribute access
- `tag.has_attr('attr')` — Check attribute existence

**Key Methods:**
- `.get_attribute_list(attr)` — Always return attribute as list
- `.string` — Shortcut to first string in tag
- `.get_text(separator='', strip=False)` — Extract all text content
- `.stripped_strings` — Generator of non-empty text strings

## Quick Reference: Tag Modification

`append(element)`
Add element to end of tag's contents.
Returns appended element.

`extend(elements)`
Add all elements from list to tag's contents.
Returns list of appended elements. (BS 4.7.0+)

`insert(position, element)`
Insert element at numeric position in tag's contents.
Multiple elements supported.
Returns list of inserted elements.

`insert_before(element)`
Insert tag/string immediately before current element.
Returns list of inserted elements.

`insert_after(element)`
Insert tag/string immediately after current element.
Returns list of inserted elements.

`clear()`
Remove all contents from tag.

`extract()`
Remove tag/string from tree and return it.
Parent becomes `None`, allowing separate manipulation.

`decompose()`
Remove tag/string and completely destroy it and contents.
Check `.decomposed` property afterward. (BS 4.9.0+)

`new_tag(name, namespace=None, nsprefix=None, attrs={}, **kwargs)`
Create new tag (on BeautifulSoup object only).
Returns empty `Tag` object.

`new_string(s, subclass=NavigableString)`
Create new string object (on BeautifulSoup object only).

`copy_self()`
Create shallow copy of tag (without contents). (BS 4.13.0+)

`replace_with(*elements)`
Extract tag/string and replace with one or more tags/strings.
Returns replaced element/string. (BS 4.10.0+ supports multiple arguments)

`wrap(tag)`
Wrap element in specified tag.
Returns new wrapper tag.

`unwrap()`
Replace tag with its contents.
Returns replaced tag.
Opposite of `wrap()`.

`smooth()`
Consolidate adjacent `NavigableString` objects into single strings.
Cleans up after multiple modifications. (BS 4.8.0+)

## Quick Reference: Output Methods

`prettify(formatter='minimal', encoding=None)`
Return formatted string with each tag/string on separate line. Returns UTF-8 unless encoding specified.

`str()` - Return compact string representation (no formatting).

`encode(encoding='utf-8', formatter='minimal')` - Return bytestring with specified encoding.

`decode(formatter='minimal')` - Return Unicode string.

`get_text(separator='', strip=False)` - Extract all text content as single string.
`strip=True` removes whitespace around each text bit.

`stripped_strings` - Generator yielding non-empty text strings (whitespace stripped).

## Quick Reference: `soup.new_tag()`

Basic Syntax:
`tag_obj = soup.new_tag(name, namespace=None, nsprefix=None, attrs={}, **kwargs)`

Parameters:
- `name` — Tag name as string (required, e.g., `'div'`, `'a'`, `'p'`)
- `namespace` — XML namespace URI (optional, for XML documents)
- `nsprefix` — XML namespace prefix (optional, for XML documents)
- `attrs` — Dictionary of initial attributes (optional, alternative to `**kwargs`)
- `**kwargs` — Tag attributes passed as keyword arguments (alternative to `attrs` dict)

Returns: Empty `Tag` object detached from any tree

Additional notes:
- Created tags are regular `Tag` objects with full functionality. Access them as you would any other tag.
- `new_tag()` is faster than parsing HTML strings via `BeautifulSoup()`
- Created tags don't participate in parsing and have no document context until inserted

### Examples

Create a basic tag with no attributes:
```python
new_div = soup.new_tag('div')
```
Creates: `<div></div>`

Adding attributes via `**kwargs`:
```python
new_link = soup.new_tag('a', href='http://example.com', id='mylink')
```
Creates: `<a href="http://example.com" id="mylink"></a>`

Adding attributes via `attrs` dictionary:
```python
new_div = soup.new_tag('div', attrs={'data-id': '123', 'class': 'container'})
```
Creates: `<div class="container" data-id="123"></div>`

> Use the `attrs` parameter for complex attribute names (e.g., containing hyphens or reserved keywords)

For attributes with multiple values (like `class`), pass as list or space-separated string:
```python
new_p = soup.new_tag('p', attrs={'class': ['highlight', 'bold']})
# Or with string:
new_p = soup.new_tag('p', attrs={'class': 'highlight bold'})
# Creates same result.
```
Creates: `<p class="highlight bold"></p>`

For XML documents, specify namespace and prefix:
```python
soup = BeautifulSoup('', 'xml')
ns_tag = soup.new_tag('item', namespace='http://example.com/ns', nsprefix='ex')
```
Creates: `<ex:item xmlns:ex="http://example.com/ns"></ex:item>`

To copy, either create anew, or use `copy.copy()`:
```python
import copy
original = soup.new_tag('div', id='original')
original.string = 'Content'
duplicate = copy.copy(original)
```

### Edge Cases

**Empty attributes dict:** `new_tag('div', attrs={})` works fine; no attributes added

**None values:** `new_tag('div', title=None)` creates tag with `title="None"` (string); use `attrs` dict without key to omit

**Boolean attributes (HTML5):** `new_tag('input', checked='checked')` or in HTML5 output use formatter

**Reserved keywords:** Use `attrs` dict: `new_tag('div', attrs={'class': 'x'})` instead of `new_tag('div', class='x')`

### Integration with Search & Modification

`new_tag()` integrates seamlessly with all tree modification methods:

```python
soup = BeautifulSoup('<div id="parent"></div>', 'html.parser')
parent = soup.find('div')

# Create and insert new tags
new_p = soup.new_tag('p')
new_p.string = 'New paragraph'
parent.append(new_p)

# Wrap existing content
wrapper = soup.new_tag('section')
parent.wrap(wrapper)

# Extract and reuse
extracted = new_p.extract()
another_parent = soup.new_tag('article')
another_parent.append(extracted)
```

## Advanced I

**Line tracking:** Available via `tag.sourceline` and `tag.sourcepos` (html.parser/html5lib only; disable with `store_line_numbers=False`)

## bs4 v4.14.2 object properties overview

```
children GEN
descendants GEN
next_elements GEN
next_siblings GEN
parents GEN
previous_elements GEN
previous_siblings GEN
self_and_descendants GEN
self_and_next_elements GEN
self_and_next_siblings GEN
self_and_parents GEN
self_and_previous_elements GEN
self_and_previous_siblings GEN
strings GEN
stripped_strings GEN

__weakref__ N
declared_html_encoding N
markup N
namespace N
nextSibling N
next_sibling N
original_encoding N
parent N
parse_only N
prefix N
previous N
previousSibling N
previous_element N
previous_sibling N
sourceline N
sourcepos N
string N

__dir__ BIN
__format__ BIN
__init_subclass__ BIN
__new__ BIN
__reduce__ BIN
__reduce_ex__ BIN
__sizeof__ BIN
__subclasshook__ BIN

__annotations__ DCT
__dict__ DCT
_namespaces DCT
cdata_list_attributes DCT
element_classes DCT

ASCII_SPACES STR
ROOT_TAG_NAME STR
__doc__ STR
__module__ STR
name STR
text STR

__firstlineno__ INT

DEFAULT_BUILDER_FEATURES LST
contents LST
current_data LST
preserve_whitespace_tag_stack LST
string_container_stack LST
tagStack LST

__static_attributes__ TPL
default TPL

MAIN_CONTENT_STRING_TYPES SET
interesting_string_types SET
preserve_whitespace_tags SET

_is_xml B8L
can_be_empty_element B8L
contains_replacement_characters B8L
decomposed B8L
hidden B8L
is_empty_element B8L
is_xml B8L
known_xml B8L

EMPTY_ELEMENT_EVENT <class 'bs4.element.Tag._TreeTraversalEvent'>
END_ELEMENT_EVENT <class 'bs4.element.Tag._TreeTraversalEvent'>
START_ELEMENT_EVENT <class 'bs4.element.Tag._TreeTraversalEvent'>
STRING_ELEMENT_EVENT <class 'bs4.element.Tag._TreeTraversalEvent'>
_most_recent_element <class 'bs4.element.NavigableString'>
attrs <class 'bs4.element.AttributeDict'>
builder <class 'bs4.builder._html5lib.HTML5TreeBuilder'>
css <class 'bs4.css.CSS'>
currentTag <class 'bs4.BeautifulSoup'>
next <class 'bs4.element.Tag'>
next_element <class 'bs4.element.Tag'>
open_tag_counter <class 'collections.Counter'>
```

The script used to generate it:

```python
def colorize(text, fg_color='91', bg_color='0', fg_bright=True, bg_bright=False):
    O33 = '\033['
    END = '\033[0m'

    colors = ['black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white']

    # Color mappings
    f_dk = {v: str(30 + i) for i, v in enumerate(colors)}  # Foreground: Dark colors
    f_br = {v: str(90 + i) for i, v in enumerate(colors)}  # Foreground: Bright colors
    b_dk = {v: str(40 + i) for i, v in enumerate(colors)}  # Background: Dark colors
    b_br = {v: str(100 + i) for i, v in enumerate(colors)}  # Background: Bright colors

    the_list = [f_br[fg_color] if fg_bright else f_dk[fg_color]]

    if bg_color != '0':
        the_list.append(b_br[bg_color] if bg_bright else b_dk[bg_color])

    res = f'{O33}{';'.join(the_list)}m{text}{END}'
    return res


def my_dir(obj, colored_output=False):
    cm = {  # Custom Mapping
        "<class 'str'>": "STR",
        "<class 'list'>": "LST",
        "<class 'set'>": "SET",
        "<class 'type'>": "TPE",
        "<class 'dict'>": "DCT",
        "<class 'method'>": "MTH",
        "<class 'method-wrapper'>": "MTHW",
        "<class 'builtin_function_or_method'>": "BIN",
        "<class 'int'>": "INT",
        "<class 'tuple'>": "TPL",
        "<class 'NoneType'>": "N",
        "<class 'bool'>": "B8L",
        "<class 'generator'>": "GEN"
    }

    r = dict()
    for key in dir(obj):
        r[key] = str(type(getattr(obj, key)))

        # Replace the type values of interest
        if r[key] in cm:
            r[key] = cm[r[key]]

    if colored_output:
        for k, v in r.items():
            match v:
                case "STR":
                    r[k] = colorize(v, 'green')
                case "LST" | "TPL":
                    r[k] = colorize(v, 'cyan')
                case "SET" | "DCT":
                    r[k] = colorize(v, 'red')
                case "TPE":
                    r[k] = colorize(v, 'cyan', fg_bright=False)
                case "MTH" | "MTHW":
                    r[k] = colorize(v, 'magenta')
                case "BIN":
                    r[k] = colorize(v, 'blue', fg_bright=False)
                case "INT":
                    r[k] = colorize(v, 'blue')
                case "N":
                    r[k] = colorize(v, 'black')
                case "B8L":
                    r[k] = colorize(v, 'yellow')
                case "GEN":
                    r[k] = colorize(v, 'magenta', fg_bright=False)
    return r
```