'''
Project: RPQR
Author: Tomáš Korbař (tomas.korb@seznam.cz)
Copyright 2021 - 2022 Tomáš Korbař
'''

from typing import List
import hawkey
from rpqr.loader.plugins.library import RPQRBasePlugin
import networkx


class RPQRRelationPlugin(RPQRBasePlugin):
    """ Plugin allowing to store information about package relation
    """
    desiredName = None

    def fillData(self, id: int, pkg: hawkey.Package, graph: networkx.MultiDiGraph, query: hawkey.Query):
        """ Insert relations specified by prepared data method to graph

        :param id: id of package node
        :type id: int
        :param pkg: Hawkey package object
        :type pkg: hawkey.Package
        :param graph: graph of packages
        :type graph: networkx.MultiDiGraph
        :param query: Query object allowing further queries through dnf api
        :type query: hawkey.Query
        """
        targetList = self.prepareData(pkg, graph, query)
        for target in targetList:
            graph.add_edge(id, target, key=self.desiredName)

    def prepareData(self, pkg: hawkey.Package, graph: networkx.MultiDiGraph, query: hawkey.Query) -> List[int]:
        """ Get list of nodes to which we want to form a relation

        :param pkg: hawkey package object
        :type pkg: hawkey.Package
        :param graph: graph of packages
        :type graph: networkx.MultiDiGraph
        :param query: Query object allowing further queries through dnf api
        :type query: hawkey.Query
        """
        pass
