# Week 3 Lecture: JSON & File I/O

## Learning Objectives

By the end of this lecture, students will be able to:
1. Understand the JSON data format and its role in web development
2. Read and write text files in Python
3. Parse JSON data into Python objects
4. Save Python data structures as JSON files
5. Handle file errors gracefully
6. Build a persistent place database
7. Work with file paths using `pathlib`
8. Validate and debug JSON data

**Estimated Time:** 3 hours (including exercises and breaks)

---

# Hour 1: Introduction to Data Persistence and JSON

## Part 1: Why File I/O? (15 minutes)

### The Problem with In-Memory Data

Every time you run a Python program, variables start fresh:

```python
# Run 1: Add some places
places = [
    {"name": "Taipei 101", "rating": 4.7},
    {"name": "Din Tai Fung", "rating": 4.9},
]
places.append({"name": "Shilin Market", "rating": 4.5})
print(f"We have {len(places)} places!")  # 3 places

# Program ends...

# Run 2: Start over
places = []  # Empty again!
print(f"We have {len(places)} places!")  # 0 places 😢
```

### Types of Data Storage

| Storage Type | Speed | Persistence | Use Case |
|--------------|-------|-------------|----------|
| Variables (RAM) | Very Fast | No (lost on exit) | Temporary data |
| Text Files | Fast | Yes | Configuration, logs |
| JSON Files | Fast | Yes | Structured data, APIs |
| CSV Files | Fast | Yes | Tabular data, spreadsheets |
| Databases | Medium | Yes | Large data, queries |

### The Solution: File Storage

```python
# Save to file before exiting
save_places(places, "places.json")

# Later, in a new session...
places = load_places("places.json")
# All your data is back! 🎉
```

### Real-World Examples

1. **Video Games** - Save game progress to files
2. **Web Browsers** - Store bookmarks, history in files
3. **Mobile Apps** - Cache data locally in JSON
4. **Our Project** - Save favorite places for later use

---

## Part 2: Introduction to JSON (20 minutes)

### What is JSON?

**JSON** = **J**ava**S**cript **O**bject **N**otation

Created by Douglas Crockford in the early 2000s as a lightweight alternative to XML.

**Key characteristics:**
- Human-readable text format
- Language-independent (Python, JavaScript, Java, Go, etc.)
- The standard for web APIs (REST APIs)
- Simpler than XML, more structured than CSV

### JSON vs Other Formats

```
XML (old school):
<place>
    <name>Taipei 101</name>
    <rating>4.7</rating>
</place>

JSON (modern):
{"name": "Taipei 101", "rating": 4.7}

CSV (tabular):
name,rating
Taipei 101,4.7
```

### JSON Syntax Rules

```json
{
    "name": "Taipei 101",
    "latitude": 25.0330,
    "longitude": 121.5654,
    "rating": 4.7,
    "is_open": true,
    "tags": ["landmark", "shopping", "observation"],
    "floors": 101,
    "address": null
}
```

**Important rules:**
1. Data is in key-value pairs
2. Keys MUST be strings with **double quotes**
3. Values can be: string, number, boolean, null, array, object
4. Items separated by commas
5. NO trailing commas allowed
6. NO comments allowed

### JSON Data Types

| JSON Type | Python Type | JSON Example | Python Example |
|-----------|-------------|--------------|----------------|
| object | `dict` | `{"a": 1}` | `{"a": 1}` |
| array | `list` | `[1, 2, 3]` | `[1, 2, 3]` |
| string | `str` | `"hello"` | `"hello"` |
| number (int) | `int` | `42` | `42` |
| number (float) | `float` | `3.14` | `3.14` |
| true | `True` | `true` | `True` |
| false | `False` | `false` | `False` |
| null | `None` | `null` | `None` |

### 🔍 Spot the Differences: JSON vs Python

```python
# Python dictionary
python_dict = {
    "name": "Taipei 101",
    "rating": 4.7,
    "is_open": True,      # Capital T
    "address": None,      # Capital N
    'alt_name': '101',    # Single quotes OK in Python
}

# Equivalent JSON (as a string)
json_string = """
{
    "name": "Taipei 101",
    "rating": 4.7,
    "is_open": true,
    "address": null
}
"""
# Note: No single quotes, lowercase true/null, no trailing comma
```

