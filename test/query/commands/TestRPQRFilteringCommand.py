import unittest

from rpqr.query.commands.RPQRFilteringCommand import RPQRFilteringCommand
from networkx import MultiDiGraph


class TestRPQRFilteringCommand(unittest.TestCase):
    def testBFSOut(self):
        graph = MultiDiGraph()
        nodes = [1]
        graph.add_node(1, name="one")
        graph.add_node(2, name="two")
        graph.add_node(3, name="three")
        graph.add_node(4, name="four")
        graph.add_edge(1, 2, "depends")
        graph.add_edge(2, 3, "depends")

        self.assertEqual(RPQRFilteringCommand._BFS(
            graph, nodes, 20, "depends", inEdges=False), [1, 2, 3])
    
    def testBFSIn(self):
        graph = MultiDiGraph()
        nodes = [3]
        graph.add_node(1, name="one")
        graph.add_node(2, name="two")
        graph.add_node(3, name="three")
        graph.add_node(4, name="four")
        graph.add_edge(1, 2, "depends")
        graph.add_edge(2, 3, "depends")

        self.assertEqual(RPQRFilteringCommand._BFS(
            graph, nodes, 20, "depends", inEdges=True), [3, 2, 1])
