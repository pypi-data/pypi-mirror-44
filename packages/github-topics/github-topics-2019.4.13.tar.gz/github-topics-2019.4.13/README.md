<!--
https://pypi.org/project/readme-generator/
https://pypi.org/project/python-readme-generator/
-->

[![](https://img.shields.io/pypi/pyversions/github-topics.svg?longCache=True)](https://pypi.org/project/github-topics/)

#### Installation
```bash
$ [sudo] pip install github-topics
```

#### Config
bash|python
-|-
`export GITHUB_TOKEN="your_github_token"`|`os.environ["GITHUB_TOKEN"]="your_github_token"`

#### Functions
function|`__doc__`
-|-
`github_topics.replace(fullname, topics)` |replace repo topics

#### Executable modules
usage|`__doc__`
-|-
`python -m github_topics.add fullname topic ...` |add repo topics
`python -m github_topics.clear fullname` |remove all repo topics
`python -m github_topics.get fullname` |print repo topics
`python -m github_topics.remove fullname topic ...` |remove repo topics
`python -m github_topics.replace fullname topic ...` |set repo topics

<p align="center">
    <a href="https://pypi.org/project/python-readme-generator/">python-readme-generator</a>
</p>