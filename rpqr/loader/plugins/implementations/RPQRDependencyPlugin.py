from rpqr.loader.plugins.library import RPQRRelationPlugin
from networkx import MultiGraph

class RPQRDependencyPlugin(RPQRRelationPlugin):
    desiredName = "depends"

    def prepareData(self, pkg, graph : MultiGraph, query):
        if self.optionalDataStructure == None:
            self.optionalDataStructure = {}
            for (node, attribs) in graph.nodes.items():
                self.optionalDataStructure[attribs["Name"]] = node

        edges = list()
        requiredPackages = query.filter(provides=pkg.requires).run()
        for dependency in requiredPackages:
            target = self.optionalDataStructure[str(dependency)]
            edges.append((target, target))
        return edges
