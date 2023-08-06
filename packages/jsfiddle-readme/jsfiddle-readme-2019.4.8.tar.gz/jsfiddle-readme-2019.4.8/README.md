<!--
https://pypi.org/project/readme-generator/
https://pypi.org/project/python-readme-generator/
-->

[![](https://img.shields.io/pypi/pyversions/jsfiddle-readme.svg?longCache=True)](https://pypi.org/project/jsfiddle-readme/)

#### Installation
```bash
$ [sudo] pip install jsfiddle-readme
```

#### Classes
class|`__doc__`
-|-
`jsfiddle_readme.Readme` |README.md class. methods: `render`, `save(path)`

#### Executable modules
usage|`__doc__`
-|-
`python -m jsfiddle_readme path ...` |generate jsfiddle README.md

#### Examples
generate multiple README.md files
```bash
$ find . -name "demo.html" | xargs python -m jsfiddle_readme
```

#### Related projects
+   [`jsfiddle.py` - jsfiddle helper](https://pypi.org/project/jsfiddle/)
+   [`jsfiddle-build.py` - build html file from jsfiddle files](https://pypi.org/project/jsfiddle-build/)
+   [`jsfiddle-generator.py` - jsfiddle files generator](https://pypi.org/project/jsfiddle-generator/)
+   [`jsfiddle-readme.py` - generate jsfiddle `README.md`](https://pypi.org/project/jsfiddle-readme/)

#### Links
+   [Display fiddle from a Github repository](https://docs.jsfiddle.net/github-integration/untitled-1)

<p align="center">
    <a href="https://pypi.org/project/python-readme-generator/">python-readme-generator</a>
</p>