'''
Project: RPQR
Author: Tomáš Korbař (tomas.korb@seznam.cz)
Copyright 2021 - 2022 Tomáš Korbař
'''


import hawkey
from typing import List
from networkx import MultiDiGraph
from logging import Logger

from rpqr.loader.plugins.library import RPQRRelationPlugin
from rpqr.query.commands import RPQRFilteringCommand


class OnWhatDependsFilter(RPQRFilteringCommand):
    """Command filtering packages on which supplied package depends
    """
    args = [str, int]
    name = "ONWHATDEPENDS"

    def execute(graph: MultiDiGraph, args: list) -> List[int]:
        """ Get node ids of packages on which depends package with name arg[0]
            to max depth arg[1] 

        :param graph: built graph of packages
        :type graph: MultiDiGraph
        :param args: arguments supplied to command
        :type args: list
        :return: ids of dependencies
        :rtype: List[int]
        """
        targetName = args[0]
        depth = int(args[1])
        nodes = []
        targetNode = None
        for (node, attrs) in graph.nodes.items():
            if attrs["name"] == targetName:
                targetNode = node
                break
        # we did not find the root package
        if targetNode == None:
            return []
        nodes.append(targetNode)

        return RPQRFilteringCommand._BFS(graph, nodes, depth, "depends", inEdges=False)


class WhatDepensOnFilter(RPQRFilteringCommand):
    """Command filtering packages which depend on supplied package
    """
    args = [str, int]
    name = "WHATDEPENDSON"

    def execute(graph: MultiDiGraph, args: list) -> List[int]:
        """ Get node ids of packages which depend on package with name arg[0]
            to max depth arg[1] 

        :param graph: built graph of packages
        :type graph: MultiDiGraph
        :param args: arguments supplied to command
        :type args: list
        :return: ids dependent packages
        :rtype: List[int]
        """
        # this algorithm is almost identical to the first command but
        # it traverses through graph by in edges instead of out edges
        targetName = args[0]
        depth = int(args[1])
        nodes = []
        targetNode = None
        for (node, attrs) in graph.nodes.items():
            if attrs["name"] == targetName:
                targetNode = node
                break
        if targetNode == None:
            return []
        nodes.append(targetNode)

        return RPQRFilteringCommand._BFS(graph, nodes, depth, "depends")


class RPQRDependencyPlugin(RPQRRelationPlugin):
    """Plugin for gathering dependencies of packages and allowing filtering
    by them
    """
    desiredName = "depends"
    implementedCommands = [OnWhatDependsFilter, WhatDepensOnFilter]

    def __init__(self, rootLogger: Logger = None, config: dict = None) -> None:
        self.optionalDataStructure = None

    def prepareData(self, pkg: hawkey.Package, graph: MultiDiGraph, query: hawkey.Query) -> List[int]:
        """ Get list of nodes to which we want to form this relation

        :param pkg: hawkey package object. Holds information supplied by dnf api
        :type pkg: hawkey.Package
        :param graph: graph of packages
        :type graph: MultiDiGraph
        :param query: hawkey query object. Allows further queries through dnf api
        :type query: hawkey.Query
        :return: list of target nodes for this node
        :rtype: List[int]
        """
        # we will use dictionary for optimalization of this process
        if self.optionalDataStructure == None:
            self.optionalDataStructure = {}
            for (node, attribs) in graph.nodes.items():
                self.optionalDataStructure[attribs["name"]] = node

        edges = list()
        requiredPackages = query.filter(provides=pkg.requires).run()
        for dependency in requiredPackages:
            target = self.optionalDataStructure[str(dependency)]
            edges.append(target)
        return edges
