'''
Project: RPQR
Author: Tomáš Korbař (tomas.korb@seznam.cz)
Copyright 2021 - 2021 Tomáš Korbař
'''

from rpqr.loader.plugins.library import RPQRBasePlugin
import networkx


class RPQRRelationPlugin(RPQRBasePlugin):
    desiredName = None
    optionalDataStructure = None

    def fillData(self, id, pkg, graph: networkx.MultiDiGraph, query):
        targetList = self.prepareData(pkg, graph, query)
        for target in targetList:
            graph.add_edge(id, target, type=self.desiredName)

    def prepareData(self, pkg, graph, query):
        pass
