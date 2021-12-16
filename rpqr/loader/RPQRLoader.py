'''
Project: RPQR
Author: Tomáš Korbař (tomas.korb@seznam.cz)
Copyright 2021 - 2021 Tomáš Korbař
'''

import dnf
import hawkey
import networkx

from rpqr.library import RPQRConfiguration
from rpqr.loader.plugins.library.RPQRDataPlugin import RPQRDataPlugin
from rpqr.loader.plugins.library.RPQRRelationPlugin import RPQRRelationPlugin


class RPQRLoader:
    """ Class handling loading of repositories and building graphs
    """
    def __init__(self, config : RPQRConfiguration) -> None:
        """ Create instance of RPQRLoader

        :param config: provided rpqr configuration
        :type config: RPQRConfiguration
        """
        self.repositories = config.repositories
        self.plugins = config.plugins

    def createDatabase(self) -> networkx.MultiDiGraph:
        """ Get graph of packages with data and relations described by plugins

        :return: Graph of packages
        :rtype: networkx.MultiDiGraph
        """
        graph = networkx.MultiDiGraph()
        
        dataPlugins = [plugin for plugin in self.plugins if isinstance(
            plugin, RPQRDataPlugin)]
        relationPlugins = [plugin for plugin in self.plugins if isinstance(
            plugin, RPQRRelationPlugin)]

        av_query = self._getAvailableQuery()
        q_avail = av_query.run()

        for id, pkg in enumerate(q_avail):
            graph.add_node(id)
            for pluginInstance in dataPlugins:
                pluginInstance: RPQRDataPlugin
                pluginInstance.fillData(id, pkg, graph)

        for id, pkg in enumerate(q_avail):
            for pluginInstance in relationPlugins:
                pluginInstance: RPQRRelationPlugin
                pluginInstance.fillData(id, pkg, graph, av_query)
        return graph

    def _getAvailableQuery(self) -> hawkey.Query:
        """ Get hawkey query of available packages

        :return: available query
        :rtype: hawkey.Query
        """
        base = dnf.Base()
        for (name, url) in self.repositories:
            base.repos.add_new_repo(name, base.conf, baseurl=[url])
        base.fill_sack(load_system_repo=False, load_available_repos=True)
        return base.sack.query().available()
