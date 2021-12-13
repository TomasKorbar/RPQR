from rpqr.library import RPQRComponent
from rpqr.loader.plugins.library.RPQRBasePlugin import RPQRBasePlugin
from rpqr.query.commands.RPQRFilteringCommand import RPQRFilteringCommand
from rpqr.query.language.parser import RPQRStackSymbol
from rpqr.query.language.scanner import RPQRToken
import networkx 

class RPQRResultTree:
    def __init__(self, result, left, right):
        self.left = left
        self.right = right
        self.result = result

class RPQRInterpreter(RPQRComponent):

    def __init__(self, pluginDirectories):
        super().__init__(pluginDirectories)
        self.commandNameToClass = {}
        for plugin in self.plugins:
            plugin : RPQRBasePlugin
            for command in plugin.implementedCommands:
                command : RPQRFilteringCommand
                self.commandNameToClass[command.name] = command

    def performCommands(self, graph : networkx.MultiGraph, AST: RPQRStackSymbol):
        # (result, symbol)
        stack = []
        resultStack = []
        curNode : RPQRStackSymbol = AST
        curResult : RPQRResultTree = RPQRResultTree(None, None, None)
        stack.append(curNode)
        resultStack.append(curResult)
        while len(stack) > 0:
            curNode = stack[-1]
            curResult = resultStack[-1]
            if curNode.operator is not None:
                if curResult.left is None:
                    curResult.left = RPQRResultTree(None, None, None)
                    resultStack.append(curResult.left)
                    curResult = curResult.left
                    curNode = curNode.children[0]
                    stack.append(curNode)
                elif curResult.right is None:
                    curResult.right = RPQRResultTree(None, None, None)
                    resultStack.append(curResult.right)
                    curResult= curResult.right
                    curNode = curNode.children[1]
                    stack.append(curNode)
                else:
                    leftNodes : networkx.MultiGraph = curResult.left.result
                    rightNodes : networkx.MultiGraph = curResult.right.result
                    validNodes = []
                    if curNode.operator == '&':
                        validNodes = [a for a in list(leftNodes) if a in list(rightNodes)]
                    elif curNode.operator == '|':
                        validNodes = leftNodes
                        for b in list(rightNodes):
                            if b not in validNodes:
                                validNodes.append(b)

                    curResult.result = validNodes
                    stack.pop()
                    resultStack.pop()
            else:
                commandToken : RPQRToken = curNode.children[0]
                commandClass = self.commandNameToClass[commandToken.content]
                arguments = []
                for token in curNode.children[1:]:
                    arguments.append(token.content)
                curResult.result = commandClass.execute(graph, arguments)
                stack.pop()
                resultStack.pop()
        return graph.subgraph(curResult.result)