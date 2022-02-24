'''
Project: RPQR
Author: Tomáš Korbař (tomas.korb@seznam.cz)
Copyright 2021 - 2022 Tomáš Korbař
'''

import unittest

from rpqr.loader.plugins.implementations.RPQRMaintainerPlugin import DependsOnUserFilter, RPQRMaintainerPlugin, MaintainerFilter
from loader.plugins.implementations.HawkeyPackageMock import HawkeyPackageMock
from networkx import MultiDiGraph


class TestRPQRMaintainerPlugin(unittest.TestCase):
    def testPrepareData(self):
        plug = RPQRMaintainerPlugin(config={"url": "hello"})
        plug._downloadJson = lambda: {"one": ["maint1", "maint2"]}
        pkg = HawkeyPackageMock()
        self.assertEqual(plug.prepareData(pkg), ["maint1", "maint2"])

    def testMaintainerFilter(self):
        graph = MultiDiGraph()
        graph.add_node(1, name="one", maintainer=["maint1", "maint2"])
        graph.add_node(2, name="two", maintainer=["maint1"])
        graph.add_node(3, name="three", maintainer=["maint2"])
        self.assertEqual(MaintainerFilter.execute(graph, ["maint1"]), [1, 2])

    def testDependsOnUserFilter(self):
        graph = MultiDiGraph()
        graph.add_node(1, name="one", maintainer=["maint1", "maint2"])
        graph.add_node(2, name="two", maintainer=["maint1"])
        graph.add_node(3, name="three", maintainer=["maint2"])
        graph.add_edge(3, 1, key="depends")
        self.assertEqual(DependsOnUserFilter.execute(
            graph, ["maint1", "3"]), [1, 2, 3])
