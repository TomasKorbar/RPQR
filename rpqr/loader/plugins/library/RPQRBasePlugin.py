'''
Project: RPQR
Author: Tomáš Korbař (tomas.korb@seznam.cz)
Copyright 2021 - 2022 Tomáš Korbař
'''

from logging import Logger
import hawkey
import networkx


class RPQRBasePlugin:
    """Base class for all plugins
    """
    implementedCommands = []

    def __init__(self, rootLogger: Logger = None, config: dict = None):
        pass

    def fillData(self, id: int, pkg: hawkey.Package, graph: networkx.MultiDiGraph):
        """ Method implemented by plugin type to describe way how to save data

        :param id: id of package node
        :type id: int
        :param pkg: Hawkey package object
        :type pkg: hawkey.Package
        :param graph: graph of packages
        :type graph: networkx.MultiDiGraph
        """
        pass

    def prepareData(self):
        """ Method implemented by individual plugin implementations returning data for particular
        package
        """
        pass
