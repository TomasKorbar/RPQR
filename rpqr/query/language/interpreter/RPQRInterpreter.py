'''
Project: RPQR
Author: Tomáš Korbař (tomas.korb@seznam.cz)
Copyright 2021 - 2022 Tomáš Korbař
'''

import networkx

from rpqr.query.commands.RPQRFilteringCommand import RPQRFilteringCommand
from rpqr.loader.plugins.library.RPQRBasePlugin import RPQRBasePlugin
from rpqr.library.RPQRConfiguration import RPQRConfiguration
from rpqr.query.language.interpreter import RPQRResultTree
from rpqr.query.language.parser import RPQRStackSymbol
from rpqr.query.language.scanner import RPQRToken


class RPQRInterpreter:
    """ RPQR language interpreter
    """

    def __init__(self, config: RPQRConfiguration) -> None:
        """ Get RPQRInterpreter instance

        :param config: provided rpqr configuration
        :type config: RPQRConfiguration
        """
        # dictionary for optimalization
        self.commandNameToClass = {}
        for plugin in config.plugins:
            plugin: RPQRBasePlugin
            for command in plugin.implementedCommands:
                command: RPQRFilteringCommand
                self.commandNameToClass[command.name] = command

    def performCommands(self, graph: networkx.MultiGraph, AST: RPQRStackSymbol) -> networkx.MultiDiGraph:
        """ Interpret abstract syntactic tree and get results

        :param graph: graph of packages
        :type graph: networkx.MultiGraph
        :param AST: Abstract syntactic tree
        :type AST: RPQRStackSymbol
        :return: subgraph matching conditions described by language
        :rtype: networkx.MultiDiGraph
        """
        # stack of RPQR stack symbols
        stack = []
        # stack of results
        resultStack = []
        curNode: RPQRStackSymbol = AST
        curResult: RPQRResultTree = RPQRResultTree(None, [])
        # interpreter is DFS algorithm resolving statements from bottom up
        stack.append(curNode)
        resultStack.append(curResult)
        while len(stack) > 0:
            curNode = stack[-1]
            curResult = resultStack[-1]
            if curNode.operator is not None:
                if len(curResult.childResults) < 1:
                    # every operator in RPQR language has at least one operand
                    leftResult = RPQRResultTree(None, [])
                    curResult.childResults.append(leftResult)
                    resultStack.append(leftResult)
                    curResult = leftResult
                    curNode = curNode.children[0]
                    stack.append(curNode)
                elif curNode.operator != '~' and len(curResult.childResults) < 2:
                    # if this is & or | then we need to yet resolve second operand
                    rightResult = RPQRResultTree(None, [])
                    curResult.childResults.append(rightResult)
                    resultStack.append(rightResult)
                    curResult = rightResult
                    curNode = curNode.children[1]
                    stack.append(curNode)
                else:
                    # now we have all operands, we can begin resolution
                    validNodes = []
                    if curNode.operator == '&':
                        validNodes = [
                            a for a in curResult.childResults[0].result if a in curResult.childResults[1].result]
                    elif curNode.operator == '|':
                        validNodes = curResult.childResults[0].result
                        for b in curResult.childResults[1].result:
                            if b not in validNodes:
                                validNodes.append(b)
                    elif curNode.operator == '~':
                        validNodes = [
                            a for a in list(graph.nodes) if a not in curResult.childResults[0].result]
                    curResult.result = validNodes
                    stack.pop()
                    resultStack.pop()
            else:
                # Since we allow commands to have statements as arguments,
                # this has to be a little more powerfull then resolving of typical
                # statement tree
                # we will be resolving arguments until we have all of them and then
                # execute the command and close node
                commandToken: RPQRToken = curNode.children[0]
                commandClass = self.commandNameToClass[commandToken.content]
                commandClass: RPQRFilteringCommand
                # if not resolved substatement is found then we need to stop resolution
                # and return to this when it is resolved
                # (we will resolve it immediately as next step)
                notResolvedStatementFound = False
                for argIndex, argType in enumerate(commandClass.args):
                    if argType == str or argType == int:
                        # literals can be resolved right away
                        if (argIndex > len(curResult.childResults)-1):
                            curResult.childResults.append(RPQRResultTree(
                                curNode.children[1:][argIndex].content, []))
                        else:
                            continue
                    elif argType == list:
                        if (argIndex > len(curResult.childResults)-1):
                            # this statement is not resolved => stop command resolution and resolve it
                            subStatementResult = RPQRResultTree(None, [])
                            curResult.childResults.append(subStatementResult)
                            resultStack.append(subStatementResult)
                            curResult = subStatementResult
                            curNode = curNode.children[1:][argIndex]
                            stack.append(curNode)
                            notResolvedStatementFound = True
                            break
                        else:
                            continue
                if notResolvedStatementFound:
                    continue
                arguments = []
                for partResult in curResult.childResults:
                    arguments.append(partResult.result)
                curResult.result = commandClass.execute(graph, arguments)
                stack.pop()
                resultStack.pop()
        return graph.subgraph(curResult.result)
