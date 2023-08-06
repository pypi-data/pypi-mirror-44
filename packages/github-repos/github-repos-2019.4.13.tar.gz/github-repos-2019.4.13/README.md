<!--
https://pypi.org/project/readme-generator/
https://pypi.org/project/python-readme-generator/
-->

[![](https://img.shields.io/pypi/pyversions/github-repos.svg?longCache=True)](https://pypi.org/project/github-repos/)

#### Installation
```bash
$ [sudo] pip install github-repos
```

#### Config
bash|python
-|-
`export GITHUB_TOKEN="your_github_token"`|`os.environ["GITHUB_TOKEN"]="your_github_token"`

#### Functions
function|`__doc__`
-|-
`github_repos.repos(login=None)` |return a list of user repos

#### Executable modules
usage|`__doc__`
-|-
`python -m github_repos [login]` |print user repos

#### Examples
delete orphaned repos (if basename = repo name)

```bash
$ cd ~/git/owner
$ python -m github_repos | awk -F '/' '{print $2}' | grep -v -iF "$(ls -1)" | xargs python -m github_delete
```

<p align="center">
    <a href="https://pypi.org/project/python-readme-generator/">python-readme-generator</a>
</p>