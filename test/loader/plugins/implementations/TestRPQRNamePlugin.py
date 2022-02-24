'''
Project: RPQR
Author: Tomáš Korbař (tomas.korb@seznam.cz)
Copyright 2021 - 2022 Tomáš Korbař
'''

import unittest

from rpqr.loader.plugins.implementations.RPQRNamePlugin import NameLikeFilter, RPQRNamePlugin, NameFilter, SetFilter
from loader.plugins.implementations.HawkeyPackageMock import HawkeyPackageMock
from networkx import MultiDiGraph


class TestRPQRNamePlugin(unittest.TestCase):
    def testPrepareData(self):
        plug = RPQRNamePlugin()
        pkg = HawkeyPackageMock()
        self.assertEqual(plug.prepareData(pkg), "one")

    def testNameFilter(self):
        graph = MultiDiGraph()
        graph.add_node(1, name="one", maintainer=["maint1", "maint2"])
        graph.add_node(2, name="two", maintainer=["maint1"])
        graph.add_node(3, name="three", maintainer=["maint2"])
        self.assertEqual(NameFilter.execute(graph, ["one"]), [1])

    def testNameLikeFilter(self):
        graph = MultiDiGraph()
        graph.add_node(1, name="one", maintainer=["maint1", "maint2"])
        graph.add_node(2, name="onelike", maintainer=["maint1"])
        graph.add_node(3, name="three", maintainer=["maint2"])
        self.assertEqual(NameLikeFilter.execute(graph, ["one"]), [1, 2])

    def testSetFilter(self):
        graph = MultiDiGraph()
        graph.add_node(1, name="one", maintainer=["maint1", "maint2"])
        graph.add_node(2, name="onelike", maintainer=["maint1"])
        graph.add_node(3, name="three", maintainer=["maint2"])
        self.assertEqual(SetFilter.execute(graph, ["one", [2, 3]]), [2])
