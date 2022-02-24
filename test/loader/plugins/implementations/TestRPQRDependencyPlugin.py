'''
Project: RPQR
Author: Tomáš Korbař (tomas.korb@seznam.cz)
Copyright 2021 - 2022 Tomáš Korbař
'''

import unittest

from rpqr.loader.plugins.implementations.RPQRDependencyPlugin import RPQRDependencyPlugin, WhatDepensOnFilter
from rpqr.loader.plugins.implementations.RPQRDependencyPlugin import OnWhatDependsFilter
from loader.plugins.implementations.HawkeyPackageMock import HawkeyPackageMock
from loader.plugins.implementations.HawkeyQueryMock import HawkeyQueryMock
from networkx import MultiDiGraph


class TestRPQRDependencyPlugin(unittest.TestCase):
    def testPrepareData(self):
        plug = RPQRDependencyPlugin()
        pkg = HawkeyPackageMock()
        query = HawkeyQueryMock()
        graph = MultiDiGraph()
        graph.add_node(1, name="one")
        graph.add_node(2, name="two")
        graph.add_node(3, name="three")
        self.assertEqual(plug.prepareData(pkg, graph, query), [1, 2, 3])

    def testOnWhatDependsFilter(self):
        graph = MultiDiGraph()
        graph.add_node(1, name="one")
        graph.add_node(2, name="two")
        graph.add_node(3, name="three")
        graph.add_edge(1, 2, key="depends")
        self.assertEqual(OnWhatDependsFilter.execute(
            graph, ["one", "3"]), [1, 2])

    def testWhatDependsOnFilter(self):
        graph = MultiDiGraph()
        graph.add_node(1, name="one")
        graph.add_node(2, name="two")
        graph.add_node(3, name="three")
        graph.add_edge(1, 2, key="depends")
        self.assertEqual(WhatDepensOnFilter.execute(
            graph, ["two", "3"]), [2, 1])
