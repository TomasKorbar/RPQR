# RPQR project
Author: Tomáš Korbař

## installation
```
$ pip install .
```
## usage
Currently there is implemented only one proof of concept.

It can be executed after installation by:

```
$ python3 -m rpqr.app.main
```

Program prints out packages that are orphaned in fedora 33 and maintainers
which are affected by this (maintain either the same package or package which depends on it).
