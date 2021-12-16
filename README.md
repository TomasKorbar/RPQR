# RPQR (RPM Package Query Resolver) project
Author: Tomáš Korbař

## installation
First you need to install python3-dnf package, because the module can be
only installed through distribution package manager.
```
$ pip install .
```
## usage
Currently there is implemented only one proof of concept.

It can be executed after installation by:

```
$ RPQROrphaned "http://ftp.fi.muni.cz/pub/linux/fedora/linux/releases/33/Everything/x86_64/os/"
```

Program prints out packages that are orphaned in fedora 33 and maintainers
which are affected by this (maintain either the same package or package which depends on it).
