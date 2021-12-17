'''
Project: RPQR
Author: Tomáš Korbař (tomas.korb@seznam.cz)
Copyright 2021 - 2021 Tomáš Korbař
'''

from typing import Optional
import networkx

from rpqr.library import RPQRConfiguration
from rpqr.query.language.interpreter import RPQRInterpreter
from rpqr.query.language.parser import RPQRParser
from rpqr.query.language.scanner import RPQRScanner


class RPQRQuery:
    """ Interface for simplification of executing queries
    """
    def performQuery(query: str, graph: networkx.MultiDiGraph, config: RPQRConfiguration) -> Optional[networkx.MultiDiGraph]:
        """ perform query on graph

        :param query: query in RPQR language
        :type query: str
        :param graph: graph of packages
        :type graph: networkx.MultiDiGraph
        :param config: RPQR configuration 
        :type config: RPQRConfiguration
        :return: result of query
        :rtype: Optional[networkx.MultiDiGraph]
        """
        scanner = RPQRScanner(config)
        parser = RPQRParser(config)
        interpreter = RPQRInterpreter(config)
        tokens = scanner.getTokens(query)
        if tokens == None:
            return None
        abstractSyntacticTree = parser.parseTokens(tokens)
        if abstractSyntacticTree == None:
            return None
        return interpreter.performCommands(graph, abstractSyntacticTree)
