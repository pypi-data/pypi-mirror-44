# python-rndua
[![PyPI version](https://badge.fury.io/py/rndua.svg)](https://badge.fury.io/py/rndua)

A python module that generate random user agent based on rules
## Why?
Most random user agent generator just randomly pick from a large list.
This one is based on rule and software version lists, generate user agent that seems legit but may not actually exist.
The goal is to generate user agent that seems as legit as possible but also keep code complexity low.
## Currently supported user agent types
* {Chrome, Firefox} on {Android, Windows, OS X}
## How it works?
Besides the source code, [data.md](data.md) may give you some hints.
## Basic usage
```python
from rndua.rndua import RandomUAGenerator
rg=RandomUAGenerator()
rg.get_random_user_agent()
```
## Advanced usage
See the source code, it's short.
