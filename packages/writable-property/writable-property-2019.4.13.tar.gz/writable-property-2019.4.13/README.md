<!--
https://pypi.org/project/readme-generator/
https://pypi.org/project/python-readme-generator/
-->

[![](https://img.shields.io/pypi/pyversions/writable-property.svg?longCache=True)](https://pypi.org/project/writable-property/)

#### Installation
```bash
$ [sudo] pip install writable-property
```

#### Classes
class|`__doc__`
-|-
`writable_property.writable_property` |writable property class

#### Examples
```python
>>> from writable_property import writable_property

>>> class Class:
    @writable_property
    def prop(self):
        return "value"

>>> obj = Class()
>>> obj.prop
"value"

>>> obj.prop = "new"
>>> obj.prop
"new"
```

<p align="center">
    <a href="https://pypi.org/project/python-readme-generator/">python-readme-generator</a>
</p>