<!--
https://pypi.org/project/readme-generator/
https://pypi.org/project/python-readme-generator/
-->

[![](https://img.shields.io/pypi/pyversions/github-delete.svg?longCache=True)](https://pypi.org/project/github-delete/)

#### Installation
```bash
$ [sudo] pip install github-delete
```

#### Config
bash|python
-|-
`export GITHUB_TOKEN="your_github_token"`|`os.environ["GITHUB_TOKEN"]="your_github_token"`

#### Functions
function|`__doc__`
-|-
`github_delete.delete(fullname)` |delete github repo

#### Executable modules
usage|`__doc__`
-|-
`python -m github_delete name ...` |delete github repo(s)

#### Examples
```bash
$ python -m github_delete repo1 repo2
$ python -m github_delete my_org/repo1 my_org/repo2
```

<p align="center">
    <a href="https://pypi.org/project/python-readme-generator/">python-readme-generator</a>
</p>