### ⚠️ JSON Limitations

```python
# Things that DON'T work in JSON:

# 1. Tuples → become lists
coords = (25.0330, 121.5654)  # Python tuple
# In JSON: [25.0330, 121.5654]  # Becomes array

# 2. Sets → NOT supported
tags = {"food", "local"}  # Python set
# JSON cannot represent sets!

# 3. Comments → NOT allowed
# { "name": "test" /* comment */ }  ← INVALID JSON

# 4. Single quotes → must use double
# {'name': 'test'}  ← INVALID JSON
# {"name": "test"}  ← VALID JSON

# 5. Trailing commas → NOT allowed
# {"a": 1, "b": 2,}  ← INVALID JSON (trailing comma)
# {"a": 1, "b": 2}   ← VALID JSON

# 6. Special float values → NOT standard
# NaN, Infinity, -Infinity are not valid JSON
```

### 🎯 Mini-Exercise 1: Valid or Invalid?

Which of these are valid JSON? (Answers at bottom of section)

```
A) {"name": "test", "value": 42}
B) {'name': 'test'}
C) {"items": [1, 2, 3,]}
D) {"active": True}
E) {"data": null}
F) {"coords": (25.0, 121.5)}
```

<details>
<summary>Click for answers</summary>

- A) ✓ Valid
- B) ✗ Invalid (single quotes)
- C) ✗ Invalid (trailing comma)
- D) ✗ Invalid (True should be true)
- E) ✓ Valid
- F) ✗ Invalid (tuples not supported, and uses parentheses)

</details>

---

## Part 3: The `json` Module (25 minutes)

### Importing the Module

```python
import json  # Built-in, no installation needed!
```

### The Four Key Functions

| Function | Purpose | Direction |
|----------|---------|-----------|
| `json.dumps()` | Python → JSON string | Serialize to string |
| `json.loads()` | JSON string → Python | Parse from string |
| `json.dump()` | Python → JSON file | Serialize to file |
| `json.load()` | JSON file → Python | Parse from file |

**Memory trick:**
- `s` at the end = **s**tring (dumps/loads)
- No `s` = file (dump/load)

### Converting Python to JSON String: `json.dumps()`

```python
import json

place = {
    "name": "Taipei 101",
    "coords": [25.0330, 121.5654],
    "rating": 4.7,
    "is_open": True,
    "address": None
}

# Basic conversion
json_string = json.dumps(place)
print(json_string)
# {"name": "Taipei 101", "coords": [25.033, 121.5654], "rating": 4.7, "is_open": true, "address": null}
print(type(json_string))  # <class 'str'>
```

### Pretty Printing JSON

```python
# With indentation (much more readable!)
json_pretty = json.dumps(place, indent=2)
print(json_pretty)
```

Output:
```json
{
  "name": "Taipei 101",
  "coords": [
    25.033,
    121.5654
  ],
  "rating": 4.7,
  "is_open": true,
  "address": null
}
```

### Sorting Keys

```python
# Alphabetically sorted keys (useful for consistent output)
json_sorted = json.dumps(place, indent=2, sort_keys=True)
print(json_sorted)
```

Output:
```json
{
  "address": null,
  "coords": [25.033, 121.5654],
  "is_open": true,
  "name": "Taipei 101",
  "rating": 4.7
}
```

### Handling Non-ASCII Characters (Chinese, Japanese, etc.)

```python
place = {"name": "鼎泰豐", "city": "台北"}

# Default behavior: escape non-ASCII characters
print(json.dumps(place))
# {"name": "\u9f0e\u6cf0\u8c50", "city": "\u53f0\u5317"}

# Keep Chinese characters readable
print(json.dumps(place, ensure_ascii=False))
# {"name": "鼎泰豐", "city": "台北"}

# Recommended for files with Asian text:
json.dumps(place, indent=2, ensure_ascii=False)
```

### Compact Output (for APIs/network)

```python
# Remove unnecessary whitespace
compact = json.dumps(place, separators=(",", ":"))
print(compact)
# {"name":"Taipei 101","coords":[25.033,121.5654],"rating":4.7}
```

### Parsing JSON String to Python: `json.loads()`

