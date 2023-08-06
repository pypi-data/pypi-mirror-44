# enum

Python enum implementation

## Usage

```
>>> from enum import EnumBase
>>>
>>> class Color(EnumBase):
>>>     red = 1
>>>     green = 2
>>>     ...
>>> Color.red
1
>>> Color.get_value('red')
1
>>> Color.get_name(1)
'red'
```

## TODO

* Added setup.py
* Unittest
* CI
