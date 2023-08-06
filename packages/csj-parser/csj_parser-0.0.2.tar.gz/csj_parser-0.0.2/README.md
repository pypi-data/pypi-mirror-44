# CSJ Parser for Python

[![N|package](https://img.shields.io/pypi/v/csj-parser.svg)](https://pypi.python.org/pypi/csj-parser) [![Build Status](https://circleci.com/gh/panuwizzle/csj-parser.svg?style=svg)](https://circleci.com/gh/panuwizzle/csj-parser)

Comma Separated JSON (CSJ) is a CSV like file format designed for stream processing where each cell is valid JSON. This makes it very similar to CSV, but without the problems that CSV has.

For more information, please visit [https://kirit.com/Comma%20Separated%20JSON]

## Installation

CSJ Parser requires Python 3.5 or later to run.
CSJ Parser can be installed using pip:

```
$ pip install csj-parser
```
If you want the latest release, you can install from git:
```
$ pip install git+https://github.com/Proteus-tech/csj-parser.git
```

## Examples

Convert JSON to CSJ
```python
from csj_parser.csj import Csj

json_list = [
    {
        "key1" : "value1",
        "key2" : ["item1", "item2", "item3"],
        "key3" : {"key" : "value"}
    },
    {
        "key1" : 10,
        "key2" : None,
        "key3" : None
    }
]

# This function returns a string of data in CSJ format
def convert_json_to_csj(json_dict):
    csj_string = Csj.from_dicts(json_dict)
    return csj_string
    
convert_json_to_csj(json_list)
```
Output
```
"key1","key2","key3"
"value1",["item1","item2","item3"], {"key":"value"}
10,null,null
```
Convert CSJ to JSON
```python
from csj_parser.csj import Csj

csj_str = '''"key1","key2","key3"\n"value1","value2","value3"\n"value4","value5","value6"\n'''

# This function returns a dictionary of data in JSON format
def convert_csj_to_json(csj_string):
    json_dict = Csj.to_dict(csj_string)
    return json_dict
    
convert_csj_to_json(csj_str)
```
Output
```
[{'key1': 'value1', 'key2': 'value2', 'key3': 'value3'},{'key1': 'value4', 'key2': 'value5', 'key3': 'value6'}]
```

[//]: #

[https://kirit.com/Comma%20Separated%20JSON]: <https://kirit.com/Comma%20Separated%20JSON>
