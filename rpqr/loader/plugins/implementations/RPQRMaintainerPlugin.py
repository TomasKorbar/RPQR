'''
Project: RPQR
Author: Tomáš Korbař (tomas.korb@seznam.cz)
Copyright 2021 - 2022 Tomáš Korbař
'''

from logging import Logger
from typing import List
import requests
import networkx
import hawkey

from rpqr.loader.plugins.library import RPQRDataPlugin
from rpqr.query.commands import RPQRFilteringCommand


class MaintainerFilter(RPQRFilteringCommand):
    """Command allowing to filter packages by maintainer
    """
    args = [str]
    name = "MAINTAINER"

    def execute(graph: networkx.MultiDiGraph, args: list) -> List[int]:
        """ Get node ids of packages which have supplied maintainer args[0]

        :param graph: built graph of packages
        :type graph: MultiDiGraph
        :param args: arguments supplied to command
        :type args: list
        :return: node ids of packages with supplied maintainer
        :rtype: List[int]
        """
        targetMaintainer = args[0]
        nodes = []
        for (node, attrs) in graph.nodes.items():
            if targetMaintainer in attrs["maintainer"]:
                nodes.append(node)

        return nodes


class DependsOnUserFilter(RPQRFilteringCommand):
    """Command allowing filtering packages which depend on certain maintainer.
    That means the person is either maintaining them or package depends on
    package which they maintain recursively.
    """
    args = [str, int]
    name = "DEPENDSONUSER"

    def execute(graph: networkx.MultiDiGraph, args: list) -> List[int]:
        """ Get list of ids of packages which depend on user specified in args[0]
        to max depth args[1]

        :param graph: built graph of packages
        :type graph: MultiDiGraph
        :param args: arguments supplied to command
        :type args: list
        :return: node ids of packages which depend on specified maintainer
        :rtype: List[int]
        """
        targetUser = args[0]
        depth = int(args[1])
        nodes = [a for a in list(graph.nodes)
                 if targetUser in graph.nodes[a]["maintainer"]]

        return RPQRFilteringCommand._BFS(graph, nodes, depth, "depends")


class RPQRMaintainerPlugin(RPQRDataPlugin):
    """ Plugin allowing us to store information about package maintainers
        and ask Queries about them
    """
    desiredName = "maintainer"

    implementedCommands = [MaintainerFilter, DependsOnUserFilter]

    packageToMaintainer = None

    def __init__(self, rootLogger: Logger = None, config: dict = None):
        self.listUrl = None
        if config == None and rootLogger != None:
            lgr = rootLogger.getChild("RPQRDataPlugin")
            lgr.warning("url for retrieval of maintainers was not supplied")
            return

        self.logger = rootLogger.getChild(
            "RPQRDataPlugin") if rootLogger != None else None

        self.listUrl = config.get("url")

    def _downloadJson(self):
        if self.listUrl == None:
            return {}
        receivedResponse = requests.get(self.listUrl)

        if receivedResponse.status_code != 200:
            self.logger.error(
                "RPQR was unable to retrieve maintainer list from supplied url %s" % self.listUrl)

        return receivedResponse.json().get("rpms", {})

    def prepareData(self, pkg: hawkey.Package) -> List[str]:
        """Get maintainers of package

        :param pkg: hawkey package information
        :type pkg: hawkey.Package
        :return: list of maintainers
        :rtype: List[str]
        """
        # download package maintainer list and build dictionary from it
        if RPQRMaintainerPlugin.packageToMaintainer is None:
            RPQRMaintainerPlugin.packageToMaintainer = {}
            data = self._downloadJson()
            data: dict
            for name, value in data.items():
                RPQRMaintainerPlugin.packageToMaintainer[name] = value
        # owner alias json uses source names as keys
        return RPQRMaintainerPlugin.packageToMaintainer[pkg.name if pkg.source_name == None else pkg.source_name]
