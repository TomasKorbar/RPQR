import dnf
import os
import importlib
import sys

from plugins.library import RPQRBasePlugin
import networkx

from rpqr.loader.plugins.library.RPQRDataPlugin import RPQRDataPlugin
from rpqr.loader.plugins.library.RPQRRelationPlugin import RPQRRelationPlugin

class Loader:
    def __init__(self, repositories: list, pluginDirs: list):
        self.repositories = repositories
        self.pluginDirectories = pluginDirs
        self.plugins = []

    def createDatabase(self) -> bool:
        graph = networkx.MultiGraph()
        base = dnf.Base()
        for (name, url) in self.repositories:
            base.repos.add_new_repo(name, base.conf, baseurl=[url])
        base.fill_sack(load_system_repo=False, load_available_repos=True)
        q_avail = base.sack.query().available().run()
        self._initializePlugins()
        dataPlugins = [plugin for plugin in self.plugins if isinstance(plugin, RPQRDataPlugin)]
        relationPlugins = [plugin for plugin in self.plugins if isinstance(plugin, RPQRRelationPlugin)]
        av_query = base.sack.query().available()
        id = 0
        for pkg in q_avail:
            graph.add_node(id)
            for pluginInstance in dataPlugins:
                pluginInstance: RPQRDataPlugin
                pluginInstance.fillData(id , pkg, graph)
            id += 1
        
        id = 0
        for pkg in q_avail:
            for pluginInstance in relationPlugins:
                pluginInstance : RPQRRelationPlugin
                pluginInstance.fillData(id, pkg, graph, av_query)
            id += 1
        

    def _initializePlugins(self):
        for dir in self.pluginDirectories:
            sys.path.append(dir)
            pluginModules = os.listdir(dir)

        for file in pluginModules:
            moduleName = file[:-3]
            if moduleName.startswith("_"):
                continue
            module = importlib.import_module(moduleName)
            pluginClass: RPQRBasePlugin = getattr(module, moduleName)
            pluginInstance = pluginClass()
            self.plugins.append(pluginInstance)

if __name__ == "__main__":
    loader = Loader(
        [("remote-repo", "http://ftp.fi.muni.cz/pub/linux/fedora/linux/releases/33/Everything/x86_64/os/")], ["/home/tkorbar/development/rpqr/rpqr/loader/plugins/implementations"])
    loader.createDatabase()
