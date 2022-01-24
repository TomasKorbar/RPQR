'''
Project: RPQR
Author: Tomáš Korbař (tomas.korb@seznam.cz)
Copyright 2021 - 2022 Tomáš Korbař
'''

import hawkey
import networkx

from rpqr.loader.plugins.library import RPQRBasePlugin


class RPQRDataPlugin(RPQRBasePlugin):
    """ Base class for plugins which are inserting data into package nodes
    """
    desiredName: str = None

    def fillData(self, id: int, pkg: hawkey.Package, graph: networkx.MultiDiGraph) -> None:
        """ Insert data prepared by implementation to particular package node 

        :param id: id of package node
        :type id: int
        :param pkg: Hawkey package object
        :type pkg: hawkey.Package
        :param graph: graph of packages
        :type graph: networkx.MultiDiGraph
        """
        graph.nodes[id][self.desiredName] = self.prepareData(pkg)

    def prepareData(self, pkg: hawkey.Package):
        """ Method, provided by data plugins, which tells us value to save into node

        :param pkg: hawkey package object
        :type pkg: hawkey.Package
        """
        pass
