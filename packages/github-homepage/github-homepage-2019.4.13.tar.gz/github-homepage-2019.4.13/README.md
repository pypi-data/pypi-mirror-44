<!--
https://pypi.org/project/readme-generator/
https://pypi.org/project/python-readme-generator/
-->

[![](https://img.shields.io/pypi/pyversions/github-homepage.svg?longCache=True)](https://pypi.org/project/github-homepage/)

#### Installation
```bash
$ [sudo] pip install github-homepage
```

#### Config
bash|python
-|-
`export GITHUB_TOKEN="your_github_token"`|`os.environ["GITHUB_TOKEN"]="your_github_token"`

#### Functions
function|`__doc__`
-|-
`github_homepage.get(fullname)` |return repo homepage
`github_homepage.update(fullname, url)` |update repo homepage

#### Executable modules
usage|`__doc__`
-|-
`python -m github_homepage fullname [url]` |get/set repo homepage

<p align="center">
    <a href="https://pypi.org/project/python-readme-generator/">python-readme-generator</a>
</p>