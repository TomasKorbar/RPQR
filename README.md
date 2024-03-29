# RPQR (RPM Package Query Resolver) project
Author: Tomáš Korbař

## installation
First you need to install python3-dnf package, because the module can be
only installed through distribution package manager.
And then install scripts
```
$ pip install .
```
## usage
Proof of concept can be executed after installation by:

```
$ RPQROrphaned
```

Program prints out packages that are orphaned in fedora rawhide and maintainers
which are affected by this (maintain either the same package or package which depends on it).

More general tool is RPQR script, which uses the RPQR module.
First you need to provide configuration in the following format:
```
[RPQR]
pluginDirectories=["./rpqr/loader/plugins/implementations"]
cache=/var/tmp/rpqr.json

[RPQRRepo_f34-repo]
url=http://ftp.fi.muni.cz/pub/linux/fedora/linux/releases/34/Everything/x86_64/os/

[RPQRMaintainerPlugin]
url=https://src.fedoraproject.org/extras/pagure_owner_alias.json
```

Then you can execute your queries through CLI interface and get visualized results.
```
$ RPQR --cfgpath example.conf "NAMELIKE('libyang')" --visualize --filterattributes "name"
```
