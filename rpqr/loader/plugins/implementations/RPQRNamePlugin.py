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

        return graph.subgraph(nodes)

class RPQRNamePlugin(RPQRDataPlugin):
    desiredName = "name"
    
    implementedCommands = [NameFilter]

    def prepareData(self, pkg):
        return str(pkg)