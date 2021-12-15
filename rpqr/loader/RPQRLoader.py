'''
Project: RPQR
Author: Tomáš Korbař (tomas.korb@seznam.cz)
Copyright 2021 - 2021 Tomáš Korbař
'''

import dnf
import networkx
from rpqr.library import RPQRConfiguration

from rpqr.loader.plugins.library.RPQRDataPlugin import RPQRDataPlugin
from rpqr.loader.plugins.library.RPQRRelationPlugin import RPQRRelationPlugin


class RPQRLoader:
    def __init__(self, config : RPQRConfiguration):
        self.repositories = config.repositories
        self.plugins = config.plugins

    def createDatabase(self) -> networkx.MultiGraph:
        graph = networkx.MultiDiGraph()
        base = dnf.Base()
        for (name, url) in self.repositories:
            base.repos.add_new_repo(name, base.conf, baseurl=[url])
        base.fill_sack(load_system_repo=False, load_available_repos=True)
        q_avail = base.sack.query().available().run()
        dataPlugins = [plugin for plugin in self.plugins if isinstance(
            plugin, RPQRDataPlugin)]
        relationPlugins = [plugin for plugin in self.plugins if isinstance(
            plugin, RPQRRelationPlugin)]
        av_query = base.sack.query().available()
        id = 0
        for pkg in q_avail:
            graph.add_node(id)
            for pluginInstance in dataPlugins:
                pluginInstance: RPQRDataPlugin
                pluginInstance.fillData(id, pkg, graph)
            id += 1

        id = 0
        for pkg in q_avail:
            for pluginInstance in relationPlugins:
                pluginInstance: RPQRRelationPlugin
                pluginInstance.fillData(id, pkg, graph, av_query)
            id += 1
        return graph
