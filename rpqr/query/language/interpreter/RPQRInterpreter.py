from rpqr.library.RPQRConfiguration import RPQRConfiguration
from rpqr.loader.plugins.library.RPQRBasePlugin import RPQRBasePlugin
from rpqr.query.commands.RPQRFilteringCommand import RPQRFilteringCommand
from rpqr.query.language.parser import RPQRStackSymbol
from rpqr.query.language.scanner import RPQRToken
from rpqr.query.language.interpreter import RPQRResultTree
import networkx


class RPQRInterpreter:
    def __init__(self, config: RPQRConfiguration):
        self.commandNameToClass = {}
        for plugin in config.plugins:
            plugin: RPQRBasePlugin
            for command in plugin.implementedCommands:
                command: RPQRFilteringCommand
                self.commandNameToClass[command.name] = command

    def performCommands(self, graph: networkx.MultiGraph, AST: RPQRStackSymbol):
        # (result, symbol)
        stack = []
        resultStack = []
        curNode: RPQRStackSymbol = AST
        curResult: RPQRResultTree = RPQRResultTree(None, [])
        stack.append(curNode)
        resultStack.append(curResult)
        while len(stack) > 0:
            curNode = stack[-1]
            curResult = resultStack[-1]
            if curNode.operator is not None:
                if len(curResult.childResults) < 1:
                    leftResult = RPQRResultTree(None, [])
                    curResult.childResults.append(leftResult)
                    resultStack.append(leftResult)
                    curResult = leftResult
                    curNode = curNode.children[0]
                    stack.append(curNode)
                elif curNode.operator != '~' and len(curResult.childResults) < 2:
                    rightResult = RPQRResultTree(None, [])
                    curResult.childResults.append(rightResult)
                    resultStack.append(rightResult)
                    curResult = rightResult
                    curNode = curNode.children[1]
                    stack.append(curNode)
                else:
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
                commandToken: RPQRToken = curNode.children[0]
                commandClass = self.commandNameToClass[commandToken.content]
                commandClass : RPQRFilteringCommand
                notResolvedStatementFound = False
                for argIndex, argType in enumerate(commandClass.args):
                    if argType == str or argType == int:
                        if (argIndex > len(curResult.childResults)-1):
                            curResult.childResults.append(RPQRResultTree(curNode.children[1:][argIndex].content, []))
                        else:
                            continue
                    elif argType == list:
                        if (argIndex > len(curResult.childResults)-1):
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
