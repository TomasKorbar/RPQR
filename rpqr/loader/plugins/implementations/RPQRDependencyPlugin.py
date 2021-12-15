'''
Project: RPQR
Author: Tomáš Korbař (tomas.korb@seznam.cz)
Copyright 2021 - 2021 Tomáš Korbař
'''

from rpqr.loader.plugins.library import RPQRRelationPlugin
from networkx import MultiDiGraph
from rpqr.query.commands import RPQRFilteringCommand


class OnWhatDependsFilter(RPQRFilteringCommand):
    args = [str, int]
    name = "ONWHATDEPENDS"

    def execute(graph: MultiDiGraph, args: list):
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
            for node1, node2, data in graph.out_edges([curNode], data=True):
                if data["type"] != "depends":
                    continue
                if node2 not in nodes:
                    nodes.append(node2)
                    graph.nodes[node2]["depth"] = graph.nodes[curNode]["depth"] + 1
            nodesIndex += 1

        return nodes

class WhatDepensOnFilter(RPQRFilteringCommand):
    args = [str, int]
    name = "WHATDEPENDSON"

    def execute(graph: MultiDiGraph, args: list):
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

        return nodes

class RPQRDependencyPlugin(RPQRRelationPlugin):
    desiredName = "depends"
    implementedCommands = [OnWhatDependsFilter, WhatDepensOnFilter]

    def prepareData(self, pkg, graph: MultiDiGraph, query):
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
