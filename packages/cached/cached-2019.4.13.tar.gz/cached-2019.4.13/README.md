<!--
https://pypi.org/project/readme-generator/
https://pypi.org/project/python-readme-generator/
-->

[![](https://img.shields.io/pypi/pyversions/cached.svg?longCache=True)](https://pypi.org/project/cached/)

#### Installation
```bash
$ [sudo] pip install cached
```

#### Functions
function|`__doc__`
-|-
`cached.cached(function)` |`@cache` decorator, `cache(function)` - cache function result

#### Examples
`@cached` decorator

```python
>>> from cached import cached

>>> @cached
    def func(*args, **kwags):
```

`cached(function)` function
```python
>>> from cached import cached

>>> def func(*args, **kwags):
        ...
>>> cached(func)()
```

<p align="center">
    <a href="https://pypi.org/project/python-readme-generator/">python-readme-generator</a>
</p>