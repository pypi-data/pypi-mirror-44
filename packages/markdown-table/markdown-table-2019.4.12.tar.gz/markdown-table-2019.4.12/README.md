<!--
https://pypi.org/project/readme-generator/
https://pypi.org/project/python-readme-generator/
-->

[![](https://img.shields.io/pypi/pyversions/markdown-table.svg?longCache=True)](https://pypi.org/project/markdown-table/)

#### Installation
```bash
$ [sudo] pip install markdown-table
```

#### Classes
class|`__doc__`
-|-
`markdown_table.Column` |attrs: `header`, `align` (`left`, `center`, `right`)
`markdown_table.Table` |attrs: `columns`, `matrix`. methods: `getheaders()`, `getseparators()`, `getmatrix()`, `render()`

#### Functions
function|`__doc__`
-|-
`markdown_table.render(headers, matrix)` |return a string with markdown table (one-line cells only)

<p align="center">
    <a href="https://pypi.org/project/python-readme-generator/">python-readme-generator</a>
</p>