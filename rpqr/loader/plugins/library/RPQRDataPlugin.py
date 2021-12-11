from typing import Type
from rpqr.loader.plugins.library import RPQRBasePlugin

class RPQRDataPlugin(RPQRBasePlugin):
    desiredType: Type = None
    desiredName: str = None

    def fillData(self, id, pkg, graph):
        data = self.prepareData(pkg)
        graph.nodes[id][self.desiredName] = data

    def prepareData(self, pkg):
        pass