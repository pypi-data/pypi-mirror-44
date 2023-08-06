# Print Extended

Extended functionalists and better control over Python's built-in print function

[![PyPI version](https://badge.fury.io/py/print-extended.svg)](https://badge.fury.io/py/print-extended)
[![Build Status](https://travis-ci.com/arrrlo/print-extended.svg?branch=master)](https://travis-ci.com/arrrlo/print-extended)

![GitHub issues](https://img.shields.io/github/issues/arrrlo/print-extended.svg)
![GitHub closed issues](https://img.shields.io/github/issues-closed/arrrlo/print-extended.svg)
![GitHub closed pull requests](https://img.shields.io/github/issues-pr-closed/arrrlo/print-extended.svg)

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/Marine-Traffic-API.svg)
![GitHub](https://img.shields.io/github/license/arrrlo/print-extended.svg?color=blue)
![GitHub last commit](https://img.shields.io/github/last-commit/arrrlo/print-extended.svg?color=blue)

## Installation

```bash
> pip install print-extended
```

# Usage

If you run Python interpreter with `-O` flag print will be disabled (watches for __debug__):

```bash
python -O

>>> import print_extended
>>> print('foo')
>>>
```

Runing it without `-O` flag works normal:

```bash
python

>>> import print_extended
>>> print('foo')
foo
>>>
```

Control your print with `PrintControl` class:

```python
import print_extended
from print_extended import PrintControl

PrintControl.template = '--> {print} <--'
PrintControl.fg_color = 'green'
PrintControl.bg_color = 'blue'
```

![PrintControl](docs/images/terminal.png)

Change underlying print function:

```python
import print_extended
from pprint import pprint
from print_extended import PrintControl

PrintControl.print_function = pprint

print({...}) # will print it using pprint
```

Disable and enable printing

```python
import print_extended
from print_extended import PrintControl

PrintControl.disable() # print(...) now does nothing

PrintControl.enable() # print(...) now prints
```
