<!--
https://pypi.org/project/readme-generator/
https://pypi.org/project/python-readme-generator/
-->

[![](https://img.shields.io/pypi/pyversions/jsfiddle-generator.svg?longCache=True)](https://pypi.org/project/jsfiddle-generator/)

#### Installation
```bash
$ [sudo] pip install jsfiddle-generator
```

#### How it works
```
.
├── demo.css
├── demo.details
├── demo.js
├── demo.html
```

#### Executable modules
usage|`__doc__`
-|-
`python -m jsfiddle_generator path ...` |generate jsfiddle files: `demo.css`, `demo.js`, `demo.html`, `demo.details`

#### Examples
create `demo.css`, `demo.js`, `demo.details` in every dir with `demo.html`:
```bash
$ find . -name "demo.html" -exec python -m jsfiddle_generator {} \;
```
---
create `demo.css`, `demo.js`, `demo.details`, `demo.html` in every empty dir:

`find . -not -path '*/\.*' -type d -links 2 -exec python -m jsfiddle_generator {} \;`

---
paths with spaces:

OS|speed|command
-|-|-
any|slow|`find ... -exec python -m jsfiddle_generator {} \;`
Linux|fast|`find ... -print0 \| xargs -d '\n' python -m jsfiddle_generator`
macOS|fast|`find ... -print0 \| xargs -0 python -m jsfiddle_generator`

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