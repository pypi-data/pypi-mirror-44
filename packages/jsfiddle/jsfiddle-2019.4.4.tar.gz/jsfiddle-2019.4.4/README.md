<!--
https://pypi.org/project/readme-generator/
https://pypi.org/project/python-readme-generator/
-->

[![](https://img.shields.io/pypi/pyversions/jsfiddle.svg?longCache=True)](https://pypi.org/project/jsfiddle/)

#### Installation
```bash
$ [sudo] pip install jsfiddle
```

#### Functions
function|`__doc__`
-|-
`jsfiddle.github_tree()` |return `github_tree` string. git remote required
`jsfiddle.url()` |return `https://jsfiddle.net/gh/get/library/pure/{github_tree}/` string
`jsfiddle.details.load()` |return a dictorinary with `demo.details` data
`jsfiddle.details.save(data)` |save a dictionary to a `demo.details` file

#### Executable modules
usage|`__doc__`
-|-
`python -m jsfiddle.details.description path [value]` |get/set `demo.details` `description`
`python -m jsfiddle.details.name path [value]` |get/set `demo.details` `name`
`python -m jsfiddle.details.resources path [url ...]` |get/set `demo.details` `resources`

#### Examples
set `demo.details` `resources` urls
```bash
$ find . -name "demo.details" -exec python -m jsfiddle.details.resources {} https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css https://code.jquery.com/jquery-3.3.1.slim.min.js \;
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