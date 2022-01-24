'''
Project: RPQR
Author: Tomáš Korbař (tomas.korb@seznam.cz)
Copyright 2021 - 2022 Tomáš Korbař
'''

from typing import Callable, List
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

    def _BFS(graph: networkx.MultiDiGraph, rootNodes: List[int], maxDepth: int, relationType: str,
             filter: Callable[[int, int, dict], bool] = lambda x,y,z: True,
             inEdges: bool = True) -> List[int]:
        """ This is implementation of breadth first search algorithm which goes trough rootNodes
            and adds nodes which are adjacent to them and fulfill specified filter.

        :param graph: graph of packages
        :type graph: networkx.MultiDiGraph
        :param rootNodes: nodes where search should start
        :type rootNodes: List[int]
        :param maxDepth: maximal depth of graph (relations can lead through too many packages and
            this allows us to find valid results while keeping the graph understandable)
        :type maxDepth: int
        :param relationType: type of relation through which bfs should traverse
        :param filter: condition which all nodes should fulfill, defaults to lambda x,y,z: True
        :type filter: Callable[[int, int, dict], bool], optional
        :param inEdges: specifies whether bfs should traverse through in or out edges,
            defaults to True
        :type inEdges: bool, optional
        :return: Ids of nodes which passed filter and were found by BFS
        :rtype: List[int]
        """
        nodes = rootNodes.copy()
        nodeIndex = 0
        for node in rootNodes:
            graph.nodes[node]["depth"] = 0

        while len(rootNodes) > nodeIndex:
            curNode = nodes[nodeIndex]
            if maxDepth != -1 and graph.nodes[curNode]["depth"] > maxDepth:
                nodeIndex += 1
                continue
            edges = graph.in_edges([curNode], keys=True) if inEdges else graph.out_edges(
                [curNode], keys=True)
            for node1, node2, key in edges:
                if key != relationType:
                    continue
                checkedNode = node1 if inEdges else node2
                if checkedNode not in nodes and filter(node1, node2, key):
                    graph.nodes[checkedNode]["depth"] = graph.nodes[curNode]["depth"]+1
                    nodes.append(checkedNode)
            nodeIndex += 1

        for node in nodes:
            graph.nodes[node].pop("depth")

        return nodes
