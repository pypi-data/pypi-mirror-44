# Jshort

Python shorthand for json. inspired by [q](https://pypi.org/project/q/)

This package allows json load, dump from and to file with few code.

## Installation

```bash
pip install jshort
```

## Usage

```python
# This is an instance
import j 

# Loads json from file, stores it in data property
h = j(input_path='/tmp/data.json')

# Get data
h.data
#{
#   "foo": "bar"
#}

# Display colored content
print(h)
# or
h.prt()
# {
#     "oh": "dayum!"
# }

# The same, in short
# For data
j(i='/tmp/data.json').d
# Print
j(i='/tmp/data.json').prt()

# Write json
j(output_path='/tmp/out.json', data={"foo": "bar"})

# Also write data in a shorter way and change print content setting indentation to 2
j(o='/tmp/out.json', d={"hey": "jude"}, indent=2).prt()
# {
#   "hey": "jude"
# }

# Traversing json documents using https://pypi.org/project/jsonpath-ng/
j(d=my_dict).path('key')

# Shorter and with more filtering
j(d=my_dict).p('sub.*')

# Or fintering on an array and from a file
j(i='/tmp/data.json').p('key[1]')
```

Have a look at https://pypi.org/project/jsonpath-ng/ for more about json traversing.

If only one result is returned from filtering, the path method returns only the result otherwise it is a list of results.

Enjoy.
