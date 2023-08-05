# dataclass_structor

[![Documentation Status](https://readthedocs.org/projects/dataclass-structor/badge/?version=latest)](https://dataclass-structor.readthedocs.io/en/latest/?badge=latest)
![PyPI - License](https://img.shields.io/pypi/v/dataclass_structor.svg)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/dataclass_structor.svg)
![PyPI - License](https://img.shields.io/pypi/l/dataclass_structor.svg)
[![Build Status](https://api.cirrus-ci.com/github/hockeybuggy/dataclass_structor.svg)](https://cirrus-ci.com/github/hockeybuggy/dataclass_structor)

A type aware structor/destructor for python value objects.


## Install

```shell
pip install dataclass_structor
```


## Documentation

The [docs for this project can be found here](dataclass-structor.readthedocs.io).


## Example

```python

import dataclasses
import typing

from dataclass_structor import structure, unstructure


@dataclasses.dataclass
class Invite:
    email: str
    guests: typing.List["Guest"]


@dataclasses.dataclass
class Guest:
    first_name: typing.Optional[str] = None


value_type = Invite(
    email="testing",
    guests=[
      Guest(first_name="John"),
      Guest(),
    ],
)

x = unstructure(value_type)
assert x == {"email": "", "guests": [{"first_name": "John"}, {"first_name": None}]}

assert structure(x, Invite) == value_type
```
