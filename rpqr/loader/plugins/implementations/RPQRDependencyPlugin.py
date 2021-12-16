'''
Project: RPQR
Author: Tomáš Korbař (tomas.korb@seznam.cz)
Copyright 2021 - 2021 Tomáš Korbař
'''


import hawkey
from typing import List
from networkx import MultiDiGraph

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
        nodesIndex = 0
        graph.nodes[targetNode]["depth"] = 0
        # this is a BFS of dependencies
        while len(nodes) > nodesIndex:
            curNode = nodes[nodesIndex]
            # == would be sufficient but use >= just to be sure
            if graph.nodes[curNode]["depth"] >= depth:
                nodesIndex += 1
                continue
            for node1, node2, data in graph.out_edges([curNode], data=True):
                # if this is not a depends relation then skip it
                if data["type"] != "depends":
                    continue
                if node2 not in nodes:
                    nodes.append(node2)
                    graph.nodes[node2]["depth"] = graph.nodes[curNode]["depth"] + 1
            nodesIndex += 1

        # we should tidy after ourselves
        for node in nodes:
            graph.nodes[node].pop("depth")

        return nodes


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
        nodesIndex = 0
        graph.nodes[targetNode]["depth"] = 0
        while len(nodes) > nodesIndex:
            curNode = nodes[nodesIndex]
            if graph.nodes[curNode]["depth"] >= depth:
                nodesIndex += 1
                continue
            for node1, node2, data in graph.in_edges([curNode], data=True):
                if data["type"] != "depends":
                    continue
                if node1 not in nodes:
                    nodes.append(node1)
                    graph.nodes[node1]["depth"] = graph.nodes[curNode]["depth"] + 1
            nodesIndex += 1

        for node in nodes:
            graph.nodes[node].pop("depth")

        return nodes


class RPQRDependencyPlugin(RPQRRelationPlugin):
    """Plugin for gathering dependencies of packages and allowing filtering
    by them
    """
    desiredName = "depends"
    implementedCommands = [OnWhatDependsFilter, WhatDepensOnFilter]

    def __init__(self) -> None:
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
