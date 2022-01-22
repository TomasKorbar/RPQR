'''
Project: RPQR
Author: Tomáš Korbař (tomas.korb@seznam.cz)
Copyright 2021 - 2021 Tomáš Korbař
'''

import os
import dnf
import json
import hawkey
import logging
import networkx
from networkx.readwrite import json_graph


from rpqr.library import RPQRConfiguration
from rpqr.loader.plugins.library.RPQRDataPlugin import RPQRDataPlugin
from rpqr.loader.plugins.library.RPQRRelationPlugin import RPQRRelationPlugin


class RPQRLoader:
    """ Class handling loading of repositories and building graphs
    """

    def __init__(self, config: RPQRConfiguration) -> None:
        """ Create instance of RPQRLoader

        :param config: provided rpqr configuration
        :type config: RPQRConfiguration
        """
        self.repositories = config.repositories
        self.plugins = config.plugins
        self.logger = config.rootLogger.getChild("RPQRLoader")

    def createDatabase(self, cache: str = None) -> networkx.MultiDiGraph:
        """ Get graph of packages with data and relations described by plugins

        :param cache: path to cache file, defaults to None
        :type cache: str, optional
        :return: Graph of packages
        :rtype: networkx.MultiDiGraph
        """
        graph = networkx.MultiDiGraph()
        dataPlugins = [plugin for plugin in self.plugins if isinstance(
            plugin, RPQRDataPlugin)]
        relationPlugins = [plugin for plugin in self.plugins if isinstance(
            plugin, RPQRRelationPlugin)]

        pluginRecords = []
        for plugin in dataPlugins + relationPlugins:
            pluginRecords.append((plugin, plugin.__class__.__name__))

        if os.path.exists(cache) and os.path.isfile(cache):
            with open(cache, "r") as cFile:
                graph = json_graph.node_link_graph(json.loads(cFile.read()))
            self.logger.info("Using found cache")
            for (plugin, name) in pluginRecords:
                if name in graph.graph["plugins"]:
                    if plugin in dataPlugins:
                        dataPlugins.remove(plugin)
                    elif plugin in relationPlugins:
                        relationPlugins.remove(plugin)
                    self.logger.info(
                        "Will not build information for plugin %s as cache already contains it", name)
        else:
            self.logger.info("Cache was not found so building it")

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

        graph.graph["plugins"] = [name for (_, name) in pluginRecords]

        if cache is not None:
            with open(cache, "w") as cFile:
                cFile.write(json.dumps(json_graph.node_link_data(graph)))

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