```python
import json

json_string = '{"name": "Taipei 101", "rating": 4.7, "is_open": true, "floors": null}'

# Parse JSON string to Python dict
place = json.loads(json_string)

print(place)
# {'name': 'Taipei 101', 'rating': 4.7, 'is_open': True, 'floors': None}

print(type(place))        # <class 'dict'>
print(place["name"])      # Taipei 101
print(place["is_open"])   # True (Python boolean, not string!)
print(place["floors"])    # None (Python None, not string!)
```

### Type Conversion During Parsing

```python
json_string = '{"count": 42, "price": 19.99, "active": true, "data": null}'
data = json.loads(json_string)

print(type(data["count"]))   # <class 'int'>
print(type(data["price"]))   # <class 'float'>
print(type(data["active"]))  # <class 'bool'>
print(type(data["data"]))    # <class 'NoneType'>
```

### Parsing JSON Arrays

```python
json_array = '[1, 2, 3, "four", true, null]'
python_list = json.loads(json_array)

print(python_list)       # [1, 2, 3, 'four', True, None]
print(type(python_list)) # <class 'list'>
```

### 🎯 Mini-Exercise 2: Practice Conversions

```python
import json

# Convert this Python dict to JSON and back
original = {
    "name": "Test Place",
    "coordinates": (25.0, 121.5),  # Note: tuple!
    "tags": ["food", "local"],
    "rating": 4.5,
    "is_verified": True
}

# TODO: Convert to JSON string
json_str = ___

# TODO: Parse back to Python
parsed = ___

# Question: What type is parsed["coordinates"]?
print(type(parsed["coordinates"]))  # ?
```

---

# ☕ Break (10 minutes)

---

# Hour 2: File Operations

## Part 4: Reading and Writing Files (30 minutes)

### Basic File Writing

```python
# Open a file for writing
file = open("hello.txt", "w")
file.write("Hello, World!")
file.close()  # Don't forget to close!
```

### The `with` Statement (Context Manager)

The `with` statement automatically closes the file, even if an error occurs:

```python
# Recommended approach
with open("hello.txt", "w") as file:
    file.write("Hello, World!")
    file.write("\nWelcome to Python!")
# File is automatically closed here

# Equivalent to:
file = open("hello.txt", "w")
try:
    file.write("Hello, World!")
finally:
    file.close()
```

### Why `with` is Better

```python
# Without 'with' - risky!
f = open("data.txt", "w")
f.write("Some data")
# If an error occurs here, file never closes!
1 / 0  # ZeroDivisionError
f.close()  # Never reached!

# With 'with' - safe!
with open("data.txt", "w") as f:
    f.write("Some data")
    1 / 0  # Error occurs
# File is STILL closed properly!
```

### File Modes Explained

| Mode | Name | Description | File Must Exist? |
|------|------|-------------|------------------|
| `"r"` | Read | Read only (default) | Yes |
| `"w"` | Write | Write only, **overwrites** existing | No (creates) |
| `"a"` | Append | Write to end of file | No (creates) |
| `"x"` | Exclusive | Create new, fail if exists | No |
| `"r+"` | Read/Write | Both read and write | Yes |
| `"w+"` | Write/Read | Write and read, **overwrites** | No (creates) |

```python
# Read mode - file must exist
with open("existing.txt", "r") as f:
    content = f.read()

# Write mode - creates or OVERWRITES
with open("output.txt", "w") as f:
    f.write("This replaces everything!")

# Append mode - adds to end
with open("log.txt", "a") as f:
    f.write("New log entry\n")

# Exclusive mode - fails if file exists
with open("new_file.txt", "x") as f:
    f.write("Created new file!")
```

### ⚠️ Common Mistake: Write Mode Destroys Data!

```python
# DANGER! This destroys the original content!
with open("important_data.txt", "w") as f:  # "w" = overwrite!
    f.write("Oops, everything is gone!")

# Use append mode to add without destroying
with open("important_data.txt", "a") as f:  # "a" = append
    f.write("\nNew content added safely")
```

### Specifying Encoding (IMPORTANT!)

Different operating systems use different default encodings. Always specify UTF-8:

```python
# ❌ Bad - may fail with non-ASCII characters
with open("places.txt", "r") as f:
    content = f.read()

# ✅ Good - always works
with open("places.txt", "r", encoding="utf-8") as f:
    content = f.read()

# ✅ Also good for writing
with open("places.txt", "w", encoding="utf-8") as f:
    f.write("台北101")
```

