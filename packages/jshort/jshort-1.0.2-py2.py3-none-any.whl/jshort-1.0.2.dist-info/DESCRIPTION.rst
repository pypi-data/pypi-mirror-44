# J

Python shorthand for json. inspired by [q](https://pypi.org/project/q/)

This package allows json load, dump from and to file with few code.

## Installation

```bash
pip install jshort
```

## Usage

```python
import j #This is an instance

# loads json from file, stores it in data property
h = j(input_path='/tmp/data.json')

# get data
h.data
#{"foo": "bar"}

# Display colored content
print(h)
# or
h.prt()

{
    "foo": "bar"
}

# The same, in short
j(i='/tmp/data.json').d
j(i='/tmp/data.json').prt()

# Write json
j(output_path='/tmp/data.json', data={"foo": "bar"})
# Also change print indnentation
h = j(o='/tmp/data.json', data={"hey": "jude"}, indent=2)
h.prt()

{
    "hey": "jude"
}

# Traversing json documents using https://pypi.org/project/jsonpath-ng/
j(d=my_dict).path('key')
# Shorter and with more filtering
j(d=my_dict).p('sub.*')
# Or with an array and from a file
j(i='/tmp/data.json').p('key[1]')

```

Enjoy.

Have a look at https://pypi.org/project/jsonpath-ng/ for more about json traversing


