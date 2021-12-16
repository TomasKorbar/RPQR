'''
Project: RPQR
Author: Tomáš Korbař (tomas.korb@seznam.cz)
Copyright 2021 - 2021 Tomáš Korbař
'''

from typing import List
import networkx


class RPQRFilteringCommand:
    """ Base class for commands
    """
    args = None
    name = None

    def execute(graph: networkx.MultiDiGraph, args: list) -> List[int]:
        """ Get nodes matching described conditions

        :param graph: graph of packages
        :type graph: networkx.MultiDiGraph
        :param args: arguments supplied to command
        :type args: list
        :return: list of nodes matching described conditions
        :rtype: List[int]
        """
        pass
