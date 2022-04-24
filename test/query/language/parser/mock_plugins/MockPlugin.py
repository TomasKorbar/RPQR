'''
Project: RPQR
Author: Tomáš Korbař (tomas.korb@seznam.cz)
Copyright 2021 - 2022 Tomáš Korbař
'''

from typing import List

import hawkey
from rpqr.loader.plugins.library import RPQRDataPlugin
from rpqr.query.commands import RPQRFilteringCommand
import networkx


class DummyFilter(RPQRFilteringCommand):
    args = [str]
    name = "DUMMY"

    def execute(graph: networkx.MultiGraph, args: list) -> List[int]:
        return list(graph.nodes)

class SmartFilter(RPQRFilteringCommand):
    args = [int]
    name = "SMART"

    def execute(graph: networkx.MultiGraph, args: list) -> List[int]:
        id = int(args[0])
        return [id]

class SubstatementFilter(RPQRFilteringCommand):
    args = [list]
    name = "SUB"

    def execute(graph: networkx.MultiGraph, args: list) -> List[int]:
        return [args[0]]

class MockPlugin(RPQRDataPlugin):
    """Plugin allowing us to gather package names and perform queries
    about them
    """
    desiredName = "mock"

    implementedCommands = [DummyFilter, SmartFilter, SubstatementFilter]

    def prepareData(self, pkg: hawkey.Package) -> str:
        return 'mock'