### Reading Files: Different Methods

```python
# Method 1: Read entire file as one string
with open("story.txt", "r", encoding="utf-8") as f:
    content = f.read()
    print(content)  # Entire file as one string

# Method 2: Read all lines as a list
with open("story.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()
    print(lines)  # ['Line 1\n', 'Line 2\n', 'Line 3\n']

# Method 3: Read line by line (memory efficient for large files)
with open("story.txt", "r", encoding="utf-8") as f:
    for line in f:
        print(line.strip())  # Remove \n

# Method 4: Read specific number of characters
with open("story.txt", "r", encoding="utf-8") as f:
    first_100_chars = f.read(100)
```

### Writing Files: Different Methods

```python
# Method 1: Write a string
with open("output.txt", "w", encoding="utf-8") as f:
    f.write("Hello, World!\n")
    f.write("Second line\n")

# Method 2: Write multiple lines at once
lines = ["Line 1\n", "Line 2\n", "Line 3\n"]
with open("output.txt", "w", encoding="utf-8") as f:
    f.writelines(lines)

# Method 3: Use print() with file parameter
with open("output.txt", "w", encoding="utf-8") as f:
    print("Hello, World!", file=f)
    print("Second line", file=f)
```

### 🎯 Mini-Exercise 3: File Operations

```python
# Create a file with your top 5 favorite places (one per line)
places = ["Taipei 101", "Din Tai Fung", "Shilin Market", "Elephant Mountain", "Jiufen"]

# TODO: Write to file
with open("favorites.txt", "___", encoding="utf-8") as f:
    for place in places:
        f.write(___ + "\n")

# TODO: Read back and print
with open("favorites.txt", "___", encoding="utf-8") as f:
    for line in f:
        print(line.___)  # Remove newline
```

---

## Part 5: File Paths and `pathlib` (20 minutes)

### Understanding File Paths

```python
# Relative paths (relative to current directory)
"data.txt"           # Same folder
"data/places.json"   # Subfolder
"../data.txt"        # Parent folder

# Absolute paths
"/home/user/data.txt"           # Linux/Mac
"C:\\Users\\User\\data.txt"     # Windows
"C:/Users/User/data.txt"        # Windows (forward slashes work too)
```

### The Problem with Manual Paths

```python
# This breaks on Windows!
path = "data/places/" + filename  # Uses forward slash

# This breaks on Linux/Mac!
path = "data\\places\\" + filename  # Uses backslash

# Concatenation is error-prone
path = folder + "/" + subfolder + "/" + filename  # Messy!
```

### The `os.path` Module (Traditional)

```python
import os

# Join paths safely (handles OS differences)
path = os.path.join("data", "places", "taipei.json")
# Windows: data\places\taipei.json
# Linux/Mac: data/places/taipei.json

# Check if file exists
if os.path.exists("places.json"):
    print("File exists!")

# Get file name from path
os.path.basename("/home/user/data/places.json")  # "places.json"

# Get directory from path
os.path.dirname("/home/user/data/places.json")   # "/home/user/data"

# Check if it's a file or directory
os.path.isfile("places.json")  # True/False
os.path.isdir("data")          # True/False
```

### The `pathlib` Module (Modern - Python 3.4+)

```python
from pathlib import Path

# Create a path object
data_dir = Path("data")
places_file = Path("data/places.json")

# Join paths with /
config = Path("data") / "config" / "settings.json"
print(config)  # data/config/settings.json

# Check if exists
if places_file.exists():
    print("File exists!")

# Get parts of the path
print(places_file.name)      # places.json
print(places_file.stem)      # places
print(places_file.suffix)    # .json
print(places_file.parent)    # data

# Read and write directly
content = places_file.read_text(encoding="utf-8")
places_file.write_text("new content", encoding="utf-8")

# List files in directory
for file in Path("data").glob("*.json"):
    print(file)
```

### Creating Directories

```python
from pathlib import Path

# Create a directory
Path("output").mkdir(exist_ok=True)  # No error if exists

# Create nested directories
Path("output/data/2024").mkdir(parents=True, exist_ok=True)

# Using os module
import os
os.makedirs("output/data/2024", exist_ok=True)
```

### Working with the Data Directory

