<!--
https://pypi.org/project/readme-generator/
https://pypi.org/project/python-readme-generator/
-->

[![](https://img.shields.io/badge/OS-Unix-blue.svg?longCache=True)]()

#### Installation
```bash
$ [sudo] pip install github-fullname
```

#### Scripts usage
```bash
usage: github-fullname path
```

#### Examples
```bash
$ cd path/to/repo
$ github-fullname .
owner/repo
```

```bash
$ find ~/git -type d -mindepth 1 -maxdepth 1 -exec github-fullname {} \;
owner/repo1
SKIP (~/git/repo2): .git NOT EXISTS
owner/repo3
...
```

hide errors
```bash
$ find ~/git -maxdepth 1 -exec github-fullname {} \; 2> /dev/null
owner/repo1
owner/repo3
...
```

show github orphaned repos:
```bash
$ python -m github_repos | grep -v "$(find ~/git -maxdepth 1 -exec github-fullname {} \; 2> /dev/null)"
```

delete github orphaned repos:
```bash
$ python -m github_repos | grep -v "$(find ~/git -maxdepth 1 -exec github-fullname {} \; 2> /dev/null)" | xargs python -m github_delete
```

<p align="center">
    <a href="https://pypi.org/project/python-readme-generator/">python-readme-generator</a>
</p>