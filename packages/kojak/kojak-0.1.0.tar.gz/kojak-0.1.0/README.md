# kojak

[![Build Status](https://travis-ci.org/4383/kojak.svg?branch=devel)](https://travis-ci.org/4383/kojak)
![PyPI](https://img.shields.io/pypi/v/kojak.svg)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/kojak.svg)
![PyPI - Status](https://img.shields.io/pypi/status/kojak.svg)

Python projects analyzer

kojak is a development tools that help you to get informations
about a given python file and to get a big picture of this one
like all the module classes and all the module classes functions members.

kojak retrieve informations from python projects by using the python [abstract
tree syntax (AST)](https://docs.python.org/3/library/ast.html).

## Warning
Really young project with poor functionalities for now.

## Features
- Get class and methods
- Get function from python module

## Install or Update kojak

```sh
$ pip install -U kojak
```

## Usage

### Help and options

```shell
$ kojak <path to your python file>
Class1
    - method11
    - method12
    - method13
Class2
    - method21
    - method22
    - method23
```

## Future improvements
- add the possibility to do a recursive of the whole files of a given project
- inspect from the stdin
- add the possibility to scoping an object or a given method or function

## Contribute

If you want to contribute to kojak [please first read the contribution guidelines](CONTRIBUTING.md)

## Licence

This project is under the MIT License.

[See the license file for more details](LICENSE)
