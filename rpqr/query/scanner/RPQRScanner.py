from enum import Enum
import logging
from typing import Optional

from rpqr.library.RPQRComponent import RPQRComponent
from rpqr.loader.plugins.library.RPQRBasePlugin import RPQRBasePlugin
from rpqr.query.Commands.RPQRFilteringCommand import RPQRFilteringCommand

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

class Token:
    def __init__(self, type : int = None, content : str = ""):
        self.type = type
        self.content = content

    def appendToContent(self, what : str):
        self.content += what

class RPQRScanner(RPQRComponent):
    tokenTypes = {"leftBracelet": 0, "rightBracelet": 1,"and": 3, "or": 4, "number": 5, "string": 6, "command": 7}
    commandTypes = {}
    allowedSpecialCharacters = ['&', '|', '-', '.']
    commandIndex = 8
    
    def __init__(self, pluginDirectories):
        super().__init__(pluginDirectories)
        for plugin in self.plugins:
            plugin : RPQRBasePlugin
            for command in plugin.implementedCommands:
                command : RPQRFilteringCommand
                self.commandTypes[command.name] = self.commandIndex
                self.commandIndex += 1

    def getTokens(self, input : str) -> Optional[list]:
        tokens = list()
        curToken = Token()
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
                    curToken = Token(self.tokenTypes["leftBracelet"], c)
                    curState = States.LEFTBRACELET
                elif c == ')':
                    curToken = Token(self.tokenTypes["rightBracelet"], c)
                    curState = States.RIGHTBRACELET
                elif c == '&':
                    curToken = Token(self.tokenTypes["and"], c)
                    curState = States.AND
                elif c == '|':
                    curToken = Token(self.tokenTypes["or"], c)
                    curState = States.OR
                elif c == '\'':
                    curToken = Token(self.tokenTypes["string"], '')
                    curState = States.STARTSTRING
                elif c.isnumeric():
                    curToken = Token(self.tokenTypes["number"], c)
                    curState = States.NUMBER
                elif c.isalpha():
                    curToken = Token(self.tokenTypes["command"], c)
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
        return tokens