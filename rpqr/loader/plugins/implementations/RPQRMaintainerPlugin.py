'''
Project: RPQR
Author: Tomáš Korbař (tomas.korb@seznam.cz)
Copyright 2021 - 2021 Tomáš Korbař
'''

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
        maxDepth = int(args[1])
        nodes = [a for a in list(graph.nodes)
                 if targetUser in graph.nodes[a]["maintainer"]]
        for node in nodes:
            graph.nodes[node]["depth"] = 1
        nodeIndex = 0
        # our well know BFS
        # TODO: investigate whether BFS and DFS could not be implemented
        # generally in plugin base class
        while len(nodes) > nodeIndex:
            curNode = nodes[nodeIndex]
            if maxDepth != 0 and graph.nodes[curNode]["depth"] >= maxDepth:
                nodeIndex += 1
                continue
            for node1, node2, data in graph.in_edges([curNode], data=True):
                if data["type"] != "depends":
                    continue
                if node1 not in nodes:
                    graph.nodes[node1]["depth"] = graph.nodes[curNode]["depth"]+1
                    nodes.append(node1)
            nodeIndex += 1

        for node in nodes:
            graph.nodes[node].pop("depth")
        
        return nodes


class RPQRMaintainerPlugin(RPQRDataPlugin):
    """ Plugin allowing us to store information about package maintainers
        and ask Queries about them
    """
    desiredName = "maintainer"

    implementedCommands = [MaintainerFilter, DependsOnUserFilter]

    packageToMaintainer = None

    def prepareData(self, pkg : hawkey.Package) -> List[str]:
        """Get maintainers of package

        :param pkg: hawkey package information
        :type pkg: hawkey.Package
        :return: list of maintainers
        :rtype: List[str]
        """
        # download package maintainer list and build dictionary from it
        if RPQRMaintainerPlugin.packageToMaintainer is None:
            RPQRMaintainerPlugin.packageToMaintainer = {}
            data = requests.get(
                'https://src.fedoraproject.org/extras/pagure_owner_alias.json').json()["rpms"]
            data: dict
            for name, value in data.items():
                RPQRMaintainerPlugin.packageToMaintainer[name] = value
        # owner alias json uses source names as keys
        return RPQRMaintainerPlugin.packageToMaintainer[pkg.source_name]
