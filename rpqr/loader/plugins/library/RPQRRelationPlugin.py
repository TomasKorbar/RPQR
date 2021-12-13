from rpqr.loader.plugins.library import RPQRBasePlugin
import networkx


class RPQRRelationPlugin(RPQRBasePlugin):
    desiredName = None
    optionalDataStructure = None

    def fillData(self, id, pkg, graph: networkx.MultiGraph, query):
        targetList = self.prepareData(pkg, graph, query)
        for (target, direction) in targetList:
            if direction is not None:
                graph.add_edge(
                    id, target, type=self.desiredName, direction=target)
            else:
                graph.add_edge(id, target, type=self.desiredName)

    def prepareData(self, pkg, graph, query):
        pass
