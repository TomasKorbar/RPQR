'''
Project: RPQR
Author: Tomáš Korbař (tomas.korb@seznam.cz)
Copyright 2021 - 2021 Tomáš Korbař
'''

from typing import List

import hawkey
from rpqr.loader.plugins.library import RPQRDataPlugin
from rpqr.query.commands import RPQRFilteringCommand
import networkx


class NameFilter(RPQRFilteringCommand):
    """ Command allowing us to filter packages by name
    """
    args = [str]
    name = "NAME"

    def execute(graph: networkx.MultiGraph, args: list) -> List[int]:
        """ Get list of package node ids for packages which name exactly matches
            args[0]

        :param graph: built graph of packages
        :type graph: MultiDiGraph
        :param args: arguments supplied to command
        :type args: list
        :return: node ids of packages which name exactly matches supplied name (only one)
        :rtype: List[int]
        """
        targetName = args[0]
        nodes = []

        for (node, attrs) in graph.nodes.items():
            if attrs["name"] == targetName:
                nodes.append(node)
                break

        return nodes


class NameLikeFilter(RPQRFilteringCommand):
    """Command allowing us to filter packages by existence of substring
    in their name
    """
    args = [str]
    name = "NAMELIKE"

    def execute(graph: networkx.MultiGraph, args: list) -> List[int]:
        """ Get list of package node ids which name contains substring
            args[0]

        :param graph: built graph of packages
        :type graph: MultiDiGraph
        :param args: arguments supplied to command
        :type args: list
        :return: node ids of packages which name contains supplied substring
        :rtype: List[int]
        """
        targetName = args[0]
        nodes = []
        for (node, attrs) in graph.nodes.items():
            if targetName in attrs["name"]:
                nodes.append(node)

        return nodes


class FilterSet(RPQRFilteringCommand):
    """ Command allowing us to filter subset of packages by existence of
    substring in their name

    NOTE: Now used mainly for testing of subset filtering feature
    """
    args = [str, list]
    name = "SUBSETNAMELIKE"

    def execute(graph: networkx.MultiGraph, args: list) -> List[int]:
        """ Get list of package node ids for packages of subset args[1]
        which name contains substring args[0]

        :param graph: built graph of packages
        :type graph: MultiDiGraph
        :param args: arguments supplied to command
        :type args: list
        :return: node ids of packages from subset which name contains supplied substring
        :rtype: List[int]
        """
        targetName = args[0]
        subset = args[1]

        nodes = []
        for node in subset:
            if targetName in graph.nodes[node]["name"]:
                nodes.append(node)

        return nodes


class RPQRNamePlugin(RPQRDataPlugin):
    """Plugin allowing us to gather package names and perform queries
    about them
    """
    desiredName = "name"

    implementedCommands = [NameFilter, NameLikeFilter, FilterSet]

    def prepareData(self, pkg: hawkey.Package) -> str:
        return str(pkg)
