'''
Project: RPQR
Author: Tomáš Korbař (tomas.korb@seznam.cz)
Copyright 2021 - 2022 Tomáš Korbař
'''

from tkinter.messagebox import NO
from typing import Optional
import networkx

from rpqr.library import RPQRConfiguration
from rpqr.loader import RPQRLoader
from rpqr.query.language.interpreter import RPQRInterpreter
from rpqr.query.language.parser import RPQRParser
from rpqr.query.language.scanner import RPQRScanner


class RPQRQuery:
    """ Interface for simplification of executing queries
    """
    def __init__(self, config: RPQRConfiguration) -> None:
        self._config = config
        loader = RPQRLoader(self._config)
        self._graph = loader.createDatabase()

    def performQuery(self, query: str, graph: networkx.MultiDiGraph = None, config: RPQRConfiguration = None) -> Optional[networkx.MultiDiGraph]:
        """ perform query on graph
        :param query: query in RPQR language
        :type query: str
        :return: result of query
        :rtype: Optional[networkx.MultiDiGraph]
        """
        scanner = RPQRScanner(self._config)
        parser = RPQRParser(self._config)
        interpreter = RPQRInterpreter(self._config)
        tokens = scanner.getTokens(query)
        if tokens == None:
            return None
        abstractSyntacticTree = parser.parseTokens(tokens)
        if abstractSyntacticTree == None:
            return None
        return interpreter.performCommands(self._graph, abstractSyntacticTree)
