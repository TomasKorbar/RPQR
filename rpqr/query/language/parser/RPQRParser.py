'''
Project: RPQR
Author: Tomáš Korbař (tomas.korb@seznam.cz)
Copyright 2021 - 2022 Tomáš Korbař
'''

from typing import List

from rpqr.query.commands.RPQRFilteringCommand import RPQRFilteringCommand
from rpqr.loader.plugins.library.RPQRBasePlugin import RPQRBasePlugin
from rpqr.query.language.parser import RPQRPrecedentCommands
from rpqr.library.RPQRConfiguration import RPQRConfiguration
from rpqr.query.language.scanner.RPQRToken import RPQRToken
from rpqr.query.language.parser import RPQRStackSymbol


class RPQRParser:
    """ Parser of RPQR language tokens
    """

    def __init__(self, config: RPQRConfiguration) -> None:
        """ Get instance of RPQRParser

        :param config: provided rpqr configuration
        :type config: RPQRConfiguration
        """
        self.logger = config.rootLogger.getChild("RPQRParser")
        self.config = config
        self.stack = []

        self.nonTerminalTypes = {"statement": config.commandIndex,
                                 "nonResolvedStatement": config.commandIndex+1}

        self.rules = [[config.tokenTypes["leftBracelet"],
                       self.nonTerminalTypes["statement"],
                       config.tokenTypes["rightBracelet"]],
                      [self.nonTerminalTypes["statement"],
                       config.tokenTypes["and"],
                       self.nonTerminalTypes["statement"]],
                      [self.nonTerminalTypes["statement"],
                       config.tokenTypes["or"],
                       self.nonTerminalTypes["statement"]],
                      [config.tokenTypes["not"],
                       self.nonTerminalTypes["statement"]]
                      ]

        # we will dynamically create syntactic rules for language
        # according to available plugins
        for plugin in config.plugins:
            plugin: RPQRBasePlugin
            for command in plugin.implementedCommands:
                command: RPQRFilteringCommand
                rule = [config.commandTypes[command.name]]
                rule.append(config.tokenTypes["leftBracelet"])
                for index, arg in enumerate(command.args):
                    if arg == str:
                        rule.append(config.tokenTypes["string"])
                    elif arg == int:
                        rule.append(config.tokenTypes["number"])
                    elif arg == list:
                        rule.append(self.nonTerminalTypes["statement"])
                    if (index != len(command.args) - 1):
                        rule.append(config.tokenTypes["comma"])
                rule.append(config.tokenTypes["rightBracelet"])
                self.rules.append(rule)

        self.callbacks = [self._collapseBraceletStatement,
                          self._performAnd, self._performOr, self._performNot]

    def _performNot(self):
        """ Resolve not statement on stack
        """
        origStatement = self.stack[-1]
        self.stack = self.stack[:-3]
        neg = RPQRStackSymbol(self.nonTerminalTypes["statement"], [
                              origStatement], operator='~')
        self.stack.append(neg)

    def _collapseBraceletStatement(self):
        """Resolve statement in bracelets on stack
        """
        origStatement = self.stack[-3:][1]
        self.stack = self.stack[:-4]
        self.stack.append(origStatement)

    def _performAnd(self):
        """Resolve And statement on stack
        """
        part = self.stack[-3:]
        self.stack = self.stack[:-4]
        newStatement = RPQRStackSymbol(self.nonTerminalTypes["statement"], [
                                       part[0], part[2]], operator='&')
        self.stack.append(newStatement)

    def _performOr(self):
        """Resolve Or statement on stack
        """
        part = self.stack[-3:]
        self.stack = self.stack[:-4]
        newStatement = RPQRStackSymbol(self.nonTerminalTypes["statement"], [
                                       part[0], part[2]], operator='|')
        self.stack.append(newStatement)

    def parseTokens(self, tokens: List[RPQRToken]) -> RPQRStackSymbol:
        """ parse scanned tokens

        :param tokens: list of RPQR tokens
        :type tokens: List[RPQRToken]
        :return: Abstract Syntactic Tree
        :rtype: RPQRStackSymbol
        """
        self.stack = [RPQRStackSymbol(self.config.tokenTypes["end"])]
        lastTerminalIndex = 0
        curInput = tokens.pop(0)

        # initialize precedenc table
        leftBraceletRow = {self.config.tokenTypes["leftBracelet"]: RPQRPrecedentCommands.LOADMORE,
                           self.config.tokenTypes["rightBracelet"]: RPQRPrecedentCommands.CONTINUE,
                           self.config.tokenTypes["and"]: RPQRPrecedentCommands.LOADMORE,
                           self.config.tokenTypes["or"]: RPQRPrecedentCommands.LOADMORE,
                           self.config.tokenTypes["not"]: RPQRPrecedentCommands.LOADMORE,
                           self.config.tokenTypes["end"]: RPQRPrecedentCommands.ERROR
                           }
        rightBraceletRow = {self.config.tokenTypes["leftBracelet"]: RPQRPrecedentCommands.ERROR,
                            self.config.tokenTypes["rightBracelet"]: RPQRPrecedentCommands.COLLAPSE,
                            self.config.tokenTypes["and"]: RPQRPrecedentCommands.COLLAPSE,
                            self.config.tokenTypes["or"]: RPQRPrecedentCommands.COLLAPSE,
                            self.config.tokenTypes["not"]: RPQRPrecedentCommands.COLLAPSE,
                            self.config.tokenTypes["end"]: RPQRPrecedentCommands.COLLAPSE
                            }
        andRow = {self.config.tokenTypes["leftBracelet"]: RPQRPrecedentCommands.LOADMORE,
                  self.config.tokenTypes["rightBracelet"]: RPQRPrecedentCommands.COLLAPSE,
                  self.config.tokenTypes["and"]: RPQRPrecedentCommands.COLLAPSE,
                  self.config.tokenTypes["or"]: RPQRPrecedentCommands.LOADMORE,
                  self.config.tokenTypes["not"]: RPQRPrecedentCommands.LOADMORE,
                  self.config.tokenTypes["end"]: RPQRPrecedentCommands.COLLAPSE
                  }
        orRow = {self.config.tokenTypes["leftBracelet"]: RPQRPrecedentCommands.LOADMORE,
                 self.config.tokenTypes["rightBracelet"]: RPQRPrecedentCommands.COLLAPSE,
                 self.config.tokenTypes["and"]: RPQRPrecedentCommands.LOADMORE,
                 self.config.tokenTypes["or"]: RPQRPrecedentCommands.COLLAPSE,
                 self.config.tokenTypes["not"]: RPQRPrecedentCommands.LOADMORE,
                 self.config.tokenTypes["end"]: RPQRPrecedentCommands.COLLAPSE
                 }
        notRow = {self.config.tokenTypes["leftBracelet"]: RPQRPrecedentCommands.LOADMORE,
                  self.config.tokenTypes["rightBracelet"]: RPQRPrecedentCommands.COLLAPSE,
                  self.config.tokenTypes["and"]: RPQRPrecedentCommands.COLLAPSE,
                  self.config.tokenTypes["or"]: RPQRPrecedentCommands.COLLAPSE,
                  self.config.tokenTypes["not"]: RPQRPrecedentCommands.LOADMORE,
                  self.config.tokenTypes["end"]: RPQRPrecedentCommands.COLLAPSE
                  }

        endRow = {self.config.tokenTypes["leftBracelet"]: RPQRPrecedentCommands.LOADMORE,
                  self.config.tokenTypes["rightBracelet"]: RPQRPrecedentCommands.ERROR,
                  self.config.tokenTypes["and"]: RPQRPrecedentCommands.LOADMORE,
                  self.config.tokenTypes["or"]: RPQRPrecedentCommands.LOADMORE,
                  self.config.tokenTypes["not"]: RPQRPrecedentCommands.LOADMORE,
                  self.config.tokenTypes["end"]: RPQRPrecedentCommands.SUCCESS
                  }

        precedencTable = {
            self.config.tokenTypes["leftBracelet"]: leftBraceletRow,
            self.config.tokenTypes["rightBracelet"]: rightBraceletRow,
            self.config.tokenTypes["and"]: andRow,
            self.config.tokenTypes["or"]: orRow,
            self.config.tokenTypes["not"]: notRow,
            self.config.tokenTypes["end"]: endRow
        }

        rootStatement = None
        substatementQueue = []
        curStatement = None

        # This algorithm uses precedence syntactic analysis for parsing of statements.
        # In the same time, precedence analysis is not able to handle parsing arguments of functions
        # very well, so every time command is encountered, pick right command rule and merge its
        # call into statement
        # statements used as arguments are put into queue and parsed later with precedence analysis
        while True:
            while True:
                if curInput.type in self.config.commandTypes.values():
                    commandRule = None
                    for rule in self.rules[4:]:
                        if rule[0] == curInput.type:
                            commandRule = rule
                    childList = [curInput]
                    for indexMember, member in enumerate(commandRule[1:]):
                        # if command requires substatement, then cut its tokens
                        # and put it into queue
                        if member == self.nonTerminalTypes["statement"]:
                            subStatement = self._cutSubstatement(
                                tokens, indexMember == len(commandRule[1:]) - 2)
                            if subStatement is None:
                                return None
                            delayedStatement = RPQRStackSymbol(
                                self.nonTerminalTypes["nonResolvedStatement"], subStatement)
                            childList.append(delayedStatement)
                            substatementQueue.append(delayedStatement)
                            continue
                        argToken = tokens.pop(0)
                        if argToken.type != member:
                            self.logger.error(
                                "Bad argument supplied to %s command" % (curInput.content))
                            return None
                        if argToken.type in [self.config.tokenTypes["number"], self.config.tokenTypes["string"]]:
                            childList.append(argToken)
                    newStatement = RPQRStackSymbol(
                        self.nonTerminalTypes["statement"], childList)
                    self.stack.append(newStatement)
                    curInput = tokens.pop(0)
                    continue

                lastTerminalIndex = 0
                for i, e in reversed(list(enumerate(self.stack))):
                    if e.type in self.config.tokenTypes.values():
                        lastTerminalIndex = i
                        break

                requiredAction = precedencTable[self.stack[lastTerminalIndex].type][curInput.type]
                if requiredAction == RPQRPrecedentCommands.ERROR:
                    self.logger.error("Syntax error")
                    return None
                elif requiredAction == RPQRPrecedentCommands.SUCCESS:
                    if rootStatement == None:
                        # we need to hold root so we can return entire tree
                        rootStatement = self.stack[1]
                    else:
                        curStatement: RPQRStackSymbol
                        curStatement.type = self.nonTerminalTypes["statement"]
                        curStatement.setChildren(self.stack[1].children)
                    break
                elif requiredAction == RPQRPrecedentCommands.LOADMORE:
                    self.stack.insert(
                        lastTerminalIndex+1, RPQRStackSymbol(self.config.tokenTypes["loadMore"]))
                    self.stack.append(RPQRStackSymbol(curInput.type))
                    curInput = tokens.pop(0)
                elif requiredAction == RPQRPrecedentCommands.CONTINUE:
                    self.stack.append(RPQRStackSymbol(curInput.type))
                    curInput = tokens.pop(0)
                elif requiredAction == RPQRPrecedentCommands.COLLAPSE:
                    if self._collapseStatement() == False:
                        return None
            # decide whether we need to keep parsing or everything is already done
            if len(substatementQueue) == 0:
                return rootStatement
            else:
                curStatement = substatementQueue.pop(0)
                self.stack = [RPQRStackSymbol(self.config.tokenTypes["end"])]
                tokens = curStatement.children
                curInput = tokens.pop(0)

    def _collapseStatement(self) -> bool:
        """ Perform collapse of statement on stack

        :return: True if collapse was succesfull else false
        :rtype: bool
        """
        toCollapse = []
        for member in reversed(self.stack):
            if member.type is not self.config.tokenTypes["loadMore"]:
                toCollapse.insert(0, member)
            else:
                break

        matchedRuleIndex = None
        for (ruleIndex, rule) in enumerate(self.rules[:4]):
            if (len(rule) != len(toCollapse)):
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
            self.logger.error("Syntax error")
            return False
        self.callbacks[matchedRuleIndex]()
        return True

    def _cutSubstatement(self, tokens: List[RPQRToken], lastArg: bool) -> List[RPQRToken]:
        """ Get tokens related to this argument statement

        :param tokens: list of tokens
        :type tokens: List[RPQRToken]
        :param lastArg: True if this is a last argument of command else False
        :type lastArg: bool
        :return: List of tokens related to this argument
        :rtype: List[RPQRToken]
        """
        subStatement = []
        openBracelets = 0
        ending = self.config.tokenTypes["rightBracelet"] if lastArg else self.config.tokenTypes["comma"]
        while True:
            testedToken = tokens[0]
            if testedToken.type == ending and openBracelets == 0:
                break
            elif testedToken.type == self.config.tokenTypes["leftBracelet"]:
                openBracelets += 1
            elif testedToken.type == self.config.tokenTypes["rightBracelet"]:
                openBracelets -= 1
                if openBracelets < 0:
                    self.logger.error(
                        "Not closed statement supplied as argument")
                    return None
            subStatement.append(tokens.pop(0))
        subStatement.append(RPQRToken(self.config.tokenTypes["end"]))
        return subStatement