```python
from pathlib import Path

# Get the script's directory
script_dir = Path(__file__).parent

# Data directory relative to script
data_dir = script_dir / "data"

# Ensure data directory exists
data_dir.mkdir(exist_ok=True)

# Create file path
places_file = data_dir / "places.json"

# Use in file operations
with open(places_file, "r", encoding="utf-8") as f:
    data = json.load(f)
```

---

## Part 6: JSON File Operations (20 minutes)

### Writing JSON to File: `json.dump()`

```python
import json

places = [
    {"name": "Taipei 101", "coords": [25.0330, 121.5654], "rating": 4.7},
    {"name": "Din Tai Fung", "coords": [25.0339, 121.5645], "rating": 4.9},
    {"name": "Shilin Market", "coords": [25.0878, 121.5241], "rating": 4.5},
]

# Write to file (note: dump, not dumps!)
with open("places.json", "w", encoding="utf-8") as f:
    json.dump(places, f, indent=2, ensure_ascii=False)

print("Saved places.json!")
```

### Reading JSON from File: `json.load()`

```python
import json

# Read from file (note: load, not loads!)
with open("places.json", "r", encoding="utf-8") as f:
    places = json.load(f)

print(f"Loaded {len(places)} places")
for place in places:
    print(f"  - {place['name']}: {place['rating']}★")
```

### Complete Save/Load Helper Functions

```python
import json
from pathlib import Path

def save_json(data, filename):
    """
    Save data to a JSON file.

    Args:
        data: Python object to save (dict, list, etc.)
        filename: Path to save to (string or Path)
    """
    path = Path(filename)

    # Create parent directories if needed
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"✓ Saved to {path}")


def load_json(filename, default=None):
    """
    Load data from a JSON file.

    Args:
        filename: Path to load from
        default: Value to return if file doesn't exist

    Returns:
        Parsed JSON data, or default if file not found
    """
    path = Path(filename)

    if not path.exists():
        print(f"⚠ File not found: {path}")
        return default if default is not None else {}

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    print(f"✓ Loaded from {path}")
    return data


# Usage
places = [
    {"name": "Taipei 101", "rating": 4.7},
    {"name": "Din Tai Fung", "rating": 4.9},
]

save_json(places, "data/places.json")
loaded = load_json("data/places.json", default=[])
```

### 🎯 Mini-Exercise 4: Save and Load

```python
import json

# Create a dictionary of your personal settings
my_settings = {
    "username": "student",
    "theme": "dark",
    "language": "zh-TW",
    "favorite_places": ["Taipei 101", "Din Tai Fung"],
    "max_results": 10
}

# TODO: Save to settings.json


# TODO: Load and print
```

---

# ☕ Break (10 minutes)

---

# Hour 3: Error Handling and Building a Database

## Part 7: Error Handling (25 minutes)

### Why Handle Errors?

Without error handling, your program crashes:

```python
# This crashes if file doesn't exist!
with open("nonexistent.json", "r") as f:
    data = json.load(f)
# FileNotFoundError: [Errno 2] No such file or directory: 'nonexistent.json'
```

### Common File-Related Errors

| Error | Cause | Example |
|-------|-------|---------|
| `FileNotFoundError` | File doesn't exist | Opening non-existent file for reading |
| `PermissionError` | No permission | Writing to system files |
| `IsADirectoryError` | Path is a directory | Opening a folder as a file |
| `json.JSONDecodeError` | Invalid JSON | Parsing malformed JSON |
| `UnicodeDecodeError` | Encoding mismatch | Wrong encoding specified |

### The `try`/`except` Pattern

```python
try:
    # Code that might fail
    with open("data.json", "r") as f:
        data = json.load(f)
except FileNotFoundError:
    # Handle missing file
    print("File not found!")
    data = []
```

### Handling Multiple Error Types

```python
import json

def load_data(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)

    except FileNotFoundError:
        print(f"❌ File not found: {filename}")
        return None

    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in {filename}: {e}")
        return None

    except PermissionError:
        print(f"❌ Permission denied: {filename}")
        return None

    except Exception as e:
        # Catch-all for unexpected errors
        print(f"❌ Unexpected error: {e}")
        return None
```

### The `else` and `finally` Clauses

