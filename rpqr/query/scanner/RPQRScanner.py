from enum import Enum
import logging
from typing import Optional

from rpqr.library.RPQRComponent import RPQRComponent
from rpqr.loader.plugins.library.RPQRBasePlugin import RPQRBasePlugin
from rpqr.query.Commands.RPQRFilteringCommand import RPQRFilteringCommand
from rpqr.query.scanner import RPQRToken

class States(Enum):
    START = 0
    AND = 1
    OR = 2
    NUMBER = 3
    COMMAND = 4
    STARTSTRING = 5
    STRINGCONTENT = 6
    ENDSTRING = 7
    LEFTBRACELET = 8
    RIGHTBRACELET = 9

class RPQRScanner(RPQRComponent):
    tokenTypes = {"leftBracelet": 0, "rightBracelet": 1,"and": 3, "or": 4, "number": 5, "string": 6, "command": 7, "end": 8, "loadMore": 9, "collapse" : 10}
    commandTypes = {}
    allowedSpecialCharacters = ['&', '|', '-', '.']
    commandIndex = 11
    
    def __init__(self, pluginDirectories):
        super().__init__(pluginDirectories)
        for plugin in self.plugins:
            plugin : RPQRBasePlugin
            for command in plugin.implementedCommands:
                command : RPQRFilteringCommand
                RPQRScanner.commandTypes[command.name] = self.commandIndex
                RPQRScanner.commandIndex += 1

    def getTokens(self, input : str) -> Optional[list]:
        tokens = list()
        curToken = RPQRToken()
        curState = States.START
        curInputIndex = 0
        while curInputIndex < len(input) + 1:
            if curInputIndex < len(input):
                c = input[curInputIndex]
            else:
                c = ''
            if curState == States.START:
                if c == '':
                    break
                elif c == '(':
                    curToken = RPQRToken(self.tokenTypes["leftBracelet"], c)
                    curState = States.LEFTBRACELET
                elif c == ')':
                    curToken = RPQRToken(self.tokenTypes["rightBracelet"], c)
                    curState = States.RIGHTBRACELET
                elif c == '&':
                    curToken = RPQRToken(self.tokenTypes["and"], c)
                    curState = States.AND
                elif c == '|':
                    curToken = RPQRToken(self.tokenTypes["or"], c)
                    curState = States.OR
                elif c == '\'':
                    curToken = RPQRToken(self.tokenTypes["string"], '')
                    curState = States.STARTSTRING
                elif c.isnumeric():
                    curToken = RPQRToken(self.tokenTypes["number"], c)
                    curState = States.NUMBER
                elif c.isalpha():
                    curToken = RPQRToken(self.tokenTypes["command"], c)
                    curState = States.COMMAND
                elif not c.isspace():
                    logging.error("Lexical error while reading new token near %s in column %s" % (c, curInputIndex))
                    return None
                curInputIndex += 1
            elif curState == States.AND:
                tokens.append(curToken)
                curState = States.START
            elif curState == States.OR:
                tokens.append(curToken)
                curState = States.START
            elif curState == States.NUMBER:
                if c.isnumeric():
                    curToken.appendToContent(c)
                else:
                    tokens.append(curToken)
                    curState = States.START
                curInputIndex += 1
            elif curState == States.COMMAND:
                if c.isalpha():
                    curToken.appendToContent(c)
                    curInputIndex += 1
                else:
                    if curToken.content not in self.commandTypes.keys():
                        logging.error("Lexical error command %s not implemented" % (curToken.content))
                        return None
                    curToken.type = self.commandTypes[curToken.content]
                    tokens.append(curToken)
                    curState = States.START
            elif curState == States.STARTSTRING:
                if c.isalnum() or c in self.allowedSpecialCharacters:
                    curToken.appendToContent(c)
                    curInputIndex += 1
                    curState = States.STRINGCONTENT
                elif c == '\'':
                    curState = States.ENDSTRING
                else:
                    logging.error("Lexical error while reading string literal near %s in column %s missing '" % (c, curInputIndex))
                    return None
            elif curState == States.STRINGCONTENT:
                if c.isalnum() or c in self.allowedSpecialCharacters:
                    curToken.appendToContent(c)
                    curInputIndex += 1
                elif c == '\'':
                    curState = States.ENDSTRING
                else:
                    logging.error("Lexical error while reading string literal near %s in column %s missing '" % (c, curInputIndex))
                    return None
            elif curState == States.ENDSTRING:
                tokens.append(curToken)
                curInputIndex += 1
                curState = States.START
            elif curState == States.LEFTBRACELET:
                tokens.append(curToken)
                curState = States.START
            elif curState == States.RIGHTBRACELET:
                tokens.append(curToken)
                curState = States.START
        tokens.append(RPQRToken(self.tokenTypes["end"]))
        return tokens