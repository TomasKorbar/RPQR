# RPQR (RPM Package Query Resolver) project
Author: Tomáš Korbař

## installation
First you need to install python3-dnf package, because the module can be
only installed through distribution package manager.
```
$ pip install .
```
## usage
Proof of concept can be executed after installation by:

```
$ RPQROrphaned "http://ftp.fi.muni.cz/pub/linux/fedora/linux/releases/33/Everything/x86_64/os/"
```

Program prints out packages that are orphaned in fedora 33 and maintainers
which are affected by this (maintain either the same package or package which depends on it).

More general tool is RPQR script, which uses the RPQR module.
First you need to provide configuration in the following format:
```
[RPQR]
pluginDirectories=["/bar/foo/pluginDirectory"]
repositories=["repo alias", "http://example.org/repo"]
```

Then you can execute your queries through CLI interface and get visualized results.
```
$ RPQR example.conf "NAMELIKE('libyang')"
```