```python
try:
    with open("data.json", "r") as f:
        data = json.load(f)
except FileNotFoundError:
    print("File not found")
    data = []
else:
    # Runs only if NO exception occurred
    print(f"Successfully loaded {len(data)} items")
finally:
    # ALWAYS runs, whether exception or not
    print("Operation complete")
```

### Checking Before Opening

```python
from pathlib import Path

def load_safe(filename):
    path = Path(filename)

    # Check if file exists
    if not path.exists():
        print(f"Creating new file: {filename}")
        return []

    # Check if it's actually a file
    if not path.is_file():
        print(f"Error: {filename} is not a file")
        return []

    # Now safe to open
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
```

### Validating JSON Data

```python
def validate_place(place):
    """Check if a place dictionary has required fields."""
    required = ["name", "coords", "rating"]
    errors = []

    for field in required:
        if field not in place:
            errors.append(f"Missing field: {field}")

    if "coords" in place:
        if not isinstance(place["coords"], (list, tuple)):
            errors.append("coords must be a list")
        elif len(place["coords"]) != 2:
            errors.append("coords must have 2 elements")

    if "rating" in place:
        if not isinstance(place["rating"], (int, float)):
            errors.append("rating must be a number")
        elif not 0 <= place["rating"] <= 5:
            errors.append("rating must be between 0 and 5")

    return errors


# Usage
place = {"name": "Test", "rating": 6.0}  # Invalid rating
errors = validate_place(place)
if errors:
    print("Validation errors:", errors)
```

### 🎯 Mini-Exercise 5: Error Handling

```python
import json

def safe_load_json(filename):
    """
    Safely load a JSON file.
    Returns empty dict if any error occurs.
    """
    # TODO: Implement with try/except
    pass

# Test with different files
print(safe_load_json("places.json"))        # Should work
print(safe_load_json("nonexistent.json"))   # Should return {}
print(safe_load_json("invalid.json"))       # Should return {}
```

---

## Part 8: Debugging JSON Issues (15 minutes)

### Common JSON Errors and Solutions

#### Error 1: Trailing Comma

```python
# This JSON is INVALID
bad_json = '{"name": "test", "value": 42,}'  # Trailing comma!

# Fix: Remove trailing comma
good_json = '{"name": "test", "value": 42}'
```

#### Error 2: Single Quotes

```python
# This is INVALID JSON
bad_json = "{'name': 'test'}"  # Single quotes!

# Fix: Use double quotes
good_json = '{"name": "test"}'
```

#### Error 3: Unescaped Special Characters

```python
# This is INVALID
bad_json = '{"path": "C:\new\folder"}'  # \n is newline!

# Fix: Escape backslashes or use raw string
good_json = '{"path": "C:\\\\new\\\\folder"}'
```

#### Error 4: Missing Quotes on Keys

```python
# This is INVALID
bad_json = '{name: "test"}'  # Key not quoted!

# Fix: Quote the key
good_json = '{"name": "test"}'
```

### Debugging with json.JSONDecodeError

```python
import json

bad_json = '{"name": "test", "value": 42,}'

try:
    data = json.loads(bad_json)
except json.JSONDecodeError as e:
    print(f"Error: {e.msg}")
    print(f"Line: {e.lineno}, Column: {e.colno}")
    print(f"Position: {e.pos}")

# Output:
# Error: Expecting property name enclosed in double quotes
# Line: 1, Column: 29
# Position: 28
```

### Online JSON Validators

