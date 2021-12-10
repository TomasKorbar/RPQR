import dnf
import sqlite3
import os
import importlib
import sys

from plugins.library import RPQRBasePlugin

class Loader:
    def __init__(self, repositories: list):
        self.repositories = repositories
        self.plugins = []

    def createDatabase(self) -> bool:
        sqlConnection = sqlite3.connect("temp.db")
        self._createDatabaseLayout(sqlConnection)
        base = dnf.Base()
        for (name, url) in self.repositories:
            base.repos.add_new_repo(name, base.conf, baseurl=[url])
        base.fill_sack(load_system_repo=False, load_available_repos=True)
        q_avail = base.sack.query().available().run()
        sys.path.append("/home/tkorbar/development/rpqr/rpqr/loader/plugins/implementations")
        pluginModules = os.listdir("/home/tkorbar/development/rpqr/rpqr/loader/plugins/implementations")

        for file in pluginModules:
            moduleName = file[:-3]
            if moduleName.startswith("_"):
                continue
            module = importlib.import_module(moduleName)
            pluginClass : RPQRBasePlugin = getattr(module, moduleName)
            pluginInstance = pluginClass(sqlConnection)
            self.plugins.append(pluginInstance)

        for pkg in q_avail:
            res = sqlConnection.execute("INSERT INTO PACKAGES DEFAULT VALUES")
            for pluginInstance in self.plugins:
                pluginInstance: RPQRBasePlugin
                pluginInstance.fillData(res.lastrowid, pkg)
        sqlConnection.commit()
        sqlConnection.close()

    def _createDatabaseLayout(self, connection: sqlite3.Connection) -> bool:
        connection.execute("CREATE TABLE PACKAGES (ID INTEGER NOT NULL PRIMARY KEY)")
        connection.commit()

if __name__ == "__main__":
    loader = Loader(
        [("local-repo", "http://download.eng.brq.redhat.com/composes/finished-rhel-8/RHEL-8/latest-RHEL-8.5/compose/AppStream/x86_64/os/")])
    loader.createDatabase()
