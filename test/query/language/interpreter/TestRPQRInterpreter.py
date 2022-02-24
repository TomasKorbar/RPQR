'''
Project: RPQR
Author: Tomáš Korbař (tomas.korb@seznam.cz)
Copyright 2021 - 2022 Tomáš Korbař
'''

import unittest
from networkx import MultiDiGraph

from rpqr.library.RPQRConfiguration import RPQRConfiguration
from rpqr.query.language.interpreter import RPQRInterpreter
from rpqr.query.language.parser import RPQRStackSymbol
from rpqr.query.language.scanner import RPQRToken


class TestRPQRInterpreter(unittest.TestCase):
    def testInterpreterOne(self):
        config = RPQRConfiguration(
            ["./test/query/language/parser/mock_plugins"], [])
        interpreter = RPQRInterpreter(config)

        graph = MultiDiGraph()
        graph.add_node(1, name="one")
        graph.add_node(2, name="two")
        graph.add_node(3, name="three")
        graph.add_node(4, name="four")
        myAST = RPQRStackSymbol(
            14, [RPQRToken(13, "DUMMY"), RPQRToken(6, "argument")])

        resultGraph = interpreter.performCommands(graph, myAST)
        self.assertEqual(list(resultGraph.nodes), [1, 2, 3, 4])

    def testInterpreterTwo(self):
        config = RPQRConfiguration(
            ["./test/query/language/parser/mock_plugins"], [])
        interpreter = RPQRInterpreter(config)

        graph = MultiDiGraph()
        graph.add_node(1, name="one")
        graph.add_node(2, name="two")
        graph.add_node(3, name="three")
        graph.add_node(4, name="four")
        myAST = RPQRStackSymbol(14, [RPQRStackSymbol(14, [RPQRToken(13, "DUMMY"), RPQRToken(
            6, "argument")]), RPQRStackSymbol(14, [RPQRToken(13, "SMART"), RPQRToken(5, "3")])], "&")

        resultGraph = interpreter.performCommands(graph, myAST)
        self.assertEqual(list(resultGraph.nodes), [3])
