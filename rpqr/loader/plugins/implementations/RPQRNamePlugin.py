from sys import argv
from rpqr.loader.plugins.library import RPQRDataPlugin
from rpqr.query.commands import RPQRFilteringCommand
import networkx


class NameFilter(RPQRFilteringCommand):
    args = [str]
    name = "NAME"

    def execute(graph: networkx.MultiGraph, args: list):
        targetName = args[0]
        nodes = []

        for (node, attrs) in graph.nodes.items():
            if attrs["name"] == targetName:
                nodes.append(node)
                break

        return nodes


class NameLikeFilter(RPQRFilteringCommand):
    args = [str]
    name = "NAMELIKE"

    def execute(graph: networkx.MultiGraph, args: list):
        targetName = args[0]
        nodes = []
        for (node, attrs) in graph.nodes.items():
            if targetName in attrs["name"]:
                nodes.append(node)

        return nodes

class FilterSet(RPQRFilteringCommand):
    args = [str, list]
    name = "SUBSETNAMELIKE"

    def execute(graph: networkx.MultiGraph, args: list):
        targetName = args[0]
        subset = args[1]
        
        nodes = []
        for node in subset:
            if targetName in graph.nodes[node]["name"]:
                nodes.append(node)
        
        return nodes


class RPQRNamePlugin(RPQRDataPlugin):
    desiredName = "name"

    implementedCommands = [NameFilter, NameLikeFilter, FilterSet]

    def prepareData(self, pkg):
        return str(pkg)