When debugging JSON, use online tools:
- [JSONLint](https://jsonlint.com/)
- [JSON Formatter](https://jsonformatter.curiousconcept.com/)

### Pretty Print for Debugging

```python
import json

data = {"nested": {"deep": {"value": [1, 2, 3]}}}

# Hard to read
print(data)
# {'nested': {'deep': {'value': [1, 2, 3]}}}

# Easy to read
print(json.dumps(data, indent=2))
# {
#   "nested": {
#     "deep": {
#       "value": [1, 2, 3]
#     }
#   }
# }
```

---

## Part 9: Building a Complete Place Database (30 minutes)

### Database Design

```python
"""
PlaceDatabase: A JSON-based database for storing places.

Features:
- Add, find, update, delete places (CRUD)
- Search by category, rating
- Automatic saving to file
- Error handling and validation
"""
```

### Complete Implementation

```python
import json
import os
from pathlib import Path
from datetime import datetime


class PlaceDatabase:
    """A JSON-based place database with full CRUD operations."""

    def __init__(self, filename="places_db.json"):
        """
        Initialize the database.

        Args:
            filename: Path to the JSON file
        """
        self.filename = Path(filename)
        self.places = self._load()
        print(f"📂 Database initialized: {len(self.places)} places")

    def _load(self):
        """Load places from file."""
        if not self.filename.exists():
            return []

        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                data = json.load(f)
                # Handle both list and dict formats
                if isinstance(data, dict) and "places" in data:
                    return data["places"]
                return data if isinstance(data, list) else []
        except json.JSONDecodeError as e:
            print(f"⚠️ Warning: Invalid JSON, starting fresh. Error: {e}")
            return []
        except Exception as e:
            print(f"⚠️ Warning: Could not load file. Error: {e}")
            return []

    def _save(self):
        """Save places to file with metadata."""
        # Create parent directories if needed
        self.filename.parent.mkdir(parents=True, exist_ok=True)

        data = {
            "meta": {
                "last_updated": datetime.now().isoformat(),
                "count": len(self.places)
            },
            "places": self.places
        }

        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def _validate(self, place):
        """Validate a place dictionary."""
        errors = []

        if "name" not in place or not place["name"]:
            errors.append("name is required")

        if "coords" in place:
            coords = place["coords"]
            if not isinstance(coords, (list, tuple)) or len(coords) != 2:
                errors.append("coords must be [lat, lon]")

        if "rating" in place:
            rating = place["rating"]
            if not isinstance(rating, (int, float)) or not 0 <= rating <= 5:
                errors.append("rating must be 0-5")

        return errors

    def add(self, place):
        """
        Add a new place to the database.

        Args:
            place: Dictionary with place data

        Returns:
            True if added, False if validation failed
        """
        errors = self._validate(place)
        if errors:
            print(f"❌ Validation failed: {errors}")
            return False

        # Add timestamp
        place["added_at"] = datetime.now().isoformat()

        self.places.append(place)
        self._save()
        print(f"✅ Added: {place.get('name', 'Unknown')}")
        return True

    def find_by_name(self, name):
        """Find a place by exact name match."""
        for place in self.places:
            if place.get("name") == name:
                return place
        return None

    def search(self, query):
        """Search places by name (partial match, case-insensitive)."""
        query_lower = query.lower()
        return [p for p in self.places if query_lower in p.get("name", "").lower()]

    def filter(self, category=None, min_rating=None, max_results=None):
        """
        Filter places by criteria.

        Args:
            category: Filter by category
            min_rating: Minimum rating
            max_results: Maximum number of results

        Returns:
            List of matching places
        """
        results = self.places

        if category:
            results = [p for p in results if p.get("category") == category]

        if min_rating is not None:
            results = [p for p in results if p.get("rating", 0) >= min_rating]

        # Sort by rating (highest first)
        results = sorted(results, key=lambda p: p.get("rating", 0), reverse=True)

        if max_results:
            results = results[:max_results]

        return results

    def update(self, name, updates):
        """
        Update a place by name.

        Args:
            name: Name of place to update
            updates: Dictionary of fields to update

        Returns:
            True if updated, False if not found
        """
        place = self.find_by_name(name)
        if not place:
            print(f"❌ Place not found: {name}")
            return False

        # Validate updates
        test_place = {**place, **updates}
        errors = self._validate(test_place)
        if errors:
            print(f"❌ Validation failed: {errors}")
            return False

        place.update(updates)
        place["updated_at"] = datetime.now().isoformat()
        self._save()
        print(f"✅ Updated: {name}")
        return True

    def delete(self, name):
        """
        Delete a place by name.

        Args:
            name: Name of place to delete

        Returns:
            True if deleted, False if not found
        """
        original_count = len(self.places)
        self.places = [p for p in self.places if p.get("name") != name]

        if len(self.places) < original_count:
            self._save()
            print(f"✅ Deleted: {name}")
            return True
        else:
            print(f"❌ Place not found: {name}")
            return False

    def all(self):
        """Get all places."""
        return self.places

    def count(self):
        """Get the number of places."""
        return len(self.places)

    def stats(self):
        """Get database statistics."""
        if not self.places:
            return {"count": 0}

        ratings = [p.get("rating", 0) for p in self.places if "rating" in p]
        categories = {}
        for p in self.places:
            cat = p.get("category", "uncategorized")
            categories[cat] = categories.get(cat, 0) + 1

        return {
            "count": len(self.places),
            "avg_rating": sum(ratings) / len(ratings) if ratings else 0,
            "categories": categories
        }

    def export(self, filename):
        """Export places to a different file."""
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.places, f, indent=2, ensure_ascii=False)
        print(f"✅ Exported {len(self.places)} places to {filename}")

    def __repr__(self):
        return f"PlaceDatabase({self.filename}, {len(self.places)} places)"
```

### Using the Database

```python
# Create database
db = PlaceDatabase("my_places.json")

# Add places
db.add({
    "name": "Taipei 101",
    "coords": [25.0330, 121.5654],
    "rating": 4.7,
    "category": "landmark"
})

db.add({
    "name": "Din Tai Fung",
    "coords": [25.0339, 121.5645],
    "rating": 4.9,
    "category": "restaurant"
})

db.add({
    "name": "Shilin Night Market",
    "coords": [25.0878, 121.5241],
    "rating": 4.5,
    "category": "market"
})

# Search
print("\n🔍 Search 'taipei':")
for p in db.search("taipei"):
    print(f"  - {p['name']}")

# Filter
print("\n⭐ Top rated (>= 4.6):")
for p in db.filter(min_rating=4.6):
    print(f"  - {p['name']}: {p['rating']}★")

# Statistics
print("\n📊 Stats:", db.stats())

# Update
db.update("Taipei 101", {"rating": 4.8, "visits": 1000})

# The data persists!
# Close program, run again, data is still there
```

---

## Part 10: Best Practices Summary (10 minutes)

### 1. Always Use UTF-8 Encoding

```python
# ✅ Good
with open("file.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# ❌ Bad
with open("file.json", "r") as f:  # May fail with non-ASCII
    data = json.load(f)
```

### 2. Use `with` Statement for Files

```python
# ✅ Good - auto-closes file
with open("file.json", "r") as f:
    data = json.load(f)

# ❌ Bad - may leave file open
f = open("file.json", "r")
data = json.load(f)
# f.close()  # Easy to forget!
```

### 3. Handle Errors Gracefully

```python
# ✅ Good - handles errors
def load_config(filename):
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}  # Return default

# ❌ Bad - crashes on error
def load_config(filename):
    with open(filename, "r") as f:
        return json.load(f)
```

### 4. Use pathlib for File Paths

```python
# ✅ Good - works on all OS
from pathlib import Path
data_file = Path("data") / "places.json"

# ❌ Bad - may break on Windows
data_file = "data/places.json"
```

### 5. Pretty Print for Debugging

```python
# ✅ Good - readable for debugging
json.dump(data, f, indent=2, ensure_ascii=False)

# For production/APIs - compact
json.dump(data, f, separators=(",", ":"))
```

### 6. Validate Before Saving

```python
# ✅ Good - validate data
def save_place(place):
    if "name" not in place:
        raise ValueError("name is required")
    # ... save

# ❌ Bad - save anything
def save_place(place):
    # Just save, no validation
    pass
```

---

## Summary

| Concept | Function/Pattern | Example |
|---------|------------------|---------|
| Python → JSON string | `json.dumps()` | `json.dumps({"a": 1}, indent=2)` |
| JSON string → Python | `json.loads()` | `json.loads('{"a": 1}')` |
| Python → JSON file | `json.dump()` | `json.dump(data, f, indent=2)` |
| JSON file → Python | `json.load()` | `data = json.load(f)` |
| Open file safely | `with open()` | `with open("f.json", "r") as f:` |
| Handle errors | `try/except` | `except FileNotFoundError:` |
| File paths | `pathlib.Path` | `Path("data") / "file.json"` |

---

## What's Next?

In **Week 4**, we'll use our JSON skills to:
- Make HTTP requests to web APIs
- Parse JSON responses from the Nominatim geocoding API
- Build a command-line geocoding tool
- Save API results to files for caching

---

## Homework

1. Complete all lab exercises
2. Build a personal "favorites" database using the PlaceDatabase class
3. Add at least 10 places you'd like to visit
4. Implement a simple command-line interface:
   - `add` - Add a new place
   - `list` - List all places
   - `search` - Search by name
   - `delete` - Delete a place
