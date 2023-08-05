<!--
https://pypi.org/project/readme-generator/
-->

[![](https://img.shields.io/pypi/pyversions/markdown-lists.svg?longCache=True)](https://pypi.org/project/markdown-lists/)

#### Installation
```bash
$ [sudo] pip install markdown-lists
```

#### Functions
function|`__doc__`
-|-
`markdown_lists.render(lists, depth=1)` |return a string with markdown nested lists

#### Examples
```python
>>> import markdown_lists

>>> lists = ["item1",["subitem11","subitem12"],"item2"]
>>> markdown_lists.render(lists)
+   item1
    +   subitem11
    +   subitem12
+   item2
```

<p align="center">
    <a href="https://pypi.org/project/readme-generator/">readme-generator</a>
</p>