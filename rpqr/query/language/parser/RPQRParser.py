from rpqr.library import RPQRComponent
from rpqr.query.commands.RPQRFilteringCommand import RPQRFilteringCommand
from rpqr.loader.plugins.library.RPQRBasePlugin import RPQRBasePlugin
from rpqr.query.language.scanner import RPQRScanner
from rpqr.query.language.parser import RPQRPrecedentCommands
from rpqr.query.language.parser import RPQRStackSymbol
import logging


class RPQRParser(RPQRComponent):
    def __init__(self, pluginDirectories):
        super().__init__(pluginDirectories)
        self.stack = []

        self.nonTerminalTypes = {"statement": RPQRScanner.commandIndex}

        self.rules = [[RPQRScanner.tokenTypes["leftBracelet"],
                       self.nonTerminalTypes["statement"],
                       RPQRScanner.tokenTypes["rightBracelet"]],
                      [self.nonTerminalTypes["statement"],
                       RPQRScanner.tokenTypes["and"],
                       self.nonTerminalTypes["statement"]],
                      [self.nonTerminalTypes["statement"],
                       RPQRScanner.tokenTypes["or"],
                       self.nonTerminalTypes["statement"]]
                      ]

        for plugin in self.plugins:
            plugin: RPQRBasePlugin
            for command in plugin.implementedCommands:
                command: RPQRFilteringCommand
                rule = [RPQRScanner.commandTypes[command.name]]
                for arg in command.args:
                    if arg == str:
                        rule.append(RPQRScanner.tokenTypes["string"])
                    elif arg == int:
                        rule.append(RPQRScanner.tokenTypes["number"])
                self.rules.append(rule)

        self.callbacks = [self._collapseBraceletStatement,
                          self._performAnd, self._performOr]

    def _collapseBraceletStatement(self):
        origStatement = self.stack[-3:][1]
        self.stack = self.stack[:-4]
        self.stack.append(origStatement)

    def _performAnd(self):
        part = self.stack[-3:]
        self.stack = self.stack[:-4]
        newStatement = RPQRStackSymbol(self.nonTerminalTypes["statement"], [
                                       part[0], part[2]], operator='&')
        self.stack.append(newStatement)

    def _performOr(self):
        part = self.stack[-3:]
        self.stack = self.stack[:-4]
        newStatement = RPQRStackSymbol(self.nonTerminalTypes["statement"], [
                                       part[0], part[2]], operator='|')
        self.stack.append(newStatement)

    def parseTokens(self, tokens: list):
        self.stack = []
        self.stack.append(RPQRStackSymbol(RPQRScanner.tokenTypes["end"]))
        lastTerminalIndex = 0
        curInput = tokens.pop(0)

        leftBraceletRow = {RPQRScanner.tokenTypes["leftBracelet"]: RPQRPrecedentCommands.LOADMORE,
                           RPQRScanner.tokenTypes["rightBracelet"]: RPQRPrecedentCommands.CONTINUE,
                           RPQRScanner.tokenTypes["and"]: RPQRPrecedentCommands.LOADMORE,
                           RPQRScanner.tokenTypes["or"]: RPQRPrecedentCommands.LOADMORE,
                           RPQRScanner.tokenTypes["end"]: RPQRPrecedentCommands.ERROR
                           }
        rightBraceletRow = {RPQRScanner.tokenTypes["leftBracelet"]: RPQRPrecedentCommands.ERROR,
                            RPQRScanner.tokenTypes["rightBracelet"]: RPQRPrecedentCommands.COLLAPSE,
                            RPQRScanner.tokenTypes["and"]: RPQRPrecedentCommands.COLLAPSE,
                            RPQRScanner.tokenTypes["or"]: RPQRPrecedentCommands.COLLAPSE,
                            RPQRScanner.tokenTypes["end"]: RPQRPrecedentCommands.COLLAPSE
                            }
        andRow = {RPQRScanner.tokenTypes["leftBracelet"]: RPQRPrecedentCommands.LOADMORE,
                  RPQRScanner.tokenTypes["rightBracelet"]: RPQRPrecedentCommands.COLLAPSE,
                  RPQRScanner.tokenTypes["and"]: RPQRPrecedentCommands.COLLAPSE,
                  RPQRScanner.tokenTypes["or"]: RPQRPrecedentCommands.COLLAPSE,
                  RPQRScanner.tokenTypes["end"]: RPQRPrecedentCommands.COLLAPSE
                  }
        orRow = {RPQRScanner.tokenTypes["leftBracelet"]: RPQRPrecedentCommands.LOADMORE,
                 RPQRScanner.tokenTypes["rightBracelet"]: RPQRPrecedentCommands.COLLAPSE,
                 RPQRScanner.tokenTypes["and"]: RPQRPrecedentCommands.LOADMORE,
                 RPQRScanner.tokenTypes["or"]: RPQRPrecedentCommands.COLLAPSE,
                 RPQRScanner.tokenTypes["end"]: RPQRPrecedentCommands.COLLAPSE
                 }
        endRow = {RPQRScanner.tokenTypes["leftBracelet"]: RPQRPrecedentCommands.LOADMORE,
                  RPQRScanner.tokenTypes["rightBracelet"]: RPQRPrecedentCommands.ERROR,
                  RPQRScanner.tokenTypes["and"]: RPQRPrecedentCommands.LOADMORE,
                  RPQRScanner.tokenTypes["or"]: RPQRPrecedentCommands.LOADMORE,
                  RPQRScanner.tokenTypes["end"]: RPQRPrecedentCommands.SUCCESS
                  }

        precedencTable = {
            RPQRScanner.tokenTypes["leftBracelet"]: leftBraceletRow,
            RPQRScanner.tokenTypes["rightBracelet"]: rightBraceletRow,
            RPQRScanner.tokenTypes["and"]: andRow,
            RPQRScanner.tokenTypes["or"]: orRow,
            RPQRScanner.tokenTypes["end"]: endRow
        }

        while True:
            if curInput.type in RPQRScanner.commandTypes.values():
                commandRule = None
                for rule in self.rules[3:]:
                    if rule[0] == curInput.type:
                        commandRule = rule
                childList = [curInput]
                for member in commandRule[1:]:
                    argToken = tokens.pop(0)
                    if argToken.type != member:
                        logging.error(
                            "Bad argument supplied to %s command" % (curInput.content))
                    childList.append(argToken)
                newStatement = RPQRStackSymbol(
                    self.nonTerminalTypes["statement"], childList)
                self.stack.append(newStatement)
                curInput = tokens.pop(0)
                continue
            lastTerminalIndex = 0
            for i, e in reversed(list(enumerate(self.stack))):
                if e.type in RPQRScanner.tokenTypes.values():
                    lastTerminalIndex = i
                    break

            requiredAction = precedencTable[self.stack[lastTerminalIndex].type][curInput.type]
            if requiredAction == RPQRPrecedentCommands.ERROR:
                logging.error("Syntax error")
                return None
            elif requiredAction == RPQRPrecedentCommands.SUCCESS:
                return self.stack[1]
            elif requiredAction == RPQRPrecedentCommands.LOADMORE:
                self.stack.insert(
                    lastTerminalIndex+1, RPQRStackSymbol(RPQRScanner.tokenTypes["loadMore"]))
                self.stack.append(RPQRStackSymbol(curInput.type))
                curInput = tokens.pop(0)
            elif requiredAction == RPQRPrecedentCommands.CONTINUE:
                self.stack.append(RPQRStackSymbol(curInput.type))
                curInput = tokens.pop(0)
            elif requiredAction == RPQRPrecedentCommands.COLLAPSE:
                toCollapse = []
                for member in reversed(self.stack):
                    if member.type is not RPQRScanner.tokenTypes["loadMore"]:
                        toCollapse.insert(0, member)
                    else:
                        break

                matchedRuleIndex = None
                for (ruleIndex, rule) in enumerate(self.rules[:3]):
                    if (len(rule) is not len(toCollapse)):
                        continue
                    match = True
                    for (typeIndex, requiredType) in enumerate(rule):
                        if toCollapse[typeIndex].type is not requiredType:
                            match = False
                            break
                    if match:
                        matchedRuleIndex = ruleIndex
                        break
                if matchedRuleIndex is None:
                    logging.error("Syntax error")
                    return None
                self.callbacks[matchedRuleIndex]()
