<!--
https://pypi.org/project/readme-generator/
https://pypi.org/project/python-readme-generator/
-->

[![](https://img.shields.io/pypi/pyversions/markdown-link-extractor.svg?longCache=True)](https://pypi.org/project/markdown-link-extractor/)

#### Installation
```bash
$ [sudo] pip install markdown-link-extractor
```

#### Functions
function|`__doc__`
-|-
`markdown_link_extractor.getlinks(string)` |return a list with markdown links

#### Executable modules
usage|`__doc__`
-|-
`python -m readme_links path ...` |extract links from markdown files

#### Examples
```bash
$ find -L . -name "README.md" | xargs python -m markdown_link_extractor
```

<p align="center">
    <a href="https://pypi.org/project/python-readme-generator/">python-readme-generator</a>
</p>