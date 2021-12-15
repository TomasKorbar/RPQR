from rpqr.loader.plugins.library import RPQRDataPlugin
from rpqr.query.commands import RPQRFilteringCommand
import requests
import networkx

class MaintainerFilter(RPQRFilteringCommand):
    args = [str]
    name = "MAINTAINER"

    def execute(graph: networkx.MultiDiGraph, args: list):
        targetMaintainer = args[0]
        nodes = []
        for (node, attrs) in graph.nodes.items():
            if targetMaintainer in attrs["maintainer"]:
                nodes.append(node)

        return nodes

class DependsOnUserFilter(RPQRFilteringCommand):
    args = [str, int]
    name = "DEPENDSONUSER"

    def execute(graph: networkx.MultiDiGraph, args: list):
        targetUser = args[0]
        maxDepth = int(args[1])
        nodes = [a for a in list(graph.nodes) if targetUser in graph.nodes[a]["maintainer"]]
        for node in nodes:
            graph.nodes[node]["depth"] = 0
        nodeIndex = 0
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
        return nodes

class RPQRMaintainerPlugin(RPQRDataPlugin):
    desiredName = "maintainer"

    implementedCommands = [MaintainerFilter, DependsOnUserFilter]

    packageToMaintainer = None

    def prepareData(self, pkg):
        if RPQRMaintainerPlugin.packageToMaintainer is None:
            RPQRMaintainerPlugin.packageToMaintainer = {}
            data = requests.get('https://src.fedoraproject.org/extras/pagure_owner_alias.json').json()["rpms"]
            data : dict
            for name, value in data.items():
                RPQRMaintainerPlugin.packageToMaintainer[name] = value
        return RPQRMaintainerPlugin.packageToMaintainer[pkg.source_name